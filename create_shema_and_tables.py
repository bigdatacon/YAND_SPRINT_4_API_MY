
--создание таблицы film_work
#Для POSTGRES
drop table content.film_work CASCADE;
CREATE TABLE IF NOT EXISTS content.film_work (
    id     uuid PRIMARY KEY,
    title         TEXT,
    description   TEXT,
    creation_date DATE,
    certificate   TEXT,
    rating        FLOAT,
    type          VARCHAR(20),
    created_at    TIMESTAMP WITH TIME ZONE,
    updated_at    TIMESTAMP WITH TIME ZONE
);

--cоздание таблицы content.genre
drop table content.genre;
CREATE TABLE content.genre (
    id          uuid PRIMARY KEY,
    name        TEXT,
    description TEXT,
    created_at  TIMESTAMP WITH TIME ZONE,
    updated_at  TIMESTAMP WITH TIME ZONE
);

--cоздание таблицы content.genre_film_work
drop table content.genre_film_work;
CREATE TABLE content.genre_film_work (
    id           uuid PRIMARY KEY,
    film_work_id uuid,
    genre_id     uuid,
    created_at   TIMESTAMP WITH TIME ZONE,
    CONSTRAINT fk_film_work_id FOREIGN KEY(film_work_id) REFERENCES content.film_work(id),
    CONSTRAINT fk_genre_id FOREIGN KEY(genre_id) REFERENCES content.genre(id)
);

--cоздание таблицы content.person
drop table content.person;
CREATE TABLE content.person (
    id         uuid PRIMARY KEY,
    full_name  VARCHAR(50),
    birth_date DATE,
    created_at TIMESTAMP WITH TIME ZONE,
    updated_at TIMESTAMP WITH TIME ZONE
);

--cоздание таблицы content.person_film_work
drop table content.person_film_work CASCADE;
CREATE TABLE content.person_film_work (
    id           uuid PRIMARY KEY,
    film_work_id uuid,
    person_id    uuid,
    role         TEXT,
    created_at   TIMESTAMP WITH TIME ZONE,
    CONSTRAINT fk_person_film_work_id FOREIGN KEY(film_work_id) REFERENCES content.film_work(id),
    CONSTRAINT fk_person_id FOREIGN KEY(person_id) REFERENCES content.person(id)
);







#Старое
###########################################
###########################################
--1.Попасть в plsql shell
psql -U postgres

#создание базы данных
create database movies;

#Переход в базу данных
\c movies


- 2.===== Создание схемы content ====

CREATE SCHEMA content;

-- 3.===== Создание таблицы actors в схеме content =====

drop table content.actors CASCADE;
CREATE TABLE IF NOT EXISTS content.actors (
    id uuid PRIMARY KEY,
    name TEXT
);


-- 4.===== Создание таблицы genres в схеме content(а так-же вспомогательных таблиц) =====
drop table content.genres CASCADE;
CREATE TABLE IF NOT EXISTS content.genres (
    id uuid PRIMARY KEY,
    genre TEXT
);


-- 5.===== Создание таблицы directors в схеме content(а так-же вспомогательных таблиц) =====
drop table content.directors CASCADE;
CREATE TABLE IF NOT EXISTS content.directors (
    id uuid PRIMARY KEY,
    directror TEXT
);

-- 6.===== Создание таблицы writers в схеме content(а так-же вспомогательных таблиц) =====
drop table content.writers CASCADE;
CREATE TABLE IF NOT EXISTS content.writers (
    id uuid PRIMARY KEY,
    name TEXT
);

-- 7.===== Создание таблицы rating_agency в схеме content =====
drop table content.rating_agency CASCADE;
CREATE TABLE IF NOT EXISTS content.rating_agency (
    id uuid PRIMARY KEY,
    name TEXT
);

-- 8.===== Создание таблицы movies в схеме content(а так-же вспомогательных таблиц) =====
drop table content.movies CASCADE;
CREATE TABLE IF NOT EXISTS content.movies (
    id uuid PRIMARY KEY,
    genre_id uuid,
    director_id uuid,
    writer_id uuid,
    title TEXT,
    plot TEXT,
    ratings TEXT,
    imdb_rating TEXT,
    CONSTRAINT fk_genres FOREIGN KEY(genre_id) REFERENCES content.genres(id),
    CONSTRAINT fk_directors FOREIGN KEY(director_id) REFERENCES content.directors(id),
    CONSTRAINT fk_writers FOREIGN KEY(writer_id) REFERENCES content.writers(id)
);

-- 9.====== Создание таблицы movies_actors в схеме content =====
drop table content.movies_actors CASCADE;
CREATE TABLE IF NOT EXISTS content.movies_actors (
    movies_id uuid REFERENCES content.movies(id),
    actor_id uuid REFERENCES content.actors(id),
    CONSTRAINT movies_actors_pkey PRIMARY KEY (movies_id, actor_id)
);

-- 10.====== Создание таблицы movies_writers в схеме content =====
drop table content.movies_writers CASCADE;
CREATE TABLE IF NOT EXISTS content.movies_writers (
    movies_id uuid REFERENCES content.movies(id),
    writers_id uuid REFERENCES content.actors(id),
    CONSTRAINT movies_writers_pkey PRIMARY KEY (movies_id, writers_id)
);
