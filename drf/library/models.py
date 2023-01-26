from django.db import models


class Author(models.Model):
    first_name = models.CharField(verbose_name='Имя', max_length=255,
                                  blank=False)
    middle_name = models.CharField(verbose_name='Отчество', max_length=255,
                                   blank=True)
    last_name = models.CharField(verbose_name='Фамилия', max_length=255,
                                 blank=False)
    birth_date = models.DateField(verbose_name='Дата рождения', blank=False)

    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name}'

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'
        ordering = ['-id']
        constraints = [
            models.UniqueConstraint(
                fields=['first_name', 'last_name', 'middle_name'],
                name='unique_tag')
        ]


class Genre(models.Model):
    title = models.CharField(verbose_name='Название', max_length=255,
                             unique=True)

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ['-id']


class Publisher(models.Model):
    title = models.CharField(verbose_name='Название', max_length=255,
                             unique=True)

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
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author', 'publisher'],
                name='unique_tag')
        ]
