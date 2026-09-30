import sqlite3

from database import get_connection
from models import JobApplication


def add_application(job):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO job_applications
        (
            company,
            role,
            location,
            application_date,
            status,
            interview_date,
            salary,
            notes
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        job.company,
        job.role,
        job.location,
        job.application_date,
        job.status,
        job.interview_date,
        job.salary,
        job.notes
    ))

    connection.commit()
    connection.close()

    print("Job application added successfully! ✅")