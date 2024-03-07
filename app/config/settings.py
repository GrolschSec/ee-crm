from passlib.context import CryptContext
from os import getenv
from dotenv import load_dotenv

load_dotenv()

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

PHONE_REGION = "FR"

DATABASE = {
    "ENGINE": getenv("DB_ENGINE"),
    "HOST": getenv("DB_HOST"),
    "PORT": getenv("DB_PORT"),
    "NAME": getenv("DB_NAME"),
    "USER": getenv("DB_USER"),
    "PASSWORD": getenv("DB_PASSWORD"),
}
