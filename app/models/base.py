from sqlalchemy.orm import DeclarativeBase, validates, joinedload
from sqlalchemy.exc import IntegrityError
from email_validator import validate_email, EmailNotValidError
from phonenumbers import (
    parse,
    is_valid_number,
    phonenumberutil,
    format_number,
    PhoneNumberFormat,
)
from app.config.settings import PHONE_REGION
from app.config.database import Session


class Base(DeclarativeBase):
    @validates("email")
    def validate_email(self, key, email):
        try:
            validate_email(email)
            return email
        except EmailNotValidError as e:
            raise ValueError("Invalid email.")

    @validates("phone")
    def validate_phone(self, key, phone):
        try:
            parsed_phone = parse(phone, PHONE_REGION)
            formatted_phone = format_number(parsed_phone, PhoneNumberFormat.E164)
            if not is_valid_number(parsed_phone):
                raise ValueError("Invalid phone number.")
        except phonenumberutil.NumberParseException as e:
            raise ValueError("Invalid phone number.")
        return formatted_phone

    def save(self):
        session = Session()
        session.merge(self)
        session.commit()
        session.close()

    def try_flush(self):
        session = Session()
        session.merge(self)
        try:
            session.flush()
        except IntegrityError as e:
            error_info = e.orig.args[0] if e.orig.args else str(e)
            if "unique constraint" in error_info:
                field_name = error_info.split('"')[1].split("_")
                field_value = error_info.split("=")[1].split(")")[0].replace("(", "")
                raise ValueError(
                    f"the {field_name[1]} '{field_value}' already exists in database."
                )
            else:
                raise ValueError(f"Database: {error_info}")
        finally:
            session.rollback()
            session.close()

    @classmethod
    def get_instance(cls, id: int = None, **kwargs):
        query_res = None
        session = Session()
        if id:
            query_res = session.query(cls).options(joinedload("*")).get(id)
        if kwargs:
            query_res = (
                session.query(cls).options(joinedload("*")).filter_by(**kwargs).first()
            )
        session.close()
        return query_res

    def refresh(self):
        session = Session()
        session.refresh(self)
        return self

    @classmethod
    def filter_by(cls, **kwargs):
        session = Session()
        query_res = session.query(cls).filter_by(**kwargs)
        session.close()
        return query_res

    @classmethod
    def all(cls):
        session = Session()
        query_res = session.query(cls).all()
        session.close()
        return query_res
