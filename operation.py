"""Database operations for job applications."""

from __future__ import annotations

from collections import Counter
from pathlib import Path

from database import create_table, get_connection
from models import JobApplication


STATUSES = ("Applied", "Interviewing", "Offer", "Rejected", "Withdrawn")


def _normalise_status(status: str) -> str:
    for allowed_status in STATUSES:
        if status.casefold() == allowed_status.casefold():
            return allowed_status
    allowed = ", ".join(STATUSES)
    raise ValueError(f"Status must be one of: {allowed}.")


def _application_from_row(row) -> JobApplication:
    return JobApplication(
        id=row["id"],
        company=row["company"],
        role=row["role"],
        location=row["location"] or "",
        application_date=row["application_date"],
        status=row["status"],
        interview_date=row["interview_date"],
        salary=row["salary"],
        notes=row["notes"],
    )


def add_application(job: JobApplication, database_path: str | Path | None = None) -> int:
    """Store an application and return its generated ID."""
    create_table(database_path)
    status = _normalise_status(job.status)
    with get_connection(database_path) as connection:
        cursor = connection.execute(
            """
            INSERT INTO job_applications (
                company, role, location, application_date, status,
                interview_date, salary, notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                job.company.strip(),
                job.role.strip(),
                job.location.strip() or None,
                job.application_date,
                status,
                job.interview_date,
                job.salary,
                job.notes.strip() if job.notes else None,
            ),
        )
        return int(cursor.lastrowid)


def get_applications(
    database_path: str | Path | None = None, status: str | None = None
) -> list[JobApplication]:
    """Return all applications, newest first, optionally filtered by status."""
    create_table(database_path)
    query = "SELECT * FROM job_applications"
    parameters: tuple[str, ...] = ()
    if status:
        query += " WHERE status = ?"
        parameters = (_normalise_status(status),)
    query += " ORDER BY application_date DESC, id DESC"

    with get_connection(database_path) as connection:
        rows = connection.execute(query, parameters).fetchall()
    return [_application_from_row(row) for row in rows]


def search_applications(
    query: str, database_path: str | Path | None = None
) -> list[JobApplication]:
    """Find applications by company, role, location, status, or notes."""
    create_table(database_path)
    pattern = f"%{query.strip()}%"
    with get_connection(database_path) as connection:
        rows = connection.execute(
            """
            SELECT * FROM job_applications
            WHERE company LIKE ? COLLATE NOCASE
               OR role LIKE ? COLLATE NOCASE
               OR location LIKE ? COLLATE NOCASE
               OR status LIKE ? COLLATE NOCASE
               OR notes LIKE ? COLLATE NOCASE
            ORDER BY application_date DESC, id DESC
            """,
            (pattern, pattern, pattern, pattern, pattern),
        ).fetchall()
    return [_application_from_row(row) for row in rows]


def update_status(
    application_id: int,
    status: str,
    interview_date: str | None = None,
    database_path: str | Path | None = None,
) -> bool:
    """Update an application's status and optionally its interview date."""
    create_table(database_path)
    normalised_status = _normalise_status(status)
    with get_connection(database_path) as connection:
        if interview_date is None:
            cursor = connection.execute(
                "UPDATE job_applications SET status = ? WHERE id = ?",
                (normalised_status, application_id),
            )
        else:
            cursor = connection.execute(
                """
                UPDATE job_applications
                SET status = ?, interview_date = ?
                WHERE id = ?
                """,
                (normalised_status, interview_date, application_id),
            )
        return cursor.rowcount > 0


def delete_application(application_id: int, database_path: str | Path | None = None) -> bool:
    """Delete an application by ID. Returns whether a record was removed."""
    create_table(database_path)
    with get_connection(database_path) as connection:
        cursor = connection.execute(
            "DELETE FROM job_applications WHERE id = ?", (application_id,)
        )
        return cursor.rowcount > 0


def get_statistics(database_path: str | Path | None = None) -> dict[str, object]:
    """Return totals and response metrics for the dashboard."""
    applications = get_applications(database_path)
    by_status = Counter(application.status for application in applications)
    total = len(applications)
    interviews = by_status["Interviewing"]
    offers = by_status["Offer"]
    responses = interviews + offers + by_status["Rejected"]

    return {
        "total": total,
        "by_status": by_status,
        "interviews": interviews,
        "offers": offers,
        "response_rate": (responses / total * 100) if total else 0.0,
    }


def get_analytics(database_path: str | Path | None = None) -> dict[str, list[tuple[str, float | int]]]:
    """Return application volume and salary averages for the analytics view."""
    create_table(database_path)
    with get_connection(database_path) as connection:
        monthly_rows = connection.execute(
            """
            SELECT substr(application_date, 1, 7) AS month, COUNT(*) AS total
            FROM job_applications
            GROUP BY month
            ORDER BY month DESC
            """
        ).fetchall()
        salary_rows = connection.execute(
            """
            SELECT status, ROUND(AVG(salary), 2) AS average_salary
            FROM job_applications
            WHERE salary IS NOT NULL
            GROUP BY status
            ORDER BY average_salary DESC
            """
        ).fetchall()
    return {
        "monthly_applications": [(row["month"], row["total"]) for row in monthly_rows],
        "average_salary_by_status": [
            (row["status"], row["average_salary"]) for row in salary_rows
        ],
    }
