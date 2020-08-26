# albus.model
from collections import defaultdict

from . import db


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

    def to_json(self):
        result = {}
        for name, field, value in self.enumerate_fields_values():
            result[name] = field.to_json(value)
        return result

    def enumerate_fields_values(self):
        for name, field in type(self).enumerate_fields():
            value = getattr(self, name)
            yield name, field, value


class BaseField:

    def __init__(self, default=None):
        self.__data = {}
        self.default = default

    def __set_name__(self, owner, name):
        self.owner = owner
        self.name = name
        owner.register_field(self)

    def __get__(self, obj, owner=None):
        if obj is None:
            return self
        return self.__data.get(obj, self.default)

    def __set__(self, obj, value):
        self.__data[obj] = value


class Field(BaseField):

    db_type = None

    def to_json(self, value):
        return value


class IntegerField(Field):

    db_type = db.IntegerType()


class StringField(Field):

    db_type = db.StringType()
