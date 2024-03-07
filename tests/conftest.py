import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base, Role, User


@pytest.fixture()
def engine():
    test_database = "sqlite:///:memory:"
    return create_engine(test_database)

@pytest.fixture()
def session(engine):
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = SessionLocal()
    yield session
    session.close()

@pytest.fixture()
def role_management():
    return Role(name="management")

@pytest.fixture()
def role_support():
    return Role(name="support")

@pytest.fixture()
def role_sales():
    return Role(name="sales")

@pytest.fixture(autouse=True)
def set_role_to_db(session, role_management, role_support, role_sales):
	session.add_all([role_management, role_support, role_sales])
	session.commit()
	return session.query(Role).all()

@pytest.fixture()
def testuser(session, role_sales):
    user = User(fullname="test", email="test@gmail.com", password="password", role_id=role_sales.id)
    session.add(user)
    session.commit()
    return user
