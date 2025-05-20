from db_singleton import DatabaseConnection
from datetime import datetime, timedelta
import random
import numpy as np

# Domestic companies (default company_type will be used)
companies = [
    (1, 'AAPL', 'Apple Inc.'),
    (2, 'GOOGL', 'Alphabet Inc.'),
    (3, 'MSFT', 'Microsoft Corporation'),
    (4, 'AMZN', 'Amazon.com Inc.'),
    (5, 'TSLA', 'Tesla Inc.'),
    (6, 'FB', 'Meta Platforms Inc.'),
    (7, 'NVDA', 'NVIDIA Corporation'),
    (8, 'NFLX', 'Netflix Inc.'),
    (9, 'ADBE', 'Adobe Inc.'),
    (10, 'ORCL', 'Oracle Corporation')
]

# Foreign companies (explicit company_type)
foreign_companies = [
    (1001, 'ZZZZ', 'Foreign Company A', 'foreign'),
    (1002, 'ZZZZ', 'Foreign Company B', 'foreign')
]

start_date = datetime(2023, 1, 1)
num_entries = 100

time_series_data = []

for company in companies + [(fc[0], fc[1], fc[2]) for fc in foreign_companies]:
    company_id = company[0]
    for i in range(num_entries):
        date = start_date + timedelta(days=i)
        value = round(random.uniform(100, 500), 2)
        time_series_data.append((company_id, value, date.strftime('%Y-%m-%d')))

def generate_time_series(company_id, start_date, num_days, initial_value):
    date_list = [start_date + timedelta(days=x) for x in range(num_days)]
    value_list = initial_value + np.random.normal(0, 1, num_days).cumsum()
    return [(company_id, float(v), date.strftime('%Y-%m-%d')) for date, v in zip(date_list, value_list)]

# Add extra variation for foreign company time series
time_series_data += generate_time_series(1001, start_date, 100, 100.0)
time_series_data += generate_time_series(1002, start_date, 100, 100.0)

with DatabaseConnection() as conn:
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS companies (
        id INTEGER PRIMARY KEY,
        ticker TEXT NOT NULL,
        name TEXT NOT NULL,
        company_type TEXT NOT NULL DEFAULT 'domestic' CHECK (company_type IN ('domestic', 'foreign'))
    )
    ''')

    # Insert domestic companies
    cursor.executemany('''
    INSERT OR IGNORE INTO companies (id, ticker, name)
    VALUES (?, ?, ?)
    ''', companies)

    # Insert foreign companies with explicit company_type
    cursor.executemany('''
    INSERT OR IGNORE INTO companies (id, ticker, name, company_type)
    VALUES (?, ?, ?, ?)
    ''', foreign_companies)

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS TimeSeries (
        id INTEGER PRIMARY KEY,
        company_id INTEGER,
        value REAL,
        date TEXT,
        FOREIGN KEY (company_id) REFERENCES companies(id)
    )
    ''')

    cursor.executemany('''
    INSERT INTO TimeSeries (company_id, value, date)
    VALUES (?, ?, ?)
    ''', time_series_data)

    conn.commit()
