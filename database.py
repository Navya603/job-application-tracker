import sqlite3

DATABASE_NAME = "database/jobs.db"


def get_connection():
    return sqlite3.connect(DATABASE_NAME)


def create_table():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS job_applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company TEXT NOT NULL,
            role TEXT NOT NULL,
            location TEXT,
            application_date TEXT NOT NULL,
            status TEXT NOT NULL,
            interview_date TEXT,
            salary REAL,
            notes TEXT
        )
    """)

    connection.commit()
    connection.close()


if __name__ == "__main__":
    create_table()
    print("Database created successfully!")