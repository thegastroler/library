from django.contrib import admin
from django.http import HttpResponse

from .models import Author, Book, Genre, Publisher


@admin.action(description='Export data as .csv')
def csv_export(self, request, queryset):
    import codecs
    import csv
    fields = [i.name for i in self.model._meta.fields]
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename={}.csv'.format(
        self.model._meta.object_name)
    response.write(codecs.BOM_UTF8)
    writer = csv.writer(response, dialect='excel', delimiter=';')
    writer.writerow(fields)
    for obj in queryset:
        writer.writerow([getattr(obj, field) for field in fields])
    return response


class GenreAdmin(admin.ModelAdmin):
    list_display = ('title', 'id')
    search_fields = ('title', 'id')
    list_per_page = 20
    actions = [csv_export]


class PublilsherAdmin(admin.ModelAdmin):
    list_display = ('title', 'id')
    search_fields = ('title', 'id')
    list_per_page = 20
    actions = [csv_export]


class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_genre', 'author', 'publisher', 'id')
    search_fields = ('book', 'id')
    filter_horizontal = ('genre',)
    list_filter = ('author', 'publisher', 'genre')
    list_per_page = 20
    actions = [csv_export]

    def get_genre(self, obj):
        return ', '.join([p.title for p in obj.genre.all()])


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'middle_name', 'last_name', 'birth_date', 'id')
    search_fields = ('first_name', 'last_name', 'id')
    list_per_page = 20
    actions = [csv_export]


admin.site.register(Book, BookAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Publisher, PublilsherAdmin)
admin.site.register(Author, AuthorAdmin)
