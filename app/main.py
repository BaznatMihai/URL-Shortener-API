import os
from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import RedirectResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.exc import IntegrityError
from app.database import Base, engine, SessionLocal
from app.schemas import (
    URLCreate,
    URLResponse,
    UserCreate,
    UserResponse,
    UserLogin,
    URLListResponse,
    URLStatsResponse
)
from app.security import (
    verify_password,
    create_acces_token,
    decode_acces_token
)
from app.services import (
    get_url_by_code,
    get_urls_by_user,
    generate_unique_code,
    get_user_by_username,
    get_user_by_email,
    create_user,
    create_short_url,
    get_user_by_id,
    get_url_by_id,
    delete_url,
    increment_click_count
)

Base.metadata.create_all(bind=engine)
app = FastAPI(
    title = "URL Shortener API",
    description = "An API for shortening URLs"
)
security = HTTPBearer()
BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:8000")

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    user_id = decode_acces_token(token)
    if user_id is None:
        raise HTTPException(
            status_code=401,
            detail="Token invalid sau expirat!"
        )
    db = SessionLocal()
    try:
        user_gasit = get_user_by_id(db, user_id)
    finally:
        db.close()
    if user_gasit is None:
        raise HTTPException(
            status_code=401,
            detail="Utilizatorul nu mai exista"
        )
    return user_gasit

@app.post("/register", response_model=UserResponse, status_code=201)
def register_user(data: UserCreate):
    db = SessionLocal()
    try:
        user_existent = get_user_by_username(db, data.username)
        if user_existent is not None:
            raise HTTPException(status_code=409, detail="User ul este deja folosit")
        email_existent = get_user_by_email(db, data.email)
        if email_existent is not None:
            raise HTTPException(status_code=409, detail="Email ul este deja folosit")
        try:
            user_nou = create_user(db, data.username, data.email, data.password)
        except IntegrityError:
            raise HTTPException(
                status_code=409,
                detail="Username ul sau Email ul este deja folosit"
            )
        except ValueError as e:
            raise HTTPException(
                status_code=422,
                detail=str(e)
            )
        return user_nou
    finally:
        db.close()

@app.post("/login")
def login_user(data: UserLogin):
    db = SessionLocal()
    try:
        user_gasit = get_user_by_username(db, data.username)
        if user_gasit is None:
            raise HTTPException(
                status_code=401,
                detail= "Username sau parola incorecta!"
            )
        parola_corecta = verify_password(data.password, user_gasit.hashed_password)
        if parola_corecta is False:
            raise HTTPException(
                status_code=401,
                detail="Username sau parola incorecta!"
            )
        token = create_acces_token(user_gasit.id)
        return {
            "Access Token": token,
            "Token Type": "bearer"
        }
    finally:
        db.close()

@app.get("/me", response_model=UserResponse)
def read_me(current_user = Depends(get_current_user)):
    return current_user

@app.post("/shorten", response_model=URLResponse)
def shorten_url(data: URLCreate, current_user = Depends(get_current_user)):
    original_url = str(data.original_url)
    db = SessionLocal()
    try:
        for i in range(3):
            try:
                cod = generate_unique_code(db)
                url_nou = create_short_url(db, original_url, cod, current_user.id)
                break
            except IntegrityError:
                continue
        else:
            raise HTTPException(
                status_code=503,
                detail="Nu s-a putut genera un cod scurt"
            )
    finally:
        db.close()
    short_url = f"{BASE_URL.rstrip('/')}/{url_nou.short_code}"
    return {
        "id": url_nou.id,
        "original_url": url_nou.original_url,
        "short_url": short_url
    }

@app.get("/my-urls", response_model=list[URLListResponse])
def my_urls(current_user=Depends(get_current_user)):
    db=SessionLocal()
    try:
        url_uri = get_urls_by_user(db, current_user.id)
        return url_uri
    finally:
        db.close()

@app.delete("/urls/{url_id}")
def remove_url(url_id: int, current_user=Depends(get_current_user)):
    db = SessionLocal()
    try:
        url_gasit=get_url_by_id(db, url_id)
        if url_gasit is None:
            raise HTTPException(
                status_code=404,
                detail="URL-ul nu exista!"
            )
        elif url_gasit.user_id !=current_user.id:
            raise HTTPException(
                status_code=403,
                detail="Nu ai permisiunea sa stergi acest URL"
            )
        delete_url(db, url_gasit)
        return{
            "Mesaj": "URL-ul a fost sters cu succes!"
        }
    finally:
        db.close()

@app.get("/shorten/{short_code}/stats", response_model=URLStatsResponse)
def get_url_stats(short_code: str, current_user=Depends(get_current_user)):
    db=SessionLocal()
    try:
        url_gasit = get_url_by_code(db, short_code)
        if url_gasit is None:
            raise HTTPException(
                status_code=404,
                detail="URL-ul nu a fost gasit!"
            )
        elif url_gasit.user_id!=current_user.id:
            raise HTTPException(
                status_code=403,
                detail="Nu ai accesul pentru aceste URL-uri"
            )
        return url_gasit
    finally:
        db.close()

@app.get("/{short_code}")
def redirect_url(short_code: str):
    db = SessionLocal()
    try:
        url_gasit = get_url_by_code(db, short_code)

        if url_gasit is None:
            raise HTTPException(
                status_code=404,
                detail="URL-ul nu a fost gasit"
            )
        else:
            increment_click_count(db, url_gasit)
            return RedirectResponse(
                url=url_gasit.original_url,
                status_code=307
            )
    finally:
        db.close()