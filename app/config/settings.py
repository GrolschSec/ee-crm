from passlib.context import CryptContext
from os import getenv
from dotenv import load_dotenv
import sentry_sdk

load_dotenv()

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

PHONE_REGION = getenv("PHONE_REGION")

sentry_sdk.init(
    dsn=getenv("SENTRY_DSN"),
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
    debug=False,
)

DATABASE = {
    "ENGINE": getenv("DB_ENGINE"),
    "HOST": getenv("DB_HOST"),
    "PORT": getenv("DB_PORT"),
    "NAME": getenv("DB_NAME"),
    "USER": getenv("DB_USER"),
    "PASSWORD": getenv("DB_PASSWORD"),
}

JWT = {
    "SECRET": getenv("JWT_SECRET"),
    "ALGORITHM": getenv("JWT_ALGORITHM"),
    "TOKEN_LIFETIME": int(getenv("JWT_TOKEN_LIFETIME")),
}

TIMEZONE = getenv("TZ")
