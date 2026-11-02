from utils import query_duckdb

query_duckdb("""
    CREATE TABLE IF NOT EXISTS movies (
        title TEXT,
        year INT,
        genre TEXT,
        rating TINYINT
    );
""")