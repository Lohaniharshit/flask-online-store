-- create_db_and_tables.sql

-- Create a new database
CREATE DATABASE shopping_app123;

-- Connect to the new database
\connect shopping_app;

-- Create the users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    password VARCHAR(200) NOT NULL
);

-- Create the items table
CREATE TABLE items (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    category VARCHAR(50) NOT NULL,
    price FLOAT NOT NULL
);

-- Create the cart table
CREATE TABLE cart (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) NOT NULL,
    item_id INTEGER REFERENCES items(id) NOT NULL,
    quantity INTEGER DEFAULT 1
);
