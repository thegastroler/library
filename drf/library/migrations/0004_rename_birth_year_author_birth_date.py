# Generated by Django 4.1.5 on 2023-01-25 18:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0003_remove_book_unique_tag_author_unique_tag'),
    ]

    operations = [
        migrations.RenameField(
            model_name='author',
            old_name='birth_year',
            new_name='birth_date',
        ),
    ]
