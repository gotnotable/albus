from collections import defaultdict

from .db.engine import SQLite3Engine


class BaseModel:

    __fields = defaultdict(dict)
    table_name = None

    @classmethod
    def get_table_name(cls):
        table_name = cls.table_name
        if table_name is None:
            table_name = cls.__name__.lower()
        return table_name

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

    def to_db(self):
        all_fields = []
        all_values = []
        for name, field, value in self.enumerate_fields_values():
            all_fields.append(field)
            all_values.append(value)
        return all_fields, all_values

    def enumerate_fields_values(self):
        for name, field in type(self).enumerate_fields():
            value = getattr(self, name)
            yield name, field, value

    def save(self):
        model = type(self)
        fields, values = self.to_db()
        self.db_engine.insert(model, fields, values)
