# Generated by Django 4.2.5 on 2024-02-26 19:55

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0003_alter_genrefilmwork_unique_together_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filmwork',
            name='creation_date',
            field=models.DateField(blank=True, null=True, verbose_name='creation_date'),
        ),
        migrations.AlterField(
            model_name='filmwork',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='description'),
        ),
        migrations.AlterField(
            model_name='filmwork',
            name='file_path',
            field=models.TextField(blank=True, null=True, verbose_name='file_path'),
        ),
        migrations.AlterField(
            model_name='filmwork',
            name='genres',
            field=models.ManyToManyField(null=True, through='movies.GenreFilmwork', to='movies.genre'),
        ),
        migrations.AlterField(
            model_name='filmwork',
            name='persons',
            field=models.ManyToManyField(null=True, through='movies.PersonFilmwork', to='movies.person'),
        ),
        migrations.AlterField(
            model_name='filmwork',
            name='rating',
            field=models.FloatField(blank=True, default=0.0, null=True, validators=[django.core.validators.MinValueValidator(
                0.0), django.core.validators.MaxValueValidator(10)], verbose_name='rating'),
        ),
        migrations.AlterField(
            model_name='genre',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='description'),
        ),
        migrations.AlterField(
            model_name='personfilmwork',
            name='role',
            field=models.CharField(choices=[('director', 'Director'), ('writer', 'Writer'),
                                   ('actor', 'Actor')], max_length=20, verbose_name='role'),
        ),
    ]
