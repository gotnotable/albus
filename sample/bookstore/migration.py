from albus import fields


def step_0001(m):
    m.create(
        'Author', [
            ('name', fields.StringField()),
            ('initials', fields.StringField(size=fields.TINY)),
            ('rank', fields.IntegerField()),
            ('birthdate', fields.DateTimeField()),
        ]
    )
    m.create(
        'Book', [
            ('author', fields.IntegerField()),
            ('title', fields.StringField(size=fields.BIG)),
        ]
    )
    m.reference('Book', 'author', 'Author')


def step_0002(m):
    m.add(
        'Book', [
            ('pages', fields.IntegerField()),
        ]
    )
