CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    password_hash VARCHAR(500) NOT NULL
);