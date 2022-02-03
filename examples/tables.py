import time

import pgquery
import sqlparse


class Person(pgquery.Table):
    id = pgquery.Serial(pk=True)
    name = pgquery.Varchar(90)


class Article(pgquery.Table, title="article"):
    id = pgquery.Serial(pk=True)
    content = pgquery.Text(default=pgquery.Literal.new("Not filled yet"))
    author_id = pgquery.Integer(
        references=pgquery.References(Person, Person.id)
    )


foo = Article.id
actor = pgquery.BuildingActor()
start_time = time.time()
query = (
    Article["a"]
    .join_on(Person["p"], Article["a"].author_id == Person["p"].id)
    .join_on(Person["p1"], Article["a"].author_id == Person["p"].id)
    .select(Article["a"].id, Article["a"].content)
    .where(
        pgquery.Or(
            pgquery.Func("sqrt", Article["a"].id) == pgquery.Literal.new(123),
            Article["a"].author_id == pgquery.Literal.new(456),
            pgquery.And(
                pgquery.Literal.new(100) == pgquery.Literal.new(200),
                pgquery.Literal.new(300) == pgquery.Literal.new(400)
            )
        )
    )
)

# query = Person.select({
#     "id": Person.id,
#     "info": {
#         "name": Person.name,
#         "articles": Article.select({
#             "id": Article.id,
#             "content": Article.content
#         }).where(Article.author_id == Person.id)
#     }
#
# })

result_sql = actor.build(query).sql
end_time = time.time()
print(
    pgquery.colorize_sql(
        sqlparse.format(
            actor.build(query).sql,
            reindent=True,
            keyword_case="upper",
            use_space_around_operators=True,
            # indent_width=6
        )
    ),
    "Taken:", end_time - start_time
)

