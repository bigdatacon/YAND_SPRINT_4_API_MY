from django.db import models

import uuid
from datetime import datetime

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class Gender(models.TextChoices):
    MALE = 'male', _('мужской')
    FEMALE = 'female', _('женский')


class TimeStampedMixin(models.Model):
    # В созданных вами таблицах есть поля created_at и updated_at.
    # Чтобы не повторять эти две строки в каждой модели
    # создадим класс-миксин.
    ids = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Genre(TimeStampedMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(_('name'), max_length=255)
    # blank=True делает поле необязательным для заполнения.
    description = models.TextField(_('description'), blank=True)

    class Meta:
        verbose_name = _('Жанр')
        verbose_name_plural = _('Жанры')
        # Ваши таблицы находятся в нестандартной схеме. Это тоже нужно указать в классе модели
        db_table = "genre"

    def __str__(self):
        return f"{self.name}"


class Person(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    full_name = models.CharField(_('имя'), max_length=50)
    birth_date = models.DateTimeField(_('дата рождения'))

    class Meta:
        verbose_name = _('Персона')
        verbose_name_plural = _('Персоны')
        db_table = "person"

    def __str__(self):
        return f"{self.full_name}"


class GenreFilmWork(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    film_work_id = models.ForeignKey('FilmWork', on_delete=models.CASCADE, default=None)
    genre_id = models.ForeignKey('Genre', on_delete=models.CASCADE, default=None)
    created_at = models.DateTimeField(default=datetime.now(), blank=True, verbose_name=_('Дата обращения'))

    class Meta:
        db_table = "genre_film_work"
        verbose_name = _('Жанр кинопроизведения')
        verbose_name_plural = _('Жанры кинопроизведения')

    def __str__(self):
        return f"{self.film_work_id} - {self.genre_id}"


class PersonFilmWork(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    film_work_id = models.ForeignKey('FilmWork', on_delete=models.CASCADE, default=None)
    person_id = models.ForeignKey('Person', on_delete=models.CASCADE, default=None)
    role = models.CharField(_('роль'), max_length=50)
    created_at = models.DateTimeField(default=datetime.now(), blank=True, verbose_name=_('Дата обращения'))

    class Meta:
        db_table = "person_film_work"
        verbose_name = _('Участник кинопроизведения')
        verbose_name_plural = _('Участники кинопроизведения')

    def __str__(self):
        return f"{self.role}"


class FilmWorkType(models.TextChoices):
    MOVIE = 'movie', _('movie')
    TV_SHOW = 'tv_show', _('TV Show')


class FilmWork(TimeStampedMixin, models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(_('Название'), max_length=255)
    description = models.TextField(_('Описание'), blank=True)
    creation_date = models.DateField(_('Дата создания'), blank=True)
    certificate = models.TextField(_('Сертификат'), blank=True)
    # file_path = models.FileField(_('Путь к файлу'), upload_to='film_works/')
    rating = models.FloatField(_('Рейтинг'), validators=[MinValueValidator(0),
                                                         MaxValueValidator(10)], blank=True)
    type = models.CharField(_('Тип'), max_length=20, choices=FilmWorkType.choices)
    # genres = models.ManyToManyField(Genre, through='GenreFilmWork', verbose_name=_('Жанры'))
    # person = models.ManyToManyField(Person, through='PersonFilmWork', verbose_name=_('Персоны'))

    class Meta:
        verbose_name = _('Кинопроизведение')
        verbose_name_plural = _('Кинопроизведения')
        db_table = "film_work"
