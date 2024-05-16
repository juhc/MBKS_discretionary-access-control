import jwt
import bcrypt

from datetime import datetime, timedelta

from config import settings


def jwt_encode(
    payload: dict,
    private_key: str = settings.auth.private_key.read_text(),
    algorithm: str = settings.auth.algorithm,
    expire_minutes: int = settings.auth.access_token_expire_minutes,
) -> str:
    to_encode = payload.copy()
    now = datetime.utcnow()
    expire = now + timedelta(minutes=expire_minutes)
    to_encode.update(exp=expire, iat=now)
    encoded = jwt.encode(to_encode, private_key, algorithm)

    return encoded


def jwt_decode(
    token: str | bytes,
    public_key: str = settings.auth.public_key.read_text(),
    algorithm: str = settings.auth.algorithm,
) -> dict:
    decoded = jwt.decode(token, public_key, algorithms=[algorithm])

    return decoded


def hash_password(password: str) -> bytes:
    salt = bcrypt.gensalt()
    password_bytes: bytes = password.encode()

    return bcrypt.hashpw(password_bytes, salt)


def validate_password(password: str, hashed_password: bytes) -> bool:
    password_bytes = password.encode()

    return bcrypt.checkpw(password_bytes, hashed_password)
