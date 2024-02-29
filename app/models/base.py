from sqlalchemy.orm import DeclarativeBase, validates
from email_validator import validate_email, EmailNotValidError
from phonenumbers import parse, is_valid_number, phonenumberutil
from app.config.settings import PHONE_REGION


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
