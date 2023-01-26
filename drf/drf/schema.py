import library.schema
from graphene import ObjectType, Schema


class Query(library.schema.Query, ObjectType):
    pass


class Mutation(library.schema.Mutation, ObjectType):
    pass


schema = Schema(query=library.schema.Query, mutation=library.schema.Mutation)
