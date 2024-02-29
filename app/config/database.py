from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .settings import DB_USER, DB_PASSWORD, DB_HOST, DB_NAME, DB_ENGINE, DB_PORT

DATABASE_URL = f"{DB_ENGINE}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL)

Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
