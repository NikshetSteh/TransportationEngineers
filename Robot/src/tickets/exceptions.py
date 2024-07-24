from tickets.schemes import Ticket


class InvalidTicket(Exception):
    def __init__(self, message: str, right_ticket: Ticket = None):
        super().__init__(message)
        self.right_ticket = right_ticket
