from pydantic import BaseModel


class ErrorItem(BaseModel):
    field: str
    message: str


class ErrorResponse(BaseModel):
    error: str
    details: list[ErrorItem] = []