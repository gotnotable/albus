from unittest import TestCase

from albus.field import IntegerField, StringField
from albus.model import Model


class NoFieldsModelTest(TestCase):

    def setUp(self):
        class FooModel(Model):
            pass

        self.FooModel = FooModel

    def test_new_model(self):
        new = self.FooModel()
        self.assertIsNotNone(new)

    def test_to_json(self):
        new = self.FooModel()
        got = new.to_json()
        expected = {}
        self.assertEqual(got, expected)


class SimpleModelTest(TestCase):

    def setUp(self):
        class Book(Model):
            title = StringField()
            rank = IntegerField()

        self.Book = Book

    def test_new_model(self):
        book = self.Book()
        self.assertIsNotNone(book)

    def test_initial_data(self):
        book = self.Book(title='Foo Bar Book')
        self.assertEqual(book.title, 'Foo Bar Book')

    def test_field_assignment(self):
        book = self.Book()
        book.title = 'New Title'
        self.assertEqual(book.title, 'New Title')

    def test_to_json(self):
        book = self.Book()
        book.title = 'Foo Bar Book'
        book.rank = 10
        got = book.to_json()
        expected = {
            'title': 'Foo Bar Book',
            'rank': 10,
        }
        self.assertEqual(got, expected)


class DefaultFieldValueTest(TestCase):

    def setUp(self):
        class Book(Model):
            title = StringField(default='Untitled Book')

        self.Book = Book

    def test_new_model(self):
        book = self.Book()
        self.assertEqual(book.title, 'Untitled Book')

    def test_override_initial(self):
        book = self.Book(title='New Title')
        self.assertEqual(book.title, 'New Title')

    def test_to_json(self):
        book = self.Book()
        got = book.to_json()
        expected = {
            'title': 'Untitled Book',
        }
        self.assertEqual(got, expected)
