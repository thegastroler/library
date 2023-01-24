import graphene
from graphene_django import DjangoObjectType
from graphene_django.types import DjangoObjectType


from .models import Author, Book, Genre, Publisher


class PublisherType(DjangoObjectType):
    class Meta:
        model = Publisher


class GenreType(DjangoObjectType):
    class Meta:
        model = Genre


class AuthorType(DjangoObjectType):
    class Meta:
        model = Author


class BookType(DjangoObjectType):
    class Meta:
        model = Book


class Query(graphene.ObjectType):
    # book = graphene.List(BookType, title=graphene.String())
    # books = graphene.List(BookType)
    author = graphene.List(
        AuthorType,
        id=graphene.ID(),
        first_name=graphene.String(),
        last_name=graphene.String())
    authors = graphene.List(AuthorType)

    # def resolve_book(self, info, **kwargs):
    #     name = kwargs.get('name')
    #     if name is not None:
    #         return Book.objects.filter(name=name)

    # def resolve_books(self, info, **kwargs):
    #     return Book.objects.all()

    def resolve_author(self, info, **kwargs):
        authors = None
        id = kwargs.get('id')
        first_name = kwargs.get('first_name')
        last_name = kwargs.get('last_name')
        if id:
            authors = Author.objects.filter(pk=id)
        elif first_name:
            if authors:
                authors = authors.filter(first_name__contains=first_name)
            else:
                authors = Author.objects.filter(first_name__contains=first_name)
        elif last_name:
            if authors:
                authors = authors.filter(last_name__contains=last_name)
            else:
                authors = Author.objects.filter(last_name__contains=last_name)
        return authors

    def resolve_authors(self, info, **kwargs):
        return Author.objects.all()



class AuthorInput(graphene.InputObjectType):
    first_name = graphene.String()
    last_name = graphene.String()
    birth_date = graphene.Date()


# class GenreInput(graphene.InputObjectType):
#     title = graphene.String()


# class PublisherInput(graphene.InputObjectType):
#     title = graphene.String()


# class BookInput(graphene.InputObjectType):
#     title = graphene.String()
#     author = graphene.String(AuthorInput)
#     genre = graphene.String(GenreInput)
#     publisher = graphene.String(PublisherInput)


# class CreateAuthor(graphene.Mutation):
#     class Arguments:
#         input = AuthorInput(required=True)

#     ok = graphene.Boolean()
#     author = graphene.Field(AuthorType)

#     @staticmethod
#     def mutate(root, info, input=None):
#         ok = True
#         author_instance = Author(
#             first_name=input.first_name,
#             last_name=input.last_name,
#             birth_date=input.birth_date)
#         author_instance.save()
#         return CreateAuthor(ok=ok, author=author_instance)


# class UpdateAuthor(graphene.Mutation):
#     class Arguments:
#         id = graphene.Int(required=True)
#         input = AuthorInput(required=True)

#     ok = graphene.Boolean()
#     author = graphene.Field(AuthorType)

#     @staticmethod
#     def mutate(root, info, id, input=None):
#         ok = False
#         author_instance = Author.objects.get(pk=id)
#         if author_instance:
#             ok = True
#             author_instance.name = input.name
#             author_instance.save()
#             return UpdateAuthor(ok=ok, author=author_instance)
#         return UpdateAuthor(ok=ok, author=None)
