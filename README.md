![albus][albus-header]

This Python data mapper library was created thinking on simplicity learning
and using it. As opposed to other ORM options, this one will not be as powerful
and flexible in terms of queries. That is the trade-off to make it simpler to
learn and use.

# Usage

Defining models is done using property descriptors as you would for SQLAlchemy
and Django. Querying them is completely different in regards to how we avoid
overriding Python operators or using dynamic keyword arguments.

```python
from albus.model import Model
from albus import field


class Book(Model):

    author = field.StringField()
    title = field.StringField()
    year = field.IntegerField()


query = Book.new_query()
query.filter_equals('author', 'John Doe')
query.filter_greater('year', 2000)

results = query.select()
for current in results:
    print('Found:', current.title)
```


[albus-header]: https://raw.githubusercontent.com/gotnotable/albus/master/docs/albus-top.png "Albus Header"
