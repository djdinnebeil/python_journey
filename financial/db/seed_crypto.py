from .connection import DatabaseConnection
# Inserting examples

def insert_crypto_companies_and_data():
    conn = DatabaseConnection.get_connection()  # Retrieve the database connection
    cursor = conn.cursor()

    # Insert cryptocurrency companies
    companies_insert_query = '''
    INSERT INTO companies (id, ticker, name, company_type) VALUES (?, ?, ?, ?)
    '''
    crypto_companies_data = [
        (2001, 'XBTC', 'Bitcoin', 'crypto'),
        (2002, 'XETH', 'Ethereum', 'crypto')
    ]
    cursor.executemany(companies_insert_query, crypto_companies_data)

    # Insert time series data for the cryptocurrency companies
    time_series_insert_query = '''
    INSERT INTO TimeSeries (company_id, date, value) VALUES (?, ?, ?)
    '''
    time_series_data = [
        (2001, '2024-09-20', 43000.00),
        (2001, '2024-09-21', 43500.50),
        (2002, '2024-09-20', 3000.00),
        (2002, '2024-09-21', 3050.75)
    ]
    cursor.executemany(time_series_insert_query, time_series_data)

    conn.commit()  # Commit the transactions

# Example usage
db_connection = DatabaseConnection()  # Initialize the database connection
insert_crypto_companies_and_data()  # Insert the data