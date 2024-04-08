import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base, Role, User, Client, Contract
from app.config import database


@pytest.fixture(scope="session")
def engine():
    return create_engine("sqlite:///:memory:")


@pytest.fixture(scope="session")
def session_obj(engine):
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function", autouse=True)
def mock_session(session_obj, monkeypatch):
    monkeypatch.setattr(database, "Session", session_obj)


@pytest.fixture(scope="function")
def setup_database(engine):
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)


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
def set_roles_to_db(
    setup_database,
    session_obj,
    role_management,
    role_support,
    role_sales,
    role_admin,
    role_anonymous,
):
    session = session_obj()
    session.add_all(
        [role_management, role_support, role_sales, role_admin, role_anonymous]
    )
    session.commit()


def create_user(email, role):
    user = User(
        fullname="test",
        email=email,
        password="password",
        role=role,
    )
    user.save()
    return user


@pytest.fixture()
def sales_user():
    return create_user("test_sales@gmail.com", "sales")


@pytest.fixture()
def support_user():
    return create_user("test_support@gmail.com", "support")


@pytest.fixture()
def management_user():
    return create_user("test_management@gmail.com", "management")


@pytest.fixture()
def admin_user():
    return create_user("test_admin@gmail.com", "admin")

@pytest.fixture()
def client(sales_user):
    user_id = sales_user.id
    sales_user.close()
    client = Client(
        fullname="Test Client",
        email="test_client@gmail.com",
        phone="+33695454332",
        address="123 Test St",
        company_name="Test Company",
        sales_contact_id=user_id,
    )
    client.save()
    return client

@pytest.fixture()
def contract(client):
    client_id = client.id
    client.close()
    contract = Contract(
        client_id=client_id,
        amount_total=1000.00,
        amount_due=500.00,
    )
    contract.save()
    return contract
