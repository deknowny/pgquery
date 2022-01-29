import pgquery


class Person(pgquery.Table):
    id = pgquery.Serial(pk=True)
    name = pgquery.Varchar(90)


class Article(pgquery.Table, title="article"):
    id = pgquery.Serial(pk=True)
    content = pgquery.Text(default=pgquery.literal("Not filled yet"))
    author_id = pgquery.Integer(references="person.id")


actor = pgquery.BuildingActor()
query = Person.select({
    "id": Person.id,
    "info": {
        "name": Person.name,
        "articles": Article.select({
            "id": Article.id,
            "content": Article.content
        }).where(Article.author_id == Person.id)
    }

})

print(actor.build(query).sql)

