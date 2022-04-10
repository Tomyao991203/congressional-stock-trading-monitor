DROP TABLE IF EXISTS all_transaction;

CREATE TABLE all_transaction (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    member_name TEXT NOT NULL,
    state_district_number TEXT NOT NULL,
    company TEXT NOT NULL,
    ticker TEXT NOT NULL,
    transaction_type TEXT NOT NULL,
    transaction_date DATE NOT NULL,
    value_lb INTEGER NOT NULL,
    value_ub INTEGER NOT NULL,
    description TEXT DEFAULT NULL,
    link TEXT NOT NULL
);