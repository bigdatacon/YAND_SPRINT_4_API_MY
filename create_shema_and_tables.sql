CREATE DATABASE movies;

\c movies;

CREATE SCHEMA content;

drop table content.film_work CASCADE;
CREATE TABLE content.film_work (
    id            UUID PRIMARY KEY,
    title         TEXT,
    description   TEXT,
    creation_date DATE,
    certificate   TEXT,
    file_path     TEXT,
    rating        FLOAT,
    type          VARCHAR(20),
    created_at    TIMESTAMP WITH TIME ZONE,
    updated_at    TIMESTAMP WITH TIME ZONE
);

drop table content.genre CASCADE;
CREATE TABLE content.genre (
    id          UUID PRIMARY KEY,
    name        TEXT,
    description TEXT,
    created_at  TIMESTAMP WITH TIME ZONE,
    updated_at  TIMESTAMP WITH TIME ZONE
);

drop table content.genre_film_work CASCADE;
CREATE TABLE content.genre_film_work (
    id           UUID PRIMARY KEY,
    film_work_id UUID,
    genre_id     UUID,
    created_at   TIMESTAMP WITH TIME ZONE,

    CONSTRAINT fk_film_work_id FOREIGN KEY(film_work_id) REFERENCES content.film_work(id),
    CONSTRAINT fk_genre_id FOREIGN KEY(genre_id) REFERENCES content.genre(id)
);

drop table content.person CASCADE;
CREATE TABLE content.person (
    id         UUID PRIMARY KEY,
    full_name  VARCHAR(50),
    birth_date DATE,
    created_at TIMESTAMP WITH TIME ZONE,
    updated_at TIMESTAMP WITH TIME ZONE
);


drop table content.person_film_work CASCADE;
CREATE TABLE content.person_film_work (
    id           UUID PRIMARY KEY,
    film_work_id UUID,
    person_id    UUID,
    role         TEXT,
    created_at   TIMESTAMP WITH TIME ZONE,
    CONSTRAINT fk_person_film_work_id FOREIGN KEY(film_work_id) REFERENCES content.film_work(id),
    CONSTRAINT fk_person_id FOREIGN KEY(person_id) REFERENCES content.person(id)
);
