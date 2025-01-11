import uuid
from datetime import datetime

from sqlmodel import Field, SQLModel


class AppointmentBase(SQLModel):
    title: str = Field(max_length=255)
    description: str | None = Field(default=None, max_length=511)
    appointment_time: datetime


# Create
class AppointmentCreate(AppointmentBase):
    pass


# Read (or Delete), id is always required
class AppointmentPublic(AppointmentBase):
    id: uuid.UUID
    owner_id: uuid.UUID


class AppointmentsPublic(SQLModel):
    data: list[AppointmentPublic]
    count: int


# Update
class AppointmentUpdate(AppointmentBase):
    title: str | None = Field(default=None, max_length=255)
    appointment_time: datetime | None = Field(default=None)
