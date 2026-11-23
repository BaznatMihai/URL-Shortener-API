import bcrypt
import os
from dotenv import load_dotenv
import jwt
from jwt import InvalidTokenError
from datetime import datetime, timedelta, timezone

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY nu este configurata in .env")

def hash_password (password: str) -> str:
    password_bytes = password.encode("utf-8")
    if len(password_bytes) >72:
        raise ValueError("Parola este prea lunga!")
    salt = bcrypt.gensalt()
    hashed_bytes = bcrypt.hashpw(password_bytes, salt)
    return hashed_bytes.decode("utf-8")

def verify_password(password: str, hashed_password: str) ->bool:
    password_bytes =password.encode("utf-8")
    if len(password_bytes)>72:
        return False
    hashed_bytes = hashed_password.encode("utf-8")
    return bcrypt.checkpw(password_bytes, hashed_bytes)

def create_acces_token(user_id: int)->str:
    expirare = datetime.now(timezone.utc)+timedelta(
        minutes= ACCESS_TOKEN_EXPIRE_MINUTES
    )
    payload = {
        "sub": str(user_id),
        "exp": expirare
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token

def decode_acces_token(token: str) ->int | None:
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        user_id = payload.get("sub")
        if user_id is None:
            return None
        return int(user_id)
    except (InvalidTokenError, ValueError, TypeError):
        return None