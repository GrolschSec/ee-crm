from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config.settings import DB_USER, DB_PASSWORD, DB_HOST, DB_NAME

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:5432/{DB_NAME}"

engine = create_engine(DATABASE_URL)

Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
