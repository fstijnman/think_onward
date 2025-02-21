import duckdb

db_path = "data/eaglei_data.duckdb"
conn = duckdb.connect(db_path)
conn.execute(
    "CREATE TABLE eaglei_data AS SELECT * FROM read_csv('data/eaglei_data/*.csv')"
)
