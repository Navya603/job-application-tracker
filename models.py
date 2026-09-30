class JobApplication:

    def __init__(
        self,
        company,
        role,
        location,
        application_date,
        status,
        interview_date=None,
        salary=None,
        notes=None
    ):
        self.company = company
        self.role = role
        self.location = location
        self.application_date = application_date
        self.status = status
        self.interview_date = interview_date
        self.salary = salary
        self.notes = notes