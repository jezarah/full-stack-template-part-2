import uuid

from sqlmodel import Field, Relationship

from schema.user import UserBase
from schema.appointment import AppointmentBase

class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    role: int = 0
    hashed_password: str
    appointments: list["Appointment"] = Relationship(back_populates="owner", cascade_delete=True)


class Appointment(AppointmentBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str = Field(max_length=255)
    owner_id: int = Field(foreign_key="user.id", nullable=False, ondelete="CASCADE")
    owner: User = Relationship(back_populates="appointments")
