class ReportRequestObject(object):

    def __init__(self, cancel_count, company, requests, completed_request, active):
        self.cancel_count = cancel_count
        self.company = company
        self.requests = requests
        self.completed_request = completed_request
        self.active = active
