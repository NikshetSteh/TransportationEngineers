from fastapi import HTTPException
from users.schemes import Ticket


class InvalidTicketWagon(HTTPException):
    def __init__(self, ticket: Ticket):
        buffer = ticket.model_dump()
        buffer["date"] = buffer["date"].isoformat()
        super().__init__(
            status_code=400,
            detail={"message": "Invalid wagon number", "right_ticket": buffer},
        )


class InvalidTicketDate(HTTPException):
    def __init__(self, ticket: Ticket):
        buffer = ticket.model_dump()
        buffer["date"] = buffer["date"].isoformat()
        super().__init__(
            status_code=400, detail={"message": "Invalid date", "right_ticket": buffer}
        )


class InvalidTicketTrain(HTTPException):
    def __init__(self, ticket: Ticket):
        buffer = ticket.model_dump()
        buffer["date"] = buffer["date"].isoformat()
        buffer["start_date"] = buffer["start_date"].isoformat()
        super().__init__(
            status_code=400,
            detail={"message": "Invalid train number", "right_ticket": buffer},
        )


class InvalidWithoutTickets(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail="User haven`t any active tickets")


class InvalidTicketCode(HTTPException):
    def __init__(self):
        super().__init__(status_code=401, detail="Invalid ticket code")
