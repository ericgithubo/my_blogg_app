from passlib.context import CryptContext
import hashlib

pwd_context = CryptContext(schemes= ["bcrypt"],deprecated ="auto")


def hash(password:str):
    return pwd_context.hash(password)