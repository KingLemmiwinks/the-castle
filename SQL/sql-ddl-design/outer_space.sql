-- from the terminal run:
-- psql < outer_space.sql

DROP DATABASE IF EXISTS outer_space;

CREATE DATABASE outer_space;

\c outer_space

CREATE TABLE planets
(
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  orbital_period_in_years FLOAT NOT NULL,
  orbits_around TEXT NOT NULL,
  moons_id TEXT[]
);

CREATE TABLE moons
(
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  orbits_around TEXT NOT NULL
);

CREATE TABLE galaxy
(
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  planets_id TEXT[] NOT NULL
);

INSERT INTO planets
  (name, orbital_period_in_years, orbits_around, moons_id)
VALUES
  ('Earth', 1.00, 'The Sun', '{"1"}'),
  ('Mars', 1.88, 'The Sun', '{"2", "3"}'),
  ('Venus', 0.62, 'The Sun', '{}');

INSERT INTO moons
  (name, orbits_around)
VALUES
  ('The Moon', 'Earth'),
  ('Phobos', 'Mars'),
  ('Deimos', 'Mars');

INSERT INTO galaxy
  (name, planets_id)
VALUES
  ('Milky Way', '{"1", "2", "3"}');