DROP TABLE IF EXISTS demo_table;

CREATE TABLE demo_table (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    member_name TEXT NOT NULL,
    transaction_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    company TEXT NOT NULL,
    value FLOAT NOT NULL
);