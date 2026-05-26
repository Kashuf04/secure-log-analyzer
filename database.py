import sqlite3

# Create database connection
conn = sqlite3.connect('logdata.db', check_same_thread=False)

cursor = conn.cursor()

# Create analytics table
cursor.execute('''
CREATE TABLE IF NOT EXISTS analytics (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    filename TEXT,

    metric TEXT,

    count INTEGER
)
''')

conn.commit()


# SAVE RESULTS FUNCTION
def save_results(filename, results):

    for key, value in results.items():

        cursor.execute('''
        INSERT INTO analytics (filename, metric, count)
        VALUES (?, ?, ?)
        ''', (filename, key, value))

    conn.commit()


# FETCH RESULTS FUNCTION
def fetch_results():

    cursor.execute('SELECT * FROM analytics')

    return cursor.fetchall()