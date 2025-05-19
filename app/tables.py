cursor.execute("""
CREATE TABLE events(
    id serial PRIMARY KEY,
    name text NOT NULL,
    date date NOT NULL,
    time time NOT NULL
);
""")
conn.commit()

