![albus][albus-header]

> **ARCHIVED NOTICE**
> 
> Looks like the underlying problem was understimated here. The main motivation
> was to actually have a really simple data mapper where you would not need to
> care about fields details neither how to compose queries. Everything was
> supposed to be simple method calls with few arguments.
> 
> Even though the interface was not actually defined, and the idea was to define
> it on the go, one challenge was clear right away and not easy to overcome: the
> engines to access underlying databases. Even if that could be accomplished,
> the security breaches and bugs that the project would need to overcome to
> mature are tremendous.

# Albus

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
