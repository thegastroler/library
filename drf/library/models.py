from django.db import models


class Author(models.Model):
    first_name = models.CharField(verbose_name='Имя', max_length=255, blank=False)
    last_name = models.CharField(verbose_name='Фамилия', max_length=255, blank=False)
    birth_year = models.DateField(verbose_name='Дата рождения', blank=False)

    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name}'

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'
        ordering = ['-id']
        constraints = [
            models.UniqueConstraint(fields=['first_name', 'last_name'], name='unique_tag')
        ]


class Genre(models.Model):
    title = models.CharField(verbose_name='Название', max_length=255, unique=True)

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ['-id']


class Publisher(models.Model):
    title = models.CharField(verbose_name='Название', max_length=255, unique=True)

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = 'Издатель'
        verbose_name_plural = 'Издатели'
        ordering = ['-id']


class Book(models.Model):
    title = models.CharField(verbose_name='Название', max_length=255)
    author = models.ForeignKey(
        Author,
        related_name='books',
        on_delete=models.CASCADE,
        verbose_name='Автор',
        blank=False
        )
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Жанр',
        blank=False)
    publisher = models.ForeignKey(
        Publisher,
        related_name='books',
        on_delete=models.CASCADE,
        verbose_name='Издатель',
        blank=False)

    def __str__(self) -> str:
        return f'{self.title}, {self.author}'

    class Meta:
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'
        ordering = ['-id']


# class BookGenre(models.Model):
#     book = models.ForeignKey(
#         Book,
#         verbose_name='Книга',
#         on_delete=models.CASCADE,
#         related_name='book_genre',
#     )
#     genre = models.ForeignKey(
#         Genre,
#         verbose_name='Жанр',
#         on_delete=models.CASCADE,
#         related_name='book_genre',
#     )

#     def __str__(self):
#         return f'{self.book}: {self.genre}'

#     class Meta:
#         verbose_name = 'Книга и жанр'
#         verbose_name_plural = 'Книги и жанры'