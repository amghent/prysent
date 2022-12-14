DROP DATABASE IF EXISTS "prysent-dev";
DROP SCHEMA IF EXISTS "prysent-dev";
DROP ROLE IF EXISTS prysent;

CREATE ROLE prysent PASSWORD 'prysent';
ALTER ROLE prysent WITH LOGIN;
ALTER ROLE prysent WITH CREATEDB;

CREATE DATABASE "prysent-dev";
CREATE SCHEMA "prysent-dev";
