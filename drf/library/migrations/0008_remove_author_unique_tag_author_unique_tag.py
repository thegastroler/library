# Generated by Django 4.1.5 on 2023-01-25 19:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0007_alter_author_middle_name'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='author',
            name='unique_tag',
        ),
        migrations.AddConstraint(
            model_name='author',
            constraint=models.UniqueConstraint(fields=('first_name', 'last_name', 'middle_name'), name='unique_tag'),
        ),
    ]
