from jose import jwt, JWTError
from core.config import JWT_SECRET, JWT_ALGORITHM

def verify_jwt(token: str):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload["sub"]
    except JWTError:
        return None