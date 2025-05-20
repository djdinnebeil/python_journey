# db/create_schema.py
from .connection import DatabaseConnection

def create_tables():
    with DatabaseConnection() as conn:
        cursor = conn.cursor()

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS companies (
            id INTEGER PRIMARY KEY,
            ticker TEXT NOT NULL,
            name TEXT NOT NULL,
            company_type TEXT NOT NULL DEFAULT 'domestic'
                CHECK (company_type IN ('domestic', 'foreign', 'crypto'))
        )
        ''')

        cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_companies_ticker ON companies (ticker)
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS TimeSeries (
            id INTEGER PRIMARY KEY,
            company_id INTEGER,
            value REAL,
            date TEXT,
            FOREIGN KEY (company_id) REFERENCES companies(id)
        )
        ''')

        cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_timeseries_company_id ON TimeSeries (company_id)
        ''')

if __name__ == '__main__':
    create_tables()
