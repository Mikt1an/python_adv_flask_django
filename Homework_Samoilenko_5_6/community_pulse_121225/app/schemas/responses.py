from typing import Annotated
from pydantic import BaseModel, Field, ConfigDict


class ResponseBase(BaseModel):
    question_id: Annotated[int, Field(gt=0)]
    is_agree: bool


class ResponseCreate(ResponseBase):
    pass


class ResponseUpdate(ResponseBase):
    is_agree: bool | None = None


class ResponseRead(ResponseBase):
    id: int