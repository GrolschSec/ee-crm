from app.models import Client
from app.controllers.controller import ModelController


class ClientController(ModelController):
    model_class = Client

    def validate_fullname(self, fullname):
        self.init_errors_field("fullname")
        if (len(fullname) < 6) or (len(fullname) > 50):
            self.errors["fullname"] = "Fullname must be between 6 and 50 characters."
            return False
        if not fullname.replace(" ", "").isalpha():
            self.errors["fullname"] = "Fullname must contain only alphabets."
            return False
        return True

    # is there a way to check if a client with the given field and value exists?
    # by trying to create a client with the same field and value and catching the exception if it exists
    # i should be able to do that since for the email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    # phone: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)

#     @classmethod
#     def validate_phone(cls, phone):
#         message = "invalid phone number."
#         try:
#             parsed_phone = parse(phone, PHONE_REGION)
#             normalized_phone = format_number(parsed_phone, PhoneNumberFormat.E164)
#             if not is_valid_number(parsed_phone):
#                 return [False, message]
#         except phonenumberutil.NumberParseException:
#             return [False, message]
#         if cls.phone_exist(normalized_phone):
#             return [False, "a client with this phone number already exists."]
#         return [True, normalized_phone]
