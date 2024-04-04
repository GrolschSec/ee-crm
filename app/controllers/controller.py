from sqlalchemy.orm import Mapped, RelationshipProperty, ColumnProperty
import inspect
from sqlalchemy.exc import IntegrityError


class ModelController:
    model_class = None

    def __init__(self):
        self.errors = {}
        self.fields = self.get_field_names()
        self.validate_methods = self.get_validate_methods()
        self.object = None

    @classmethod
    def get_object(cls, **kwargs):
        return cls.model_class().get_instance(**kwargs)

    def get_field_names(self):
        fields = [
            c.name
            for c in self.model_class.__table__.columns
            if not c.name.startswith("_")
        ]

        properties = [
            name
            for name, value in inspect.getmembers(self.model_class)
            if isinstance(value, property) and not name.startswith("_")
        ]

        fields.extend(properties)

        return fields

    def get_methods(self):
        return [m[0] for m in inspect.getmembers(self, predicate=inspect.ismethod)]

    def get_validate_methods(self):
        methods = self.get_methods()
        return [
            m
            for m in methods
            if m.startswith("validate_") and m.replace("validate_", "") in self.fields
        ]

    def get_validate_fields(self):
        return [m.replace("validate_", "") for m in self.validate_methods]

    def init_errors_field(self, field):
        if field in self.errors:
            self.errors.pop(field)
    
    def retrieve_error(self):
        return next(iter(self.errors.values()))

    def pop_view_args(self, **kwargs):
        view_args = ["request", "obj", "user"]
        for arg in view_args:
            kwargs.pop(arg, None)

        return kwargs

    def validate(self, **kwargs):
        self.values = self.pop_view_args(**kwargs)

        for field in self.get_validate_fields():
            method = getattr(self, f"validate_{field}")

            field_value = self.values.get(field)
            if field_value is None:
                continue

            method(field_value)

    def is_valid(self):
        self.is_valid = not bool(self.errors)
        if self.is_valid:
            self.object = self.model_class(**self.values)
        return self.is_valid

    def save(self):
        if not self.is_valid:
            raise IntegrityError("Invalid data.")
        self.object.save()
