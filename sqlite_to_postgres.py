import sqlite3
import psycopg2
import uuid
import io

import time
import datetime
from datetime import datetime
import datetime
from dataclasses import dataclass, field
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor


# ======= DATA CLASSES ==============

@dataclass
class FilmWork:
    id:            str
    title:         str
    description:   str
    creation_date: str
    certificate:   str
    type:          str
    created_at:    datetime.datetime
    updated_at:    datetime.datetime
    rating: float = field(default=0.0)

@dataclass
class Genre:
    id:            str
    name:          str
    description:   str
    created_at:    datetime.datetime
    updated_at:    datetime.datetime

@dataclass
class Genre_film_work:
    id:            str
    film_work_id:         str
    genre_id:   str
    created_at: datetime.datetime

@dataclass
class Person:
    id:            str
    full_name:         str

    created_at:    datetime.datetime
    updated_at:    datetime.datetime
    birth_date:   datetime.date = field(default=None)

@dataclass
class Person_film_work:
    id:            str
    film_work_id:         str
    person_id:   str
    role:    str
    created_at:    datetime.datetime


class PostgresSaver:
    def __init__(self, pg_conn: _connection):
        self.pg_conn = pg_conn
        self.pg_cursor = pg_conn.cursor()

    def save_all_data(self, data):
        psycopg2.extras.register_uuid()
        film_work_old_and_new_ids = []
        genre_old_and_new_ids = []
        person_old_and_new_ids = []
        # for obj in data['FilmWork']:
        for obj in data['film_work']:
            new_id = uuid.uuid4()
            film_work_old_and_new_ids.append({new_id: str(obj.id)})
            to_insert = (
                new_id, obj.title,  obj.description,
                datetime.datetime.now(), None, "movie", datetime.datetime.now(), datetime.datetime.now(), obj.rating
            )
            self.pg_cursor.execute(
                """INSERT INTO content.film_work (id, title, description, creation_date, certificate, 
                type, created_at, updated_at, rating  )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""", to_insert
            )
        for obj_actors in data['genre']:
            new_id = uuid.uuid4()
            genre_old_and_new_ids.append({new_id: obj_actors.id})

            to_insert = (new_id, obj_actors.name, obj_actors.description, obj_actors.created_at, obj_actors.updated_at)
            self.pg_cursor.execute("""INSERT INTO content.genre (id, name, description, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s)""", to_insert)
        for genre_film_work in data['genre_film_work']:
            film_work_id = None
            genre_id = None
            for film_work_old_and_new_id in film_work_old_and_new_ids:
                if str(genre_film_work.film_work_id) in film_work_old_and_new_id.values():
                    film_work_id = list(film_work_old_and_new_id.keys())[0]
                    print(f'here film_work_id : {film_work_id}')
                    break

            for genre_old_and_new_id in genre_old_and_new_ids:
                if str(genre_film_work.genre_id) in genre_old_and_new_id.values():
                    genre_id = list(genre_old_and_new_id.keys())[0]
                    print(f'here genr.id : {genre_id }')
                    break
            new_id = uuid.uuid4()
            to_insert = (new_id, film_work_id, genre_id, genre_film_work.created_at)
            if film_work_id and genre_id:
                self.pg_cursor.execute("""INSERT INTO content.genre_film_work (id, film_work_id, genre_id, created_at)
                    VALUES (%s, %s, %s, %s)""", to_insert)

        for obj_actors in data['person']:
            new_id = uuid.uuid4()
            person_old_and_new_ids.append({new_id: obj_actors.id})

            to_insert = (new_id, obj_actors.full_name, obj_actors.created_at, obj_actors.updated_at, obj_actors.birth_date)
            self.pg_cursor.execute("""INSERT INTO content.person (id, full_name, created_at, updated_at, birth_date )
                VALUES (%s, %s, %s, %s, %s)""", to_insert)


        for person_film_work in data['person_film_work']:
            film_work_id = None
            person_id = None
            for film_work_old_and_new_id in film_work_old_and_new_ids:
                if str(person_film_work.film_work_id) in film_work_old_and_new_id.values():
                    film_work_id = list(film_work_old_and_new_id.keys())[0]
                    print(f'here film_work_id : {film_work_id}')
                    break

            for person_old_and_new_id in person_old_and_new_ids:
                if str(person_film_work.person_id) in person_old_and_new_id.values():
                    person_id = list(person_old_and_new_id.keys())[0]
                    print(f'here genr.id : {genre_id }')
                    break
            new_id = uuid.uuid4()
            to_insert = (new_id, film_work_id, person_id, person_film_work.role, person_film_work.created_at)
            if film_work_id and person_id:
                self.pg_cursor.execute("""INSERT INTO content.person_film_work (id, film_work_id, person_id, role, created_at)
                    VALUES (%s, %s, %s, %s, %s)""", to_insert)

class SQLiteLoader:
    def __init__(self, connection: sqlite3.Connection):
        self.connection = connection
        self.cursor = connection.cursor()

    def load_movies(self):
        req = "SELECT name FROM sqlite_master WHERE type = 'table' " \
            "EXCEPT SELECT name FROM sqlite_master WHERE name = 'sqlite_sequence'"
        self.cursor.execute(req)
        table_names = self.cursor.fetchall()
        print(f'Table names loaded from SQLite: {table_names}')
        data = {
            'film_work': [],
            'genre': [],
            'genre_film_work': [],
            'person': [],
            'person_film_work': [],
        }
        for table_name in table_names:
            table_name = list(table_name)
            req = "SELECT * FROM %s" % table_name[0]
            self.cursor.execute(req)
            temp = list(self.cursor.fetchall())
            print(f'eto len(temp) : {len(temp)}')
            i = 0
            for obj in temp:
                if table_name[0] == "film_work":
                    if temp[i][5] != "N/A":
                        rating = temp[i][5]
                    else:
                        rating = 0
                    data[table_name[0]].append(
                        FilmWork(
                            id = temp[i][0],
                            title = temp[i][1],
                            description = temp[i][2],
                            creation_date =  temp[i][3],
                            certificate =  temp[i][4],
                            type = temp[i][6],
                            created_at = temp[i][7],
                            updated_at = temp[i][8],
                            rating = rating
                        )
                    )
                elif table_name[0] == "genre":
                    data[table_name[0]].append(Genre(name=temp[i][1],id=temp[i][0], description=temp[i][2], created_at=temp[i][3], updated_at=temp[i][4]))
                elif table_name[0] == "genre_film_work":
                    data[table_name[0]].append(Genre_film_work(film_work_id=temp[i][1],id=temp[i][0], genre_id=temp[i][2], created_at=temp[i][3]))
                elif table_name[0] == "person":
                    data[table_name[0]].append(Person(full_name=temp[i][1], id=temp[i][0],birth_date=None, created_at=temp[i][2], updated_at=temp[i][3]))
                elif table_name[0] == "person_film_work":
                    data[table_name[0]].append(Person_film_work(film_work_id=temp[i][1], id=temp[i][0], person_id=temp[i][2], role=temp[i][3], created_at=temp[i][4]))
                i += 1
        return data


def load_from_sqlite(connection: sqlite3.Connection, pg_conn: _connection):
    postgres_saver = PostgresSaver(pg_conn)
    sqlite_loader = SQLiteLoader(connection)

    data = sqlite_loader.load_movies()
    postgres_saver.save_all_data(data)


if __name__ == '__main__':
    print(datetime.datetime.now())
    dsl = {
        'dbname': 'movies',
        'user': 'postgres',
        'password': 123,
        'host': '127.0.0.1',
        'port': 5432
    }
    with sqlite3.connect('../db/db3.sqlite3') as sqlite_conn, psycopg2.connect(**dsl, cursor_factory=DictCursor) as pg_conn:
        load_from_sqlite(sqlite_conn, pg_conn)