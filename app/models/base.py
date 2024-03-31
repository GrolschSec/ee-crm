from sqlalchemy.orm import DeclarativeBase, validates, joinedload
from email_validator import validate_email, EmailNotValidError
from phonenumbers import parse, is_valid_number, phonenumberutil
from app.config.settings import PHONE_REGION
from app.config.database import Session


class Base(DeclarativeBase):
    @validates("email")
    def validate_email(self, key, email):
        try:
            validate_email(email)
            return email
        except EmailNotValidError as e:
            raise ValueError(str(e))

    @validates("phone")
    def validate_phone(self, key, phone):
        try:
            parsed_phone = parse(phone, PHONE_REGION)
            if not is_valid_number(parsed_phone):
                raise ValueError("Invalid phone number.")
        except phonenumberutil.NumberParseException as e:
            raise ValueError(str(e))
        return phone

    def save(self):
        session = Session()
        session.merge(self)
        session.commit()
        session.close()

    @classmethod
    def get_instance(cls, id: int = None, **kwargs):
        query_res = None
        session = Session()
        if id:
            query_res = session.query(cls).options(joinedload("*")).get(id)
        if kwargs:
            query_res = session.query(cls).options(joinedload("*")).filter_by(**kwargs).first()
        session.close()
        return query_res

    @classmethod
    def filter_by(cls, **kwargs):
        session = Session()
        query_res = session.query(cls).filter_by(**kwargs)
        session.close()
        return query_res
