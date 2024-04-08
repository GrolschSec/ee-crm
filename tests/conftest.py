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

@pytest.fixture()
def role_admin():
    return Role(name="admin")

@pytest.fixture()
def role_anonymous():
    return Role(name="anonymous")


@pytest.fixture(autouse=True)
def set_roles_to_db(session, role_management, role_support, role_sales, role_admin, role_anonymous):
    session.add_all([role_management, role_support, role_sales, role_admin, role_anonymous])
    session.commit()
    return session.query(Role).all()


def create_user(session, email, role):
    user = User(
        fullname="test",
        email=email,
        password="password",
        role=role,
    )
    session.add(user)
    session.commit()
    return user

@pytest.fixture()
def sales_user(session):
    return create_user(session, "test_sales@gmail.com", "sales")

@pytest.fixture()
def support_user(session):
    return create_user(session, "test_support@gmail.com", "support")

@pytest.fixture()
def management_user(session):
    return create_user(session, "test_management@gmail.com", "management")

@pytest.fixture()
def admin_user(session):
    return create_user(session, "test_admin@gmail.com", "admin")
