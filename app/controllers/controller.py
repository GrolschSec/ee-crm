from sqlalchemy.exc import IntegrityError
import inspect


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
        try:
            obj = self.model_class(**self.values)
            obj.try_flush()
        except Exception as e:
            self.errors["db"] = str(e)

    def is_valid(self):
        self.is_valid = not bool(self.errors)
        if self.is_valid:
            self.object = self.model_class(**self.values)
        return self.is_valid

    def save(self):
        if not self.is_valid:
            raise ValueError("Invalid data.")
        self.object.save()

    def list(self):
        return self.model_class.all()

    def update(self, **kwargs):
        self.updated = False
        obj = kwargs.get("obj")
        self.values = {}

        if obj is None:
            return "No object provided for update."

        self.validate(**kwargs)
        if not self.is_valid:
            return self.retrieve_error()
        for field in self.fields:
            if kwargs.get(field):
                setattr(obj, field, kwargs.get(field))
                self.updated = True
        if self.updated:
            obj.save()
            return f"{type(obj).__name__} updated successfully."
        return "No changes detected."

    def delete(self, **kwargs):
        raise NotImplementedError
