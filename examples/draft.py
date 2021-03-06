import typing

import pgquery


class Some(pgquery.Table, name="some"):
    id = pgquery.Serial(pk=True)
    field = pgquery.Text()


class Book(pgquery.Table, name="book"):
    id = pgquery.Serial(pk=True)
    title = pgquery.Varchar(100)
    text = pgquery.Text()
    released_at = pgquery.DateTime()
    author_id = pgquery.Integer(references="author.id")
    some_id = pgquery.Integer(references="some.id")


class Author(pgquery.Table, name="author"):
    id = pgquery.Serial(pk=True)
    full_name = pgquery.Varchar(100)
    bio = pgquery.Text()


# SELECT book.id, book.name FROM book
query1 = Book.select(Book.id, Book.title)

# SELECT b.id, b.name FROM book
query2 = (b := Book).select(b.id, b.title)

# SELECT b.id, b.name, a.full_name
# FROM book b
# JOIN author a
# ON b.author_id == a.id
# WHERE b.id == 100
query3 =\
    (b := Book)\
    .join(a := Author)\
    .on(b.author_id == a.id)\
    .select(b.id, b.name, a.full_name)\
    .where(b.id == 100)


query4 = (a := Author.alias(a=a)).select({
    "full_name": Author.full_name,
    "bio": Author.bio,
    "books": Book.select({
        "id": Book.id,
        "title": Book.title
    }).where(Book.author_id == Author.id)
})

query5 = Author.select(
    full_name=Author.full_name,
    bio=Author.bio,
    books=(
        Book
        .join(Author, Book.id == Author.id)
        .join(Some, Book.some_id == Some.id)
    ).select(
        id=Book.id,
        title=Book.title,
        meta=dict(
            author_name=Author.name,
            some_field=Some.field
        )
    ).where(Book.author_id == Author.id)
)


query7 = (
    Author
    .join(Book, Book.author_id == Author.id)
    .select(
        Author.full_name,
        Author.bio,
        books=Book.select(
            Book.id,
            Book.title
        ).where(Book.author_id == Author.id)
    )
)

query6 = Author.update(
    bio="Some new bio"
).where(Author.id == 100).returning(
    id=Author.id,
    full_name=Author.full_name,
    bio=Author.bio
)


queries = pgquery.QueryRegister()

T = typing.TypeVar("T")


def foo(some: T) -> T:
    return some


arg = foo({"a": "1", "b": 1})


@queries.add
def get_book_by_id(id: pgquery.IntegerType):
    entity = Book.join(Author)
    return pgquery.entity(
        b := Book,
        b.join(a := Author),

    )
    # return pgquery.Select[b := Book](
    #     id=b.id,
    #     released_at=b.released_at,
    #     author=b.join(a := Author, on=b.author_id == a.id)(
    #         id=a.id, bio=a.bio
    #     )
    # )
    # return pgquery.select[b := Book]({
    #     "id": b.id,
    #     "released_at": b.released_at,
    #     "author": pgquery.select[a := Author] {
    #
    #     }
    # })
    # return pgquery\
    #     .select(Book.id, Book.released_at)\
    #     .from_(Book)\
    #     .where(Book.id == id)


# After auto-gen
import datetime

import pydantic


class GetBookByIdResponse(pydantic.BaseModel):
    id: int
    released_at: datetime.datetime


def get_book_by_id(driver: pgquery.Driver, id: pgquery.IntegerType) -> GetBookByIdResponse:
    return driver.execute('SELECT "book"."id","book"."name" FROM "book" where "book"."id" = ?', id)
