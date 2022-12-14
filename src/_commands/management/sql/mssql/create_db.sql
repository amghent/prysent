USE master
GO

DROP DATABASE IF EXISTS prysent
GO

CREATE DATABASE prysent
GO

USE prysent
GO

CREATE USER prysent
    FOR LOGIN prysent
GO

CREATE SCHEMA prysent_dev
GO

ALTER USER prysent
    WITH DEFAULT_SCHEMA = prysent_dev
GO

GRANT ALTER, CONTROL, REFERENCES
    ON DATABASE ::prysent TO prysent
GO

GRANT ALTER, CONTROL, CREATE SEQUENCE, DELETE, INSERT, REFERENCES, SELECT, UPDATE
    ON SCHEMA ::prysent_dev TO prysent
GO

USE master
GO