class Record:
    def __init__(self):
        # To preserve attendees data
        self.record = []
        # Stack
        self.attendees = [
            {"ticketID": 1, "name": "Tester 1", "entryTime": None, "exitTime": None},
            {"ticketID": 2, "name": "Tester 2", "entryTime": None, "exitTime": None},
        ]
