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


# ОТВЕТЫ 
Alex I, [01.06.2022 18:19]
1. Почему в схеме film_scheme нет того что не отмечено плюсом
Данные в Эластике вовсе не обязаны быть копией данных из базы, у него нет задачи хранить полные данные. Туда загружаются только те поля фильма, по которым допускается поиск. Если по содержанию какого-то поля мы не хотим искать, то нет никакого смысла дублировать это поле в Elastic.

Alex I, [01.06.2022 18:21]
2. В genre_scheme к полю name добавлены еще опции
Это значит, что поле name является текстовым, то есть в нем допускается полнотекстовый поиск. Но вместе с тем добавлено поле name.raw типа keyword - оно имеет то же значение, что и name, но другого типа и поиск по его значению работает иначе - не полнотекстовый с расчетом релевантности, а ищет точное совпадение имени с запросом. В общем, чтобы по имени можно было искать и так и так.

Егор, [01.06.2022 18:22]
В вы могли бы порям в фале ответить, в том питоновском?

Егор, [01.06.2022 18:23]
[In reply to Alex I]
ну а можно как то очистить что было раньше и по новой залить?

Alex I, [01.06.2022 18:23]
3 .В схемах для моделей на заданы поля created_at и updated_at
То же что и по пункту 1 - в Эластик не загружаются поля по которым не производится поиск - очевидно поиск по имени файла и дате обновления записи в базе смысла не имеет. Поля рейтинга и другие могут иметь и другое имя, чем в Django - эти структуры данных не связаны между собой, и соответствующие поля не обязаны называться одинаково

Alex I, [01.06.2022 18:23]
Чтобы очистить и загружать поновой - удалите файл state.json. В питоновском файле ответить не могу, на том компе не работает ввод русских букв

Alex I, [01.06.2022 18:26]
4. Для film_scheme есть properties для writers и director
Да, можно в Эластик добавлять и поля, которых нет в базе. Если не заполнять в этих полях данные, то в них ничего не будет найдено, но ошибки не возникнет, и по другим полям все будет искаться нормально. Или можно поля в Эластике заполнить совсем другой информацией - например в поле writers записать всех кто имеет отношение к фильму. Тогда по ним можно будет искать все равно

Егор, [01.06.2022 18:27]
[In reply to Alex I]
удалил, вроде отработало все,

Alex I, [01.06.2022 18:29]
5. Как GenreFilmWork понимает, что нужно смотреть поле film_work
В таблице GenreFilmWork - есть поле film_work типа ForeignKey(to=FilmWork). Соответственно оно и используется как ссылка на фильм, поскольку ничего другого в этом качестве использовать нельзя. Если бы полей типа ForeignKey(to=FilmWork, ...) в таблице GenreFilmWork было несколько, то при задании отношения многие-ко-многим пришлось бы явно указать, какие из ссылочных полей в промежуточной таблице использовать для этого отношения

Alex I, [01.06.2022 18:31]
6. В каких случаях для поля типа text добавляется еще ключ fields и тип keyword
В тех случаях, когда мы хотим предусмотреть возможность делать не только полнотекстовый поиск по этому полю, но и поиск на точное совпадение

Alex I, [01.06.2022 18:34]
7. Этого вопроса не совсем понял. В структуре базы данных ничего такого указывать не нужно, структура данных Elastic не имеет к ней отношения. Просто загружая данные в Elastic нужно указать значения для этих полей загружаемого объекта. А уж как их брать - для Эластика неважно.

Егор, [01.06.2022 18:36]
[In reply to Alex I]
Где в коде берутся данные для этого поля в эластик в составе id role и title . Я предположид что в файле pg_to_es

Егор, [01.06.2022 18:50]
Там еще у меня были вопросы под пп 8,9

Alex I, [01.06.2022 18:54]
А, ну да - видимо вот в методе PGtoES.__sync_film_batch - там видны строки ARRAY_AGG(p.full_name) FILTER (WHERE pfw.role = 'actor') AS actor_names - это выбирает имена актеров из базы. И там же отдельно ARRAY_AGG(DISTINCT jsonb_build_object('id', p.id, 'name', p.full_name)) FILTER(WHERE ...) - это уже извлекает из базы список сериализованных в Json данных об актерах для каждого фильма. Их и можно загружать в поле actors

Alex I, [01.06.2022 19:09]
8. Если я в пропертис хочу указать дату рождения, то какой тип выбрать.
У Эластика есть специальный тип date, но и text или keyword подойдут. Точнее, keyword - это только если искать по точному значению даты, а если хотите дать возможность найти всех родившихся в определенном году, то text или date. Использование типа date позволит например сортировать актеров по дате рождения при выдаче или органичить даты определенным интервалом. Но для поиска, например, по году использование text тоже вполне возможно

Alex I, [01.06.2022 19:12]
9. Как функция отрабатывает if not self.state.get_state(f"index_created_{index}", True)
В get_state передается строка любого формата, имя индекса вовсе не обязательно. Вообщеself.state - это хранилище ключ-значение, которое сохраняется после выхода из скрипта и восстанавливает свои значения после следующего его запуска. Так мы запоминаем, что определенный индекс уже создан. Но ключ для этой информации может быть любым

Егор, [01.06.2022 19:13]
[In reply to Alex I]
А как он потом берет ключ из строки чтобы return сделать? https://disk.yandex.ru/i/ifwZ6yztIRkQMA

Alex I, [01.06.2022 19:17]
Вот та функция которую вы показываете возвращает значение, которое раньше было сохранено методом set_state. Она вызывается в __sync_batch, как раз сохраняя значение для ключа f"index_created_{index}" как True. Так что потом get_state(f"index_created_{index}") вернет True

Егор, [01.06.2022 19:20]
то есть она создате ключ index_created_{index}?

Alex I, [01.06.2022 19:22]
Да

Егор, [01.06.2022 19:29]
перевел Вам деньги, сегодня-завтра начну читать след спринт, я решил что сначала все пройду на коде других участников с минимом своего участия из серии лишь бы работало, но когда все закончу пойду на второй круг и там тоже рассчитываю на Вашу помощь, так как часть уже забуду к этому времени