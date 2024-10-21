import datetime
from typing import Literal

from pydantic import BaseModel


class IdReturnBase(BaseModel):
    id: int


class StatusSuccessBase(BaseModel):
    status: Literal["success"]


class GetAdvResponse(BaseModel):

    id: int
    title: str
    description: str
    price: float
    creator: str
    created_at: datetime.datetime


class CreateAdvRequest(BaseModel):
    title: str
    description: str
    price: float
    creator: str


class CreateAdvResponse(IdReturnBase):
    pass


class UpdateAdvRequest(BaseModel):
    title: str | None = None
    description: str | None = None
    price: float | None = None
    creator: str | None = None


class UpdateAdvResponse(IdReturnBase):
    pass


class DeleteAdvResponse(StatusSuccessBase):
    pass
