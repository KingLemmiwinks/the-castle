-- from the terminal run:
-- psql < music.sql

DROP DATABASE IF EXISTS music;

CREATE DATABASE music;

\c music

CREATE TABLE artists
(
id SERIAL PRIMARY KEY,
name TEXT NOT NULL,
year_formed INTEGER NOT NULL
);

CREATE TABLE songs
(
  id SERIAL PRIMARY KEY,
  title TEXT NOT NULL,
  duration_in_seconds INTEGER NOT NULL
);

CREATE TABLE albums
(
id SERIAL PRIMARY KEY,
title TEXT NOT NULL,
release_year INTEGER NOT NULL,
songs_id INTEGER[] NOT NULL,
artists_id INTEGER NOT NULL,
producers TEXT[] NOT NULL
);

INSERT INTO artists
  (name, year_formed)
VALUES
  ('Between The Buried And Me', 2000);

INSERT INTO songs
  (title, duration_in_seconds)
VALUES
  ('Monochrome', '194'),
  ('The Double Helix of Extinction', '376'),
  ('Revolution in Limbo', '552'),
  ('Fix the Error', '300'),
  ('Never Seen / Future Shock', '701'),
  ('Stare into the Abyss', '233'),
  ('Prehistory', '187'),
  ('Bad Habits', '523'),
  ('The Future is Behind Us', '322'),
  ('Turbulent', '356'),
  ('Sfumato', '69'),
  ('Human is Hell', '907');

INSERT INTO albums
  (title, release_year, songs_id, artists_id, producers)
VALUES
  ('Colors II', 2021, '{"1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"}', '1', '{"Jamie King", "Between The Buried And Me"}');