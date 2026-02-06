"""NotificationService - due date reminders and availability alerts."""

from datetime import datetime
from member import Member


class NotificationService:
    """Sends notifications to members about due dates and book availability."""

    @staticmethod
    def send_due_reminder(member: Member) -> None:
        """Remind member about books nearing due date."""
        for item in member.checked_out_items:
            if item.due_date:
                days_left = (item.due_date - datetime.now()).days
                if days_left <= 3:
                    print(f"    [Reminder -> {member.name}] "
                          f"'{item.book.title}' due in {days_left} day(s)!")

    @staticmethod
    def send_availability_alert(member: Member, book_title: str) -> None:
        """Notify member that a book they wanted is now available."""
        print(f"    [Alert -> {member.name}] '{book_title}' is now available!")

    @staticmethod
    def send_overdue_notice(member: Member, book_title: str, days: int) -> None:
        """Notify member about an overdue book."""
        print(f"    [Overdue -> {member.name}] '{book_title}' is {days} day(s) overdue!")
