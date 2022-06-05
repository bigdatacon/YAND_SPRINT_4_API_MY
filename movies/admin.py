from django.contrib import admin

from django.contrib import admin
from .models import FilmWork, PersonFilmWork, Genre, Person, GenreFilmWork


class PersonFilmWorkInline(admin.TabularInline):
    model = PersonFilmWork
    extra = 1


class GenreFilmWorkInline(admin.TabularInline):
    model = GenreFilmWork
    extra = 1


@admin.register(FilmWork)
class FilmworkAdmin(admin.ModelAdmin):
    # отображение полей в списке
    list_display = ('title', 'type', 'creation_date', 'rating',)
    # порядок следования полей в форме создания/редактирования

    # фильтрация в списке
    list_filter = ('type', 'rating')

    # поиск по полям
    search_fields = ('title', 'type')

    fields = (
        'title',
        'type',
        'description',
        'creation_date',
        #'certificate',
         'rating',
    )

    inlines = [
        PersonFilmWorkInline, GenreFilmWorkInline
    ]


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    pass


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    search_fields = ('full_name',)
    pass
