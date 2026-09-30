"""Interactive command-line job application tracker."""

from __future__ import annotations

from datetime import date

from database import create_table
from models import JobApplication
from operation import (
    STATUSES,
    add_application,
    delete_application,
    get_analytics,
    get_applications,
    get_statistics,
    search_applications,
    update_status,
)


def prompt_required(label: str) -> str:
    while True:
        value = input(f"{label}: ").strip()
        if value:
            return value
        print(f"{label} is required.")


def prompt_date(label: str, *, default: str | None = None, optional: bool = False) -> str | None:
    suffix = f" [{default}]" if default else ""
    while True:
        value = input(f"{label}{suffix}: ").strip()
        if not value and default:
            return default
        if not value and optional:
            return None
        try:
            return date.fromisoformat(value).isoformat()
        except ValueError:
            print("Enter a date in YYYY-MM-DD format.")


def prompt_status(default: str = "Applied") -> str:
    choices = ", ".join(STATUSES)
    while True:
        value = input(f"Status ({choices}) [{default}]: ").strip() or default
        for status in STATUSES:
            if value.casefold() == status.casefold():
                return status
        print(f"Choose one of: {choices}.")


def prompt_optional_salary() -> float | None:
    while True:
        value = input("Salary (optional): ").strip()
        if not value:
            return None
        try:
            salary = float(value)
            if salary < 0:
                raise ValueError
            return salary
        except ValueError:
            print("Enter a non-negative number, or leave it blank.")


def print_applications(applications: list[JobApplication]) -> None:
    if not applications:
        print("\nNo applications found.")
        return

    headers = ("ID", "Company", "Role", "Location", "Applied", "Status", "Interview")
    rows = [
        (
            str(application.id),
            application.company,
            application.role,
            application.location or "—",
            application.application_date,
            application.status,
            application.interview_date or "—",
        )
        for application in applications
    ]
    widths = [
        max(len(header), *(len(row[index]) for row in rows))
        for index, header in enumerate(headers)
    ]
    separator = "+".join("-" * (width + 2) for width in widths)
    print()
    print(" | ".join(header.ljust(widths[index]) for index, header in enumerate(headers)))
    print(separator)
    for row in rows:
        print(" | ".join(value.ljust(widths[index]) for index, value in enumerate(row)))


def add_application_flow() -> None:
    print("\nAdd a job application")
    status = prompt_status()
    job = JobApplication(
        company=prompt_required("Company"),
        role=prompt_required("Role"),
        location=input("Location (optional): ").strip(),
        application_date=prompt_date("Application date", default=date.today().isoformat()) or "",
        status=status,
        interview_date=(
            prompt_date("Interview date (optional)", optional=True)
            if status == "Interviewing"
            else None
        ),
        salary=prompt_optional_salary(),
        notes=input("Notes (optional): ").strip() or None,
    )
    application_id = add_application(job)
    print(f"Application #{application_id} saved.")


def view_applications_flow() -> None:
    filter_status = input("Filter by status (leave blank for all): ").strip()
    try:
        applications = get_applications(status=filter_status or None)
    except ValueError as error:
        print(error)
        return
    print_applications(applications)


def search_applications_flow() -> None:
    query = prompt_required("Search term")
    print_applications(search_applications(query))


def update_status_flow() -> None:
    print_applications(get_applications())
    try:
        application_id = int(prompt_required("Application ID"))
    except ValueError:
        print("Application ID must be a number.")
        return
    status = prompt_status()
    interview_date = None
    if status == "Interviewing":
        interview_date = prompt_date("Interview date (optional)", optional=True)
    if update_status(application_id, status, interview_date):
        print("Status updated.")
    else:
        print("No application has that ID.")


def delete_application_flow() -> None:
    print_applications(get_applications())
    try:
        application_id = int(prompt_required("Application ID to delete"))
    except ValueError:
        print("Application ID must be a number.")
        return
    confirmation = input("Type DELETE to confirm: ").strip()
    if confirmation != "DELETE":
        print("Deletion cancelled.")
        return
    print("Application deleted." if delete_application(application_id) else "No application has that ID.")


def show_statistics() -> None:
    statistics = get_statistics()
    print(f"\nTotal applications: {statistics['total']}")
    for status in STATUSES:
        print(f"  {status}: {statistics['by_status'][status]}")
    print(f"Interviews: {statistics['interviews']}")
    print(f"Offers: {statistics['offers']}")
    print(f"Response rate: {statistics['response_rate']:.1f}%")


def show_analytics() -> None:
    analytics = get_analytics()
    print("\nApplications by month")
    if analytics["monthly_applications"]:
        for month, total in analytics["monthly_applications"]:
            print(f"  {month}: {total}")
    else:
        print("  No applications yet.")

    print("\nAverage salary by status")
    if analytics["average_salary_by_status"]:
        for status, average_salary in analytics["average_salary_by_status"]:
            print(f"  {status}: {average_salary:,.2f}")
    else:
        print("  No salary data yet.")


def main() -> None:
    create_table()
    actions = {
        "1": add_application_flow,
        "2": view_applications_flow,
        "3": search_applications_flow,
        "4": update_status_flow,
        "5": delete_application_flow,
        "6": show_statistics,
        "7": show_analytics,
    }

    while True:
        print("\n==============================")
        print("   JOB APPLICATION TRACKER")
        print("==============================")
        print("1. Add Job Application")
        print("2. View Applications")
        print("3. Search Applications")
        print("4. Update Status")
        print("5. Delete Application")
        print("6. Statistics")
        print("7. Analytics")
        print("8. Exit")

        choice = input("\nEnter your choice: ").strip()
        if choice == "8":
            print("Thank you for using Job Application Tracker!")
            return
        action = actions.get(choice)
        if action:
            action()
        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nGoodbye!")
