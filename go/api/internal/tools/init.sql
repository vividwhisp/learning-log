CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY,
    auth_token TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS coins (
    username TEXT PRIMARY KEY,
    balance BIGINT NOT NULL DEFAULT 0
);

INSERT INTO users (username, auth_token) VALUES
    ('raj', '123QWE'),
    ('alex', '123ABC'),
    ('neel', '123RTY'),
    ('shiva','123SHI')
ON CONFLICT (username) DO NOTHING;

INSERT INTO coins (username, balance) VALUES
    ('raj', 100),
    ('alex', 200),
    ('neel', 300),
    ('shiva', 400)
ON CONFLICT (username) DO NOTHING;
