from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from settings import DATABASE

DATABASE_URL = f"{DATABASE['DB_ENGINE']}://{DATABASE['DB_USER']}:{DATABASE['DB_PASSWORD']}@{DATABASE['DB_HOST']}:{DATABASE['DB_PORT']}/{DATABASE['DB_NAME']}"

engine = create_engine(DATABASE_URL)

Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
