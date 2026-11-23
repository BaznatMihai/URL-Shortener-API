import secrets
import string
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from app.models import URL, User
from app.security import hash_password

# Functii pentru url-uri

def get_url_by_code(db, short_code):
    stmt = select(URL).where(URL.short_code == short_code)
    url_gasit = db.scalars(stmt).first()
    return url_gasit

def get_url_by_id(db, url_id):
    stmt = select(URL).where(URL.id == url_id)
    url_ul = db.scalars(stmt).first()
    return url_ul

def get_urls_by_user(db, user_id):
    stmt = select(URL).where(URL.user_id == user_id)
    url_uri = db.scalars(stmt).all()
    return url_uri

def generate_short_code():
    caractere = string.ascii_letters + string.digits
    cod = ""
    for i in range(6):
        cod += secrets.choice(caractere)
    return cod

def generate_unique_code(db):
    while True:
        cod = generate_short_code()
        url_existent = get_url_by_code(db, cod)
        if url_existent is None:
            return cod

def create_short_url(db, original_url, short_code, user_id):
    url_nou = URL(
        original_url=original_url,
        short_code=short_code,
        user_id=user_id
    )
    db.add(url_nou)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise
    db.refresh(url_nou)
    return url_nou

def delete_url(db, url_ul):
    db.delete(url_ul)
    db.commit()

def increment_click_count(db, url_ul):
    url_ul.click_count += 1
    db.commit()

# Functii pentru utilizatori
def get_user_by_username(db, username):
    stmt = select(User).where(User.username == username)
    user_gasit = db.scalars(stmt).first()
    return user_gasit

def get_user_by_email(db, email):
    stmt = select(User).where(User.email == email)
    user_gasit = db.scalars(stmt).first()
    return user_gasit

def get_user_by_id(db, user_id):
    stmt = select(User).where(User.id == user_id)
    user_gasit = db.scalars(stmt).first()
    return user_gasit

def create_user(db, username, email, password):
    hashed_password = hash_password(password)
    user_nou = User(
        username=username,
        email=email,
        hashed_password=hashed_password
    )
    db.add(user_nou)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise
    db.refresh(user_nou)
    return user_nou