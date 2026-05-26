import sqlite3

DATABASE_NAME = "logdata.db"

# CREATE TABLE FUNCTION
def create_table():

    conn = sqlite3.connect(DATABASE_NAME)

    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS analytics (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        filename TEXT,

        metric TEXT,

        count INTEGER
    )
    ''')

    conn.commit()

    conn.close()


# SAVE RESULTS
def save_results(filename, results):

    conn = sqlite3.connect(DATABASE_NAME)

    cursor = conn.cursor()

    for key, value in results.items():

        cursor.execute('''
        INSERT INTO analytics (filename, metric, count)
        VALUES (?, ?, ?)
        ''', (filename, key, value))

    conn.commit()

    conn.close()


# FETCH RESULTS
def fetch_results():

    conn = sqlite3.connect(DATABASE_NAME)

    cursor = conn.cursor()

    cursor.execute('SELECT * FROM analytics')

    data = cursor.fetchall()

    conn.close()

    return data


# CREATE TABLE AUTOMATICALLY
create_table()