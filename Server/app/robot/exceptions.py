from fastapi import HTTPException

from users.schemes import Ticket


class InvalidTicketWagon(HTTPException):
    def __init__(self, ticket: Ticket):
        super().__init__(status_code=400, detail={
            "message": "Invalid wagon number",
            "right_ticket": ticket.model_dump()
        })


class InvalidTicketDate(HTTPException):
    def __init__(self, ticket: Ticket):
        super().__init__(status_code=400, detail={
            "message": "Invalid date",
            "right_ticket": ticket.model_dump()
        })


class InvalidTicketTrain(HTTPException):
    def __init__(self, ticket: Ticket):
        super().__init__(status_code=400, detail={
            "message": "Invalid train number",
            "right_ticket": ticket.model_dump()
        })


class InvalidWithoutTickets(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail="User haven`t any active tickets")
