from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from settings import DATABASE

DATABASE_URL = f"{DATABASE['ENGINE']}://{DATABASE['USER']}:{DATABASE['PASSWORD']}@{DATABASE['HOST']}:{DATABASE['PORT']}/{DATABASE['NAME']}"

engine = create_engine(DATABASE_URL)

Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
