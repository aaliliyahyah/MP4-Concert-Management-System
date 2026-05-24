from datetime import datetime, timedelta
from .Record import Record
from utils import (
    print_message,
    print_success,
    print_error,
    display_attendees,
    display_durations,
    display_violations,
)


class Concert(Record):
    def __init__(self, **dur):
        super().__init__()
        self.duration = timedelta(
            hours=dur["hours"], minutes=dur["mins"], seconds=dur["secs"]
        )

    def pushAttendee(self):
        name = input(">>>  Enter attendee name (or press Enter to cancel): ").strip()
        if not name:
            return print_error("Push cancelled: name cannot be empty.")

        existing_ids = [a.get("ticketID", 0) for a in self.record]
        next_ticket = max(existing_ids) + 1 if existing_ids else 1

        attendee = {
            "ticketID": next_ticket,
            "name": name,
            "entryTime": datetime.now(),
            "exitTime": None,
        }

        self.attendees.append(attendee)
        self.record.append(attendee)
        print_success(f"{name} entered. Ticket: {next_ticket}")

    def popAttendee(self):
        if self._isEmpty():
            return print_error("No attendees inside the venue.")

        attendee = self.attendees.pop()
        attendee["exitTime"] = datetime.now()
        ticket_id, name, _, exit_time = self._getAttendeeData(attendee)

        print_success(
            f"{name} exited the venue. "
            f"Ticket: {ticket_id} | "
            f"Exit Time: {exit_time.strftime('%H:%M:%S')}"
        )

    def peekLastAttendee(self):
        if self._isEmpty():
            return print_error("There are no people inside.")

        ticket_id, name, entry_time, _ = self._getAttendeeData(self.attendees[-1])
        print_message(
            f"Last Attendee: ID: {ticket_id}, Name: {name}, "
            f"Entry Time: {entry_time.strftime('%H:%M:%S')}"
        )

    def getAttendanceDuration(self):
        if not self.record:
            return print_error("There are no attendees on record.")

        durations = []
        for rec in self.record:
            if rec["entryTime"] is None:
                continue
            end = rec["exitTime"] or datetime.now()
            delta = timedelta(seconds=int((end - rec["entryTime"]).total_seconds()))
            durations.append((rec["ticketID"], rec["name"], delta))

        display_durations(durations)
        return durations

    def detectRuleViolations(self):
        if not self.record:
            return print_error("There are no attendees on record.")

        violations = []
        for rec in self.record:
            if rec["entryTime"] is None:
                continue

            end = rec["exitTime"] or datetime.now()
            attended = end - rec["entryTime"]

            if attended > self.duration:
                violations.append((rec["ticketID"], rec["name"], "overstay"))
            elif rec["exitTime"] and attended < self.duration:
                violations.append((rec["ticketID"], rec["name"], "early exit"))

        display_violations(violations)
        return violations

    def displayAttendees(self):
        pass
    
    def generateAttendanceReport(self):
        pass
    # -------------------------
    # Private helpers
    # -------------------------

    def _isEmpty(self):
        return not self.attendees

    def _getAttendeeData(self, attendee):
        return (
            attendee["ticketID"],
            attendee["name"],
            attendee["entryTime"],
            attendee["exitTime"],
        )