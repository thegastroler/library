# Generated by Django 4.1.5 on 2023-01-24 17:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0002_book_unique_tag'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='book',
            name='unique_tag',
        ),
        migrations.AddConstraint(
            model_name='author',
            constraint=models.UniqueConstraint(fields=('first_name', 'last_name'), name='unique_tag'),
        ),
    ]