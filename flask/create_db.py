# create_db.py
import sqlite3

# Connect to (or create) example.db
conn = sqlite3.connect('example.db')
cursor = conn.cursor()

# Drop the users table if it already exists
cursor.execute('DROP TABLE IF EXISTS users')

# Create a users table
cursor.execute('''
    CREATE TABLE users (
        username TEXT PRIMARY KEY,
        password TEXT NOT NULL
    )
''')

# Insert some sample users
users = [
    ('admin', 'adminpass'),
    ('dj', 'python123'),
    ('laurence', 'flaskrocks')
]

cursor.executemany('INSERT INTO users (username, password) VALUES (?, ?)', users)

# Save changes and close
conn.commit()
conn.close()

print('Database created and seeded!')
