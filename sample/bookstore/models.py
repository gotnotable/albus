from albus import Model
from albus import fields


class Author(Model):

    name = fields.StringField()
    initials = fields.StringField(size=fields.TINY)
    rank = fields.IntegerField()
    birthdate = fields.DateTimeField()


class Book(Model):

    author = fields.ReferenceField('Authors')
    title = fields.StringField(size=fields.BIG)
    pages = fields.IntegerField()
