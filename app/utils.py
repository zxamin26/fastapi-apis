import jwt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()


def hasher(password: str):
    return password_hash.hash(password)

def verify_pass(plain_password,hashed_password):
    return password_hash.verify(plain_password,hashed_password)