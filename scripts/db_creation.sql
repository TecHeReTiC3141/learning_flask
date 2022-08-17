CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS Classes (
    id    INTEGER    PRIMARY KEY AUTOINCREMENT,
    name  TEXT (25)  UNIQUE,
    descr TEXT (100) UNIQUE
);

CREATE TABLE news (
    id      INTEGER    PRIMARY KEY AUTOINCREMENT,
    title   TEXT (100) UNIQUE
                       NOT NULL,
    content TEXT (600) NOT NULL,
    author  TEXT (50)  NOT NULL
);
