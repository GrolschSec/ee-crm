from passlib.context import CryptContext
from os import getenv
from dotenv import load_dotenv

load_dotenv()

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

PHONE_REGION = "FR"

DATABASE = {
	"DB_USER": getenv("DB_USER"),
	"DB_PASSWORD": getenv("DB_PASSWORD"),
	"DB_HOST": getenv("DB_HOST"),
	"DB_NAME": getenv("DB_NAME"),
	"DB_ENGINE": getenv("DB_ENGINE"),
	"DB_PORT": getenv("DB_PORT")
}
