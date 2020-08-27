from unittest import TestCase

from albus.db.engine import SQLite3Engine
from albus.field import IntegerField, StringField
from albus.model import Model


class BaseDbTest(TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._engine = None

    @property
    def engine(self):
        if self._engine is None:
            self._engine = SQLite3Engine(in_memory=True)
            self.addCleanup(self.cleanupEngine)
        return self._engine

    def cleanupEngine(self):
        if self._engine is not None:
            self._engine = None

    def assertTableExist(self, table_name):
        query = 'SELECT name from sqlite_master where type=? and name=?'
        params = ('table', table_name)
        cursor = self.engine.cursor()
        cursor.execute(query, params)
        got = cursor.fetchone()
        self.assertIsNotNone(got, f"Table {table_name!r} is missing")

    def assertColumnExist(self, table_name, column_name):
        query = 'SELECT name FROM pragma_table_info(?) WHERE name=?;'
        params = (table_name, column_name)
        cursor = self.engine.cursor()
        cursor.execute(query, params)
        got = cursor.fetchone()
        self.assertIsNotNone(got, f"Column {column_name!r} is missing")

    def assertHasRecordEqual(self, table_name, column_name, value):
        query = f'SELECT * FROM {table_name} WHERE {column_name}=?;'
        params = (value,)
        cursor = self.engine.cursor()
        cursor.execute(query, params)
        got = cursor.fetchone()
        self.assertIsNotNone(got, f"Record with {value!r} is missing")

    def assertNoRecordEqual(self, table_name, column_name, value):
        query = f'SELECT * FROM {table_name} WHERE {column_name}=?;'
        params = (value,)
        cursor = self.engine.cursor()
        cursor.execute(query, params)
        got = cursor.fetchone()
        self.assertIsNone(got, f"Record with {value!r} was found")


class CreateSimpleModelTest(BaseDbTest):

    def setUp(self):
        class Book(Model):
            db_engine = self.engine
            title = StringField()
            rank = IntegerField()

        self.Book = Book

    def test_create_model(self):
        self.engine.ddl.create_model(self.Book)
        self.assertTableExist('book')

    def test_create_column(self):
        self.engine.ddl.create_model(self.Book)
        self.assertColumnExist('book', 'title')
        self.assertColumnExist('book', 'rank')


class ModelSaveTest(BaseDbTest):

    def setUp(self):
        class Book(Model):
            db_engine = self.engine
            title = StringField()
            rank = IntegerField()

        self.Book = Book
        self.engine.ddl.create_model(self.Book)

    def test_save(self):
        book = self.Book()
        book.title = 'Only Title'
        book.rank = 10
        book.save()
        self.assertHasRecordEqual('book', 'title', 'Only Title')
        self.assertHasRecordEqual('book', 'rank', 10)

    def test_save_twice(self):
        book = self.Book()
        book.title = 'Only Title'
        book.rank = 10
        book.save()
        book.title = 'New Title'
        book.save()
        self.assertNoRecordEqual('book', 'title', 'Only Title')
        self.assertHasRecordEqual('book', 'title', 'New Title')
        self.assertHasRecordEqual('book', 'rank', 10)
