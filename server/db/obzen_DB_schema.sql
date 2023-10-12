--- obzen_DB_schema.sql

DROP SCHEMA IF EXISTS obzen_test;
CREATE DATABASE obzen_test;
USE obzen_test;

-------------------------------------------
-- Schema
-------------------------------------------
CREATE TABLE chatAnswer (
    id SERIAL PRIMARY KEY,
    text TEXT,
    chatRoom_ID VARCHAR(255),
    session_ID VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE chatQuestion (
    id SERIAL PRIMARY KEY,
    text TEXT,
    chatRoom_ID VARCHAR(255),
    session_ID VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE chatRoom (
    id SERIAL PRIMARY KEY,
    session_ID VARCHAR(255),
    chatRoom_ID VARCHAR(255),
    name VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE session (
    id SERIAL PRIMARY KEY,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expired_at TIMESTAMP DEFAULT NULL,
    session_ID VARCHAR(255) UNIQUE
);
