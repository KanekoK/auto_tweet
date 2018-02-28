CREATE TABLE twitter_lists (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    datetime VARCHAR(64),
    twitter_id INTEGER,
    user_id VARCHAR(64),
    user_name VARCHAR(64),
    profile TEXT,
    location VARCHAR(64),
    protected INTEGER,
    status VARCHAR(64)
);

