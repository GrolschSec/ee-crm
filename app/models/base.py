from typing import Any
from app.config.settings import PHONE_REGION
from app.config.database import get_session
from sqlalchemy.orm import DeclarativeBase, validates, joinedload
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from email_validator import validate_email, EmailNotValidError
from phonenumbers import (
    parse,
    is_valid_number,
    phonenumberutil,
    format_number,
    PhoneNumberFormat,
)


class Base(DeclarativeBase):
    def __init__(self, **kwargs: Any):
        super().__init__()
        self.session = get_session()
        for key, value in kwargs.items():
            setattr(self, key, value)

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
        self.session.add(self)
        self.session.commit()
        return self

    def close(self):
        self.session.close()

    def try_flush(self):
        self.session.merge(self)
        try:
            self.session.flush()
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
            self.session.rollback()

    @classmethod
    def get_instance(cls, id: int = None, **kwargs):
        instance = None
        session = get_session()
        if id:
            stmt = select(cls).options(joinedload("*")).where(cls.id == id)
            result = session.execute(stmt)
            instance = result.scalars().first()
        if kwargs and not instance:
            stmt = select(cls).options(joinedload("*")).where(*[getattr(cls, k)==v for k, v in kwargs.items()])
            result = session.execute(stmt)
            instance = result.scalars().first()
        if instance:
            instance.session = session
        else:
            session.close()
        return instance

    @classmethod
    def all(cls):
        session = get_session()
        stmt = select(cls)
        result = session.execute(stmt)
        instance_lst = result.scalars().all()
        return [instance_lst, session]
