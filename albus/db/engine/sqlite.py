import sqlite3
from uuid import uuid4

from .base import Architect, Engine, QueryBuilder


class SQLite3Architect(Architect):

    def execute(self, query):
        cursor = self._con.cursor()
        cursor.execute(query)
        return cursor

    def create_model(self, model):
        table_name = model.get_table_name()
        self.execute(f'CREATE TABLE {table_name}(id);')
        for name, field in model.enumerate_fields():
            self.create_field(table_name, field)
        self._con.commit()

    def create_field(self, table_name, field):
        name = field.name
        if name != 'id':
            self.execute(f'ALTER TABLE {table_name} ADD COLUMN {name};')
            self._con.commit()


class SQLite3QueryBuilder(QueryBuilder):

    def build_where_clause(self):
        return 'WHERE foo = ?'


class SQLite3Engine(Engine):

    ddl_class = SQLite3Architect

    def __init__(self, in_memory=False):
        self._in_memory = in_memory
        super().__init__()

    def _get_filename(self):
        if self._in_memory:
            filename = ':memory:'
        else:
            filename = 'albus.db'
        return filename

    def _generate_pk(self, model):
        return uuid4().hex

    def connect(self):
        filename = self._get_filename()
        self._con = sqlite3.connect(filename)

    def cursor(self):
        return self._con.cursor()

    def commit(self):
        self._con.commit()

    def fetch(self, model, pk, fields):
        table = model.get_table_name()
        columns = ', '.join([f.name for f in fields])
        sql = f'SELECT {columns} from {table} WHERE id=?;'
        cursor = self.cursor()
        cursor.execute(sql, [pk])
        row = cursor.fetchone()
        cursor.close()
        values = []
        assert len(row) == len(fields)
        for idx in range(len(fields)):
            current_field = fields[idx]
            current_value = current_field.from_db(row[idx])
            values.append(current_value)
        return values

    def insert(self, model, fields, values):
        pk = self._generate_pk(model)

        names = ['id'] + [f.name for f in fields]
        literals = [pk] + [v for v in values]

        columns = ', '.join(names)
        params = ', '.join(['?'] * len(literals))
        table = model.get_table_name()
        dml = f'INSERT INTO {table} ({columns}) VALUES ({params});'

        cursor = self.cursor()
        cursor.execute(dml, literals)
        self.commit()
        cursor.close()

        return pk

    def update(self, model, fields, values):
        table = model.get_table_name()
        assignments_list = []
        for current_field in fields:
            column_name = current_field.name
            current_assignment = f'\n\t{column_name} = ?'
            assignments_list.append(current_assignment)
        assignments = ','.join(assignments_list)
        dml = f'UPDATE {table} SET {assignments};'

        cursor = self.cursor()
        cursor.execute(dml, values)
        self.commit()
        cursor.close()

    def delete(self, model, pk):
        table = model.get_table_name()
        dml = f'DELETE FROM {table} WHERE id=?;'
        cursor = self.cursor()
        cursor.execute(dml, [pk])
        self.commit()
        cursor.close()
