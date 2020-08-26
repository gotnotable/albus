import sqlite3

from .base import Architect, Engine


class SQLite3Architect(Architect):

    def execute(self, query):
        cursor = self._con.cursor()
        cursor.execute(query)
        return cursor

    def create_model(self, model):
        self.execute('CREATE TABLE book(a, b);')
        self._con.commit()


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

    def connect(self):
        filename = self._get_filename()
        self._con = sqlite3.connect(filename)

    def cursor(self):
        return self._con.cursor()
