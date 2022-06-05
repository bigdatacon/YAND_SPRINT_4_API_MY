import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator
from django.conf import settings


class TimeStampedMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Genre(TimeStampedMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)+
    name = models.CharField(_('title'), max_length=255)  +
    description = models.TextField(_('description'), blank=True) +

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('genre')
        verbose_name_plural = _('genres')
        db_table = f'{settings.DB_SCHEMA}"."genre'
        indexes = [
            models.Index(fields=['name']),
        ]


class FilmworkGenre(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    film_work = models.ForeignKey('Filmwork', on_delete=models.CASCADE)
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = f'{settings.DB_SCHEMA}"."genre_film_work'
        unique_together = [['film_work', 'genre']]


class Person(TimeStampedMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) +
    full_name = models.CharField(_('full name'), max_length=255) + 
    birth_date = models.DateField(_('birth date'), blank=True) + 

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = _('person')
        verbose_name_plural = _('persons')
        db_table = f'{settings.DB_SCHEMA}"."person'


class PersonRole(models.TextChoices):
    ACTOR = 'actor', _('Actor')
    DIRECTOR = 'director', _('Director')
    WRITER = 'writer', _('Writer')


class FilmworkPerson(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    film_work = models.ForeignKey('Filmwork', on_delete=models.CASCADE)
    person = models.ForeignKey('Person', on_delete=models.CASCADE)
    role = models.CharField(_('role'), max_length=255, choices=PersonRole.choices)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = f'{settings.DB_SCHEMA}"."person_film_work'
        unique_together = [['film_work', 'person', 'role']]


class FilmworkType(models.TextChoices):
    MOVIE = 'movie', _('movie')
    TV_SHOW = 'tv_show', _('TV Show')


class Filmwork(TimeStampedMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(_('title'), max_length=255)
    description = models.TextField(_('description'), blank=True)
    creation_date = models.DateField(_('creation date'), blank=True)
    certificate = models.TextField(_('certificate'), blank=True)
    file_path = models.FileField(_('file'), upload_to='film_works/', blank=True)
    rating = models.FloatField(_('rating'), validators=[MinValueValidator(0), MaxValueValidator(10)], blank=True)
    type = models.CharField(_('type'), max_length=20, choices=FilmworkType.choices)
    genres = models.ManyToManyField(Genre, through='FilmworkGenre')
    persons = models.ManyToManyField(Person, through='FilmworkPerson')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('filmwork')
        verbose_name_plural = _('filmworks')
        db_table = f'{settings.DB_SCHEMA}"."film_work'


class Filmwork(TimeStampedMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(_('title'), max_length=255)     +
    description = models.TextField(_('description'), blank=True)        +
    creation_date = models.DateField(_('creation date'), blank=True)
    certificate = models.TextField(_('certificate'), blank=True)
    file_path = models.FileField(_('file'), upload_to='film_works/', blank=True)
    rating = models.FloatField(_('rating'), validators=[MinValueValidator(0), MaxValueValidator(10)], blank=True)
    type = models.CharField(_('type'), max_length=20, choices=FilmworkType.choices)
    genres = models.ManyToManyField(Genre, through='FilmworkGenre')   +
    persons = models.ManyToManyField(Person, through='FilmworkPerson') +

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('filmwork')
        verbose_name_plural = _('filmworks')
        db_table = f'{settings.DB_SCHEMA}"."film_work'


1. Почему в схеме film_scheme нет того что не отмечено плюсом, а то что отмечено + в частности persons - Это я отметил так как там есть director, actor, writer?
2. в genre_scheme в отличии от базовой схемы ( с которой почти все остальные поля совпадают ) к полю name" добавлены еще опции(ниже) - что они означают?   И что будет если это не добавлять?   
Я так понимаю что то важное содержится в поле "fields":                 
  "fields": {
                        "raw": {
                            "type": "keyword"
                        }
                    }
3. В схемах для  моделей не заданы поля created_at и updated_at хотя они есть в моделях?  Также поле rating называется imdb_rating, и нет поля file_path и type? 
4. Для film_scheme есть properties для writers и director, я так понимаю это потому что у дргого участника есть модель PersonRole в которой эти роли определяются, но 
в моем проекте такого класса нет и мне можно оставить только persons?, но эластик нормально отработал - получается можно и лишните пропертис писать - не страшно? 
5. В модели FilmWork(models.Model) есть трока 
genres = models.ManyToManyField(Genre, through='GenreFilmWork', verbose_name=_('Жанры'), related_name='filmworks')
Вопрос, как модель GenreFilmWork понимает что нужно смотреть моле film_work?
6. В каких случаях вообще для поля типа текст (на примере поля name ) добавляется еще ключ fields и там тип keyword
                "name": {
                    "type": "text",
                    "analyzer": "ru_en",
                    "fields": {
                        "raw": {
                            "type": "keyword"
                        }
                    }

7. В person_scheme Для поля films такие properties. Где мне в моделях или в коде увидеть что действительно тут нужны допонительно id, role, title?
первое что приходит на ум вот эта строчка из pg_to_es ARRAY_AGG(DISTINCT jsonb_build_object('id', fw.id, 'role', pfw.role, 'title', fw.title)) AS films?

                "films": {
                    "type": "nested",
                    "dynamic": "strict",
                    "properties": {
                        "id": {
                            "type": "keyword"
                        },
                        "role": {
                            "type": "text"
                        },
                        "title": {
                            "type": "text",
                            "analyzer": "ru_en"
                        }
8. Если я в пропертис захочу указать дату рождения то какой тип поля нужно выбрать?  Потом уже увидел когда вопрос написал что у другого участника тип text но в модели ведь date?
9. Тут не совсем понял как фунция отрабатывает if not self.state.get_state(f'index_created_{index}'):
Ведь в get_state должен быть передан index а тут целая строка передается
Тоже саме В self.state.set_state(f'index_created_{index}', True)
