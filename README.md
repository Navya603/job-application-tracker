# Job Application Tracker

A dependency-free Python command-line tool for tracking job applications in a
local SQLite database.

## Run it

```bash
python3 main.py
```

The app creates `database/jobs.db` automatically. The database stays on your
computer and is ignored by Git.

## Features

- Add applications with company, role, location, status, dates, salary, and notes.
- View all applications or filter them by status.
- Search by company, role, location, status, or notes.
- Update an application's status and interview date.
- Delete an application with an explicit confirmation.
- View status counts, response rate, monthly volume, and salary averages.

Supported statuses are `Applied`, `Interviewing`, `Offer`, `Rejected`, and
`Withdrawn`.
