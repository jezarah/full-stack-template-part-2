import uuid

from sqlmodel import Session

from model.models import Appointment
from schema.appointment import AppointmentCreate


def create_appointment(*, session: Session, appointment_in: AppointmentCreate, owner_id: uuid.UUID) -> Appointment:
    db_appointment = Appointment.model_validate(appointment_in, update={"owner_id": owner_id})
    session.add(db_appointment)
    session.commit()
    session.refresh(db_appointment)
    return db_appointment