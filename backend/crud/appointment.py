import uuid

from sqlmodel import Session, select, delete, col

from model.models import Appointment
from schema.appointment import AppointmentCreate, AppointmentsPublic, AppointmentUpdate, AppointmentPublic


def create_appointment(*, session: Session, appointment_in: AppointmentCreate, owner_id: int) -> Appointment:
    db_appointment = Appointment.model_validate(appointment_in, update={"owner_id": owner_id})
    session.add(db_appointment)
    session.commit()
    session.refresh(db_appointment)
    return db_appointment


def update_appointment(*, session: Session, db_appointment: Appointment, appointment_in: AppointmentUpdate) -> Appointment:
    appointment_data = appointment_in.model_dump(exclude_unset=True)
    db_appointment.sqlmodel_update(appointment_data)
    session.add(db_appointment)
    session.commit()
    session.refresh(db_appointment)
    return db_appointment


def get_all_appointments(*, session: Session, limit: int, offset: int) -> AppointmentsPublic | None:
    statement = select(Appointment).limit(limit).offset(offset).order_by(Appointment.appointment_time)
    appointments = session.exec(statement).all()
    session_appointments = AppointmentsPublic(
        data=appointments,
        count=len(appointments)
    )
    return session_appointments


def get_appointments_by_owner(*, session: Session, owner_id: int) -> AppointmentsPublic | None:
    statement = select(Appointment).where(Appointment.owner_id == owner_id)
    appointments = session.exec(statement).all()
    session_appointments = AppointmentsPublic(
        data=appointments,
        count=len(appointments)
    )
    return session_appointments


def get_appointment_by_id(*, session: Session, appointment_id: uuid.UUID) -> AppointmentPublic | None:
    statement = select(Appointment).where(Appointment.id == appointment_id)
    appointment = session.exec(statement).first()
    return appointment


def delete_appointment_by_id(*, session: Session, appointment_id: uuid.UUID) -> None:
    statement = delete(Appointment).where(col(Appointment.id) == appointment_id)
    session.exec(statement)
    session.commit()
