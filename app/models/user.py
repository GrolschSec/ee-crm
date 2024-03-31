from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey
from datetime import datetime, timedelta
from jwt import encode, decode, ExpiredSignatureError, DecodeError
from passlib.exc import UnknownHashError
from app.config.settings import pwd_context, JWT
from .base import Base
from app.config.database import Session
from sqlalchemy.orm import joinedload


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    fullname: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    _password: Mapped[str] = mapped_column(String(255), nullable=False)
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"))

    role = relationship("Role", back_populates="users")
    clients = relationship("Client", back_populates="sales_contact")
    events = relationship("Event", back_populates="support_contact")

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, plain_text_passwd):
        self._password = pwd_context.hash(plain_text_passwd)

    def verify_password(self, plain_text_passwd):
        try:
            return pwd_context.verify(plain_text_passwd, self._password)
        except UnknownHashError:
            return False

    def generate_jwt_token(self):
        exp = datetime.utcnow() + timedelta(hours=JWT["TOKEN_LIFETIME"])
        token = encode(
            {"id": self.id, "exp": exp}, JWT["SECRET"], algorithm=JWT["ALGORITHM"]
        )
        return token

    @staticmethod
    def verify_jwt_token(token):
        try:
            payload = decode(token, JWT["SECRET"], algorithms=[JWT["ALGORITHM"]])
            return payload["id"]
        except ExpiredSignatureError:
            return None
        except DecodeError:
            return None

    @classmethod
    def get_first_by_role(cls, **kwargs):
        session = Session()
        return session.query(User).filter(User.role.has(**kwargs)).first()

    @classmethod
    def all(cls):
        session = Session()
        query_res = session.query(cls).options(joinedload(cls.role)).all()
        session.close()
        return query_res
