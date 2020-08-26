from . import db


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
        prepared = self.to_internal(value)
        self.__data[obj] = prepared

    def to_internal(self, value):
        return value


class Field(BaseField):

    db_type = None

    def to_json(self, value):
        return value

    def to_internal(self, value):
        return super().to_internal(value)


class IntegerField(Field):

    db_type = db.IntegerType()


class StringField(Field):

    db_type = db.StringType()