from library.schema import Query as book_query
from graphene import Schema, ObjectType

class Query(book_query, ObjectType):
    pass

schema = Schema(query=Query)