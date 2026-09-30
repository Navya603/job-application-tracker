"""Data models used by the tracker."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class JobApplication:
    company: str
    role: str
    location: str
    application_date: str
    status: str
    interview_date: str | None = None
    salary: float | None = None
    notes: str | None = None
    id: int | None = None
