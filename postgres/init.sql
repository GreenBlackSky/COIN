CREATE TABLE test_data (
    id SERIAL PRIMARY KEY,
    value text
);
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    password_hash VARCHAR(200)
)