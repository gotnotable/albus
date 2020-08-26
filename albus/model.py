from collections import defaultdict

from .db.engine import SQLite3Engine


class BaseModel:

    __fields = defaultdict(dict)

    @classmethod
    def register_field(cls, field):
        cls.__fields[cls][field.name] = field

    @classmethod
    def enumerate_fields(cls):
        for name, field in cls.__fields[cls].items():
            yield name, field


class Model(BaseModel):

    db_engine = SQLite3Engine(in_memory=True)

    def to_json(self):
        result = {}
        for name, field, value in self.enumerate_fields_values():
            result[name] = field.to_json(value)
        return result

    def enumerate_fields_values(self):
        for name, field in type(self).enumerate_fields():
            value = getattr(self, name)
            yield name, field, value
