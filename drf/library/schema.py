import graphene
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.types import DjangoObjectType

from .models import Author, Book, Genre, Publisher


class BookType(DjangoObjectType):
    class Meta:
        model = Book


class AuthorType(DjangoObjectType):
    class Meta:
        model = Author


class GenreType(DjangoObjectType):
    class Meta:
        model = Genre


class PublisherType(DjangoObjectType):
    class Meta:
        model = Publisher


class AuthorInput(graphene.InputObjectType):
    first_name = graphene.String()
    middle_name = graphene.String()
    last_name = graphene.String()
    birth_date = graphene.Date()


class GenreInput(graphene.InputObjectType):
    title = graphene.String()


class PublisherInput(graphene.InputObjectType):
    title = graphene.String()


class BookAuthorInput(graphene.InputObjectType):
    id = graphene.ID()


class BookGenreInput(graphene.InputObjectType):
    id = graphene.ID()


class BookPublisherInput(graphene.InputObjectType):
    id = graphene.ID()


class BookInput(graphene.InputObjectType):
    title = graphene.String()
    author = graphene.Argument(BookAuthorInput)
    genre = graphene.List(BookGenreInput)
    publisher = graphene.Argument(BookPublisherInput)









class ExtendedConnection(graphene.Connection):
    class Meta:
        abstract = True

    total_count = graphene.Int()
    edge_count = graphene.Int()

    def resolve_total_count(root, info, **kwargs):
        return root.length
    def resolve_edge_count(root, info, **kwargs):
        return len(root.edges)


class AuthorsType(DjangoObjectType):
    class Meta:
        model = Author
        filter_fields = {
            'id':  ['exact', 'icontains'],
            'first_name': ['exact', 'contains'],
            'last_name': ['exact', 'contains'],
            'birth_date': ['exact'],
        }
        interfaces = (graphene.Node, )
        connection_class = ExtendedConnection









class Query(graphene.ObjectType):
    authors = DjangoFilterConnectionField(AuthorsType)
    search_author = graphene.List(
        AuthorType,
        id=graphene.ID(),
        first_name=graphene.String(),
        last_name=graphene.String())
    all_authors = graphene.List(AuthorType)
    search_book = graphene.List(
        BookType,
        id=graphene.ID(),
        title=graphene.String(),
        author=graphene.Argument(BookAuthorInput),
        genre=graphene.Argument(BookGenreInput),
        publisher=graphene.Argument(BookPublisherInput)
        )
    all_books = graphene.List(BookType)
    search_genre = graphene.List(
        GenreType,
        id=graphene.ID(),
        title=graphene.String())
    all_genres = graphene.List(GenreType)
    search_publisher = graphene.List(
        PublisherType,
        id=graphene.ID(),
        title=graphene.String())
    all_publishers = graphene.List(PublisherType)

    def resolve_all_books(self, info, **kwargs):
        return Book.objects.all()

    def resolve_all_authors(self, info, **kwargs):
        return Author.objects.all()

    def resolve_all_genres(self, info, **kwargs):
        return Genre.objects.all()

    def resolve_all_publishers(self, info, **kwargs):
        return Publisher.objects.all()

    def resolve_search_book(self, info, **kwargs):
        id = kwargs.get('id')
        title = kwargs.get('title')
        author = kwargs.get('author').get('id') if kwargs.get('author') else None
        genre = kwargs.get('genre').get('id') if kwargs.get('genre') else None
        publisher = kwargs.get('publisher').get('id') if kwargs.get('publisher') else None
        query = None
        if id:
            query = Book.objects.filter(pk=id)
        if title:
            if query is not None:
                query = query.filter(title__contains=title)
            else:
                query = Book.objects.filter(title__contains=title)
        if author:
            if query is not None:
                query = query.filter(author__pk=author)
            else:
                query = Book.objects.filter(author__pk=author)
        if genre:
            if query is not None:
                query = query.filter(genre__pk=genre)
            else:
                query = Book.objects.filter(genre__pk=genre)
        if publisher:
            if query is not None:
                query = query.filter(publisher__pk=publisher)
            else:
                query = Book.objects.filter(publisher__pk=publisher)
        return query

    def resolve_search_author(self, info, **kwargs):
        id = kwargs.get('id')
        first_name = kwargs.get('first_name')
        last_name = kwargs.get('last_name')
        query = None
        if id:
            query = Author.objects.filter(pk=id)
        if first_name:
            if query is not None:
                query = query.filter(first_name__contains=first_name)
            else:
                query = Author.objects.filter(first_name__contains=first_name)
        if last_name:
            if query is not None:
                query = query.filter(last_name__contains=last_name)
            else:
                query = Author.objects.filter(last_name__contains=last_name)
        return query

    def resolve_search_genre(self, info, **kwargs):
        id = kwargs.get('id')
        title = kwargs.get('title')
        query = None
        if id:
            query = Genre.objects.filter(pk=id)
        if title:
            if query is not None:
                query = query.filter(title__contains=title)
            else:
                query = Genre.objects.filter(title__contains=title)
        return query

    def resolve_search_publisher(self, info, **kwargs):
        id = kwargs.get('id')
        title = kwargs.get('title')
        query = None
        if id:
            query = Publisher.objects.filter(pk=id)
        if title:
            if query is not None:
                query = query.filter(title__contains=title)
            else:
                query = Publisher.objects.filter(title__contains=title)
        return query


class CreateAuthor(graphene.Mutation):
    class Arguments:
        input = AuthorInput(required=True)

    ok = graphene.Boolean()
    author = graphene.Field(AuthorType)

    @staticmethod
    def mutate(self, info, input=None):
        ok = True
        author_instance = Author(
            first_name=input.first_name,
            last_name=input.last_name,
            birth_date=input.birth_date,
        )
        if input.middle_name is not None:
            author_instance.middle_name = input.middle_name
        author_instance.save()
        return CreateAuthor(ok=ok, author=author_instance)


class CreateGenre(graphene.Mutation):
    class Arguments:
        input = GenreInput(required=True)

    ok = graphene.Boolean()
    genre = graphene.Field(GenreType)

    @staticmethod
    def mutate(self, info, input=None):
        ok = True
        genre_instance = Genre(
            title=input.title
        )
        genre_instance.save()
        return CreateGenre(ok=ok, genre=genre_instance)


class CreatePublisher(graphene.Mutation):
    class Arguments:
        input = PublisherInput(required=True)

    ok = graphene.Boolean()
    publisher = graphene.Field(PublisherType)

    @staticmethod
    def mutate(self, info, input=None):
        ok = True
        publisher_instance = Publisher(
            title=input.title
        )
        publisher_instance.save()
        return CreatePublisher(ok=ok, publisher=publisher_instance)


class CreateBook(graphene.Mutation):
    class Arguments:
        input = BookInput(required=True)
    ok = graphene.Boolean()
    book = graphene.Field(BookType)

    @staticmethod
    def mutate(root, info, input=None):
        ok = True
        author = Author.objects.filter(pk=input.author.id).first()
        publisher = Publisher.objects.filter(pk=input.publisher.id).first()
        if not all((author, publisher)):
            return CreateBook(ok=False, author=None, genre=None,
                              publisher=None)
        genres = []
        for genre_input in input.genre:
            genre = Genre.objects.filter(pk=genre_input.id).first()
            if genre is None:
                return CreateBook(ok=False, author=None, genre=None,
                                  publisher=None)
            genres.append(genre)
        book_instance = Book(
            title=input.title,
            author=author,
            publisher=publisher
        )
        book_instance.save()
        book_instance.genre.set(genres)
        return CreateBook(ok=ok, book=book_instance)


class UpdateAuthor(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        input = AuthorInput(required=True)
    ok = graphene.Boolean()
    author = graphene.Field(AuthorType)

    @staticmethod
    def mutate(root, info, id, input=None):
        author_instance = Author.objects.filter(pk=id).first()
        if not author_instance:
            return UpdateAuthor(ok=False, movie=None)
        author_instance.first_name = input.first_name
        author_instance.middle_name = input.middle_name
        author_instance.last_name = input.last_name
        author_instance.birth_date = input.birth_date
        author_instance.save()
        return UpdateAuthor(ok=True, author=author_instance)


class UpdateGenre(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        input = GenreInput(required=True)
    ok = graphene.Boolean()
    genre = graphene.Field(GenreType)

    @staticmethod
    def mutate(root, info, id, input=None):
        genre_instance = Genre.objects.filter(pk=id).first()
        if not genre_instance:
            return UpdateGenre(ok=False, genre=None)
        genre_instance.title = input.title
        genre_instance.save()
        return UpdateGenre(ok=True, genre=genre_instance)


class UpdatePublisher(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        input = PublisherInput(required=True)
    ok = graphene.Boolean()
    publisher = graphene.Field(PublisherType)

    @staticmethod
    def mutate(root, info, id, input=None):
        publisher_instance = Publisher.objects.filter(pk=id).first()
        if not publisher_instance:
            return UpdatePublisher(ok=False, publisher=None)
        publisher_instance.title = input.title
        publisher_instance.save()
        return UpdatePublisher(ok=True, publisher=publisher_instance)


class UpdateBook(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        input = BookInput(required=True)
    ok = graphene.Boolean()
    book = graphene.Field(BookType)

    @staticmethod
    def mutate(root, info, id, input=None):
        book_instance = Book.objects.filter(pk=id).first()
        if book_instance:
            author = Author.objects.filter(pk=input.author.id).first()
            publisher = Publisher.objects.filter(pk=input.publisher.id).first()
            if not all((author, publisher)):
                return UpdateBook(ok=False, book=None)
            genres = []
            for genre_input in input.genre:
                genre = Genre.objects.filter(pk=genre_input.id).first()
                if genre is None:
                    return UpdateBook(ok=False, book=None)
                genres.append(genre)
            book_instance.title = input.title
            book_instance.author = author
            book_instance.publisher = publisher
            book_instance.save()
            book_instance.genre.set(genres)
            return UpdateBook(ok=True, book=book_instance)
        return UpdateBook(ok=False, book=None)


class Mutation(graphene.ObjectType):
    create_author = CreateAuthor.Field()
    create_genre = CreateGenre.Field()
    create_publisher = CreatePublisher.Field()
    create_book = CreateBook.Field()
    update_author = UpdateAuthor.Field()
    update_genre = UpdateGenre.Field()
    update_publisher = UpdatePublisher.Field()
    update_book = UpdateBook.Field()
