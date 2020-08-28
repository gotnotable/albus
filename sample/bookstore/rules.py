from .models import Author, Book


def create_author(name):
    author = Author()
    author.name = name
    author.save()


def update_author_initials(author_id, initials):
    Author.filter(id=author_id).update(initials=initials)


def delete_author(author_id):
    Author.filter(id=author_id).delete()

    query = Author.new_query()
    query.filter_equals('id', author_id)
    query.filter_is_not_null('category')
    query.filter_greater_than('published', 2015)
    query.add_alternative(or_query)
    query.add_constraint(and_query)
    query.delete()

    query.filter(Author.id, author_id)

    query = Author.new_query()
    query.equals('id', author_id)
    query.delete()

    query = Author.new_query()
    query.filter(Author.id == author_id)
    query.filter(id=author_id)


def destroy_author(author_id):
    author = Author.get(author_id)
    author.destroy()


def create_books(author, titles):
    for current_title in titles:
        book = Book()
        book.title = current_title
        book.author = author
        book.save()


def list_author_books(author):
    query = Book.filter(author=author)
    return query.fetch()


def list_top_10():
    query = Book.all().order('-rank')
    return query.fetch(limit=10)


def list_author_top_10(author):
    query = Book.filter(author=author).order('-rank')
    return query.fetch(limit=10)


def rank_up(book):
    book.rank = book.rank + 1
    book.save()
