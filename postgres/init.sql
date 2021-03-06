CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(200) NOT NULL,
    password_hash VARCHAR(500) NOT NULL
);
CREATE TABLE accounts (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users,
    name VARCHAR(100) NOT NULL,
    is_main BOOLEAN NOT NULL DEFAULT false
);
CREATE UNIQUE INDEX only_one_main_account 
   ON accounts (user_id)
   WHERE is_main;

CREATE TABLE dates (
    id SERIAL PRIMARY KEY,
    account_id INT REFERENCES accounts,
    is_actual BOOLEAN NOT NULL DEFAULT false,
    date DATE NOT NULL,
    balance INT NOT NULL,
    unconfirmed_balance INT
);
CREATE UNIQUE INDEX only_one_current_balance 
   ON dates (account_id)
   WHERE is_actual;

CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    account_id INT REFERENCES accounts,
    name VARCHAR(100) NOT NULL,
    description VARCHAR(200),
    color VARCHAR(6),
    hidden BOOLEAN
);
CREATE TABLE events (
    id SERIAL PRIMARY KEY,
    date_id INT REFERENCES dates,
    account_id INT REFERENCES accounts,
    time TIME NOT NULL,
    diff INT NOT NULL,
    category_id INT REFERENCES categories,
    description VARCHAR(200) NOT NULL,
    confirmed BOOLEAN NOT NULL
);
CREATE TABLE templates (
    id SERIAL PRIMARY KEY,
    active BOOLEAN NOT NULL,
    account_id INT REFERENCES accounts,
    time TIME NOT NULL,
    diff INT NOT NULL,
    category_id INT REFERENCES categories,
    description VARCHAR(200) NOT NULL,
    last_confirmed_date INT REFERENCES dates,
    template INT NOT NULL,
    cycle_length INT NOT NULL
);
