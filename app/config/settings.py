from passlib.context import CryptContext
from os import getenv

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

PHONE_REGION = "FR"

DB_USER = getenv("DB_USER")

DB_PASSWORD = getenv("DB_PASSWORD")

DB_HOST = getenv("DB_HOST")

DB_NAME = getenv("DB_NAME")

