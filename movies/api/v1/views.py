from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Q
from django.http import JsonResponse
from django.views.generic.list import BaseListView
from django.views.generic.detail import BaseDetailView

from movies.models import FilmWork, Person, PersonFilmWork, GenreFilmWork, Genre

"""Код ниже возвращает результат"""
# filmworks_genres = GenreFilmWork.objects.all().select_related('film_work', 'genre')[:3]
# for filmwork_genre in filmworks_genres:
#     print(filmwork_genre.film_work.title, filmwork_genre.genre.name)

"""ниже класс как выводить даныне с учетом скрипта выше  https://disk.yandex.ru/i/IeDdbFAVAkeUjw"""

class MoviesApiMixin:
    model = FilmWork
    http_method_names = ['get']

    def get_queryset(self):
        qs = GenreFilmWork.objects.select_related('film_work', 'genre'
        ).values(
            'id', 'film_work'
        ).annotate(
            genres=ArrayAgg('genre__name', distinct=True),
            rating=ArrayAgg('film_work__rating', distinct=True)
        )
        return qs

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(context)

    def _aggregate_person(self, role):
        return ArrayAgg('persons__full_name', distinct=True, filter=Q(filmworkperson__role=role))

"""это класс второго участника - он закомментирован"""
# class MoviesApiMixin:
#     model = FilmWork
#     http_method_names = ['get']
#
#     def get_queryset(self):
#         qs = FilmWork.objects.prefetch_related(
#             'genres', 'persons'
#         ).values(
#             'id', 'title', 'description', 'creation_date', 'rating', 'type'
#         ).annotate(
#             genres=ArrayAgg('genres__name', distinct=True),
#             actors=self._aggregate_person(role=PersonRole.ACTOR),
#             directors=self._aggregate_person(role=PersonRole.DIRECTOR),
#             writers=self._aggregate_person(role=PersonRole.WRITER)
#         )
#         return qs
#
#     def render_to_response(self, context, **response_kwargs):
#         return JsonResponse(context)
#
#     def _aggregate_person(self, role):
#         return ArrayAgg('persons__full_name', distinct=True, filter=Q(filmworkperson__role=role))


class MoviesListApi(MoviesApiMixin, BaseListView):

    paginate_by = 50

    def get_context_data(self, *, object_list=None, **kwargs):
        qs = self.get_queryset()
        paginator, page, queryset, is_paginated = self.paginate_queryset(
            qs,
            self.paginate_by
        )
        context = {
            "count": paginator.count,
            "total_pages": paginator.num_pages,
            "prev": page.previous_page_number() if page.has_previous() else None,
            "next": page.next_page_number() if page.has_next() else None,
            'results': list(page),
        }
        return context


class MoviesDetailApi(MoviesApiMixin, BaseDetailView):

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)['object']
