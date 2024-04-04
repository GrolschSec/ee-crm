from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey
from datetime import datetime, timedelta
from jwt import encode, decode, ExpiredSignatureError, DecodeError
from passlib.exc import UnknownHashError
from app.config.settings import pwd_context, JWT, TIMEZONE
from .base import Base
from app.config.database import Session
from sqlalchemy.orm import joinedload
from pytz import timezone
from app.models.role import Role
from sqlalchemy.orm.exc import NoResultFound


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    fullname: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    _password: Mapped[str] = mapped_column(String(255), nullable=False)
    _role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"))
    is_active: Mapped[bool] = mapped_column(default=True)
    is_admin: Mapped[bool] = mapped_column(default=False)

    clients = relationship("Client", back_populates="sales_contact")
    events = relationship("Event", back_populates="support_contact")

    @property
    def role(self):
        with Session() as session:
            role = session.query(Role).get(self._role_id)
        return role.name if role else None

    @role.setter
    def role(self, role_name):
        with Session() as session:
            try:
                role = session.query(Role).filter_by(name=role_name).one()
                self._role_id = role.id
            except NoResultFound:
                raise ValueError(f"Role {role_name} not found.")

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
        tz = timezone(TIMEZONE)
        exp = datetime.now(tz) + timedelta(hours=JWT["TOKEN_LIFETIME"])
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
