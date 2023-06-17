CREATE DATABASE prompts_db;

CREATE TABLE prompts (
    id SERIAL PRIMARY KEY,
    prompt_text TEXT NOT NULL
);

CREATE TABLE results (
    id SERIAL PRIMARY KEY,
    prompt_id INTEGER,
    type TEXT NOT NULL,
    result_text TEXT,
    image BYTEA,
    code TEXT,
    FOREIGN KEY (prompt_id) REFERENCES prompts (id)
);
