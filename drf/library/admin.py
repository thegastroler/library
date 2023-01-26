from django.contrib import admin

from .models import Author, Book, Genre, Publisher


class GenreAdmin(admin.ModelAdmin):
    list_display = ('title', )
    search_fields = ('title',)
    list_per_page = 20


class PublilsherAdmin(admin.ModelAdmin):
    list_display = ('title', )
    search_fields = ('title',)
    list_per_page = 20


class BookAdmin(admin.ModelAdmin):
    filter_horizontal = ('genre',)
    search_fields = ('book',)
    list_filter = ('author', 'publisher', 'genre')
    list_display = ('title', 'get_genre', 'author', 'publisher')
    list_per_page = 20

    def get_genre(self, obj):
        return ', '.join([p.title for p in obj.genre.all()])


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'middle_name', 'last_name', 'birth_date')
    search_fields = ('first_name', 'last_name')
    list_per_page = 20


admin.site.register(Book, BookAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Publisher, PublilsherAdmin)
admin.site.register(Author, AuthorAdmin)
