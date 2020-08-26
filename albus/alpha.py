# albus.model


class BaseModel:

    def __init_subclass__(cls):
        super().__init_subclass__()
        cls.__fields = {}

    @classmethod
    def register_field(cls, field):
        cls.__fields[field.name] = field

    @classmethod
    def enumerate_fields(cls):
        for name, field in cls.__fields.items():
            yield name, field


class Model(BaseModel):

    def to_json(self):
        result = {}
        for name, field, value in self.enumerate_field_values():
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

    pass


class IntegerField(Field):

    pass


class StringField(Field):

    pass
