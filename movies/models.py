from django.db import models

import uuid
from datetime import datetime

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class Gender(models.TextChoices):
    MALE = 'male', _('мужской')
    FEMALE = 'female', _('женский')


class Genre(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(_('name'), max_length=255)
    description = models.TextField(_('description'), blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Жанр')
        verbose_name_plural = _('Жанры')
        db_table = "genre"
        managed = False

    def __str__(self):
        return f"{self.name}"


class Person(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    full_name = models.CharField(_('имя'), max_length=50)
    birth_date = models.DateTimeField(_('дата рождения'))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Персона')
        verbose_name_plural = _('Персоны')
        db_table = "person"
        managed = False

    def __str__(self):
        return f"{self.full_name}"


class GenreFilmWork(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    film_work = models.ForeignKey('FilmWork', on_delete=models.CASCADE, default=None)
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE, default=None)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "genre_film_work"
        verbose_name = _('Жанр кинопроизведения')
        verbose_name_plural = _('Жанры кинопроизведения')
        managed = False

    def __str__(self):
        return f"{self.film_work_id} - {self.genre_id}"





class PersonFilmWork(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    film_work = models.ForeignKey('FilmWork', on_delete=models.CASCADE, default=None)
    person = models.ForeignKey('Person', on_delete=models.CASCADE, default=None)
    role = models.CharField(_('роль'), max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "person_film_work"
        verbose_name = _('Участник кинопроизведения')
        verbose_name_plural = _('Участники кинопроизведения')
        managed = False

    def __str__(self):
        return f"{self.role}"


class FilmWorkType(models.TextChoices):
    MOVIE = 'movie', _('movie')
    TV_SHOW = 'tv_show', _('TV Show')



class FilmWork(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(_('Название'), max_length=255)
    description = models.TextField(_('Описание'), blank=True, null=True)
    creation_date = models.DateField(_('Дата создания'), blank=True, null=True)
    file_path = models.FileField(_('Путь к файлу'), upload_to='film_works/')
    rating = models.FloatField(
        _('Рейтинг'),
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        blank=True, null=True
    )
    type = models.CharField(_('Тип'), max_length=20, choices=FilmWorkType.choices)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # genres = models.ManyToManyField(Genre, through='GenreFilmWork', verbose_name=_('Жанры'))
    # person = models.ManyToManyField(Person, through='PersonFilmWork', verbose_name=_('Персоны'))
    genres = models.ManyToManyField(Genre, through='GenreFilmWork', verbose_name=_('Жанры'), related_name='filmworks')
    persons = models.ManyToManyField(Person, through='PersonFilmWork', verbose_name=_('Персоны'), related_name='filmworks')

    class Meta:
        verbose_name = _('Кинопроизведение')
        verbose_name_plural = _('Кинопроизведения')
        db_table = "film_work"
        managed = False
