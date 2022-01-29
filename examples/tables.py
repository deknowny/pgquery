import pgquery


class Book(pgquery.Table, title="book"):
    id = pgquery.Serial(pk=True)
    content = pgquery.Text()


actor = pgquery.BuildingActor()
result = actor.build(Book)
print(result.sql)

