from unittest import TestCase

from albus.db.engine import SQLite3Engine
from albus.field import IntegerField, StringField
from albus.model import Model


class BaseDbTest(TestCase):

    def setUp(self):
        self.engine = SQLite3Engine(in_memory=True)

    def assertTableExist(self, table_name):
        query = 'SELECT name from sqlite_master where type=? and name=?'
        params = ('table', table_name)
        cursor = self.engine.cursor()
        cursor.execute(query, params)
        got = cursor.fetchone()
        self.assertIsNotNone(got, f"Table {table_name} is missing")


class CreateSimpleModelTest(BaseDbTest):

    def setUp(self):
        class Book(Model):
            title = StringField()
            rank = IntegerField()

        self.Book = Book
        self.engine = SQLite3Engine(in_memory=True)

    def test_create_model(self):
        self.engine.ddl.create_model(self.Book)
        self.assertTableExist('book')
