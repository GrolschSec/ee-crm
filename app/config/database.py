from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config.settings import DATABASE

DATABASE_URL = f"{DATABASE['ENGINE']}://{DATABASE['USER']}:{DATABASE['PASSWORD']}@{DATABASE['HOST']}:{DATABASE['PORT']}/{DATABASE['NAME']}"

engine = create_engine(DATABASE_URL)

_Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Session = None

def get_session():
    global Session
    if Session is None:
        Session = _Session
    return Session()
