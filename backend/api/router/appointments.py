import uuid

from fastapi import APIRouter, Depends, HTTPException

import crud.appointment as crud
from api.deps import get_user_is_admin_user, SessionDep, CurrentUser
from schema.appointment import AppointmentsPublic, AppointmentPublic, AppointmentCreate, AppointmentUpdate
from crud.user import get_user_by_id

router = APIRouter(prefix="/appointments", tags=["appointments"])

@router.get("",
            dependencies=[Depends(get_user_is_admin_user)],
            response_model=AppointmentsPublic)
async def read_appointments(session: SessionDep, skip: int = 0, limit: int = 100):
    return crud.get_all_appointments(session=session, offset=skip, limit=limit)

@router.get("/mine",
            response_model=AppointmentsPublic)
async def read_appointments_mine(session: SessionDep, current_user: CurrentUser):
    return crud.get_appointments_by_owner(session=session, owner_id=current_user.id)

@router.post("/mine", response_model=AppointmentPublic)
async def create_appointment_mine(session: SessionDep, current_user: CurrentUser, appointment_in: AppointmentCreate):
     return crud.create_appointment(session=session, appointment_in=appointment_in, owner_id=current_user.id)

@router.get("/{appointment_id}",
            dependencies=[Depends(get_user_is_admin_user)],
            response_model=AppointmentPublic)
async def read_appointment(session: SessionDep, appointment_id: uuid.UUID):
    db_appointment = crud.get_appointment_by_id(session=session, appointment_id=appointment_id)
    if not db_appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return db_appointment

@router.patch("/{appointment_id}",
              dependencies=[Depends(get_user_is_admin_user)])
async def update_appointment(session: SessionDep, appointment_id: uuid.UUID, appointment_in: AppointmentUpdate):
    db_appointment = crud.get_appointment_by_id(session=session, appointment_id=appointment_id)
    if not db_appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return crud.update_appointment(session=session, db_appointment=db_appointment, appointment_in=appointment_in)

@router.delete("/{appointment_id}",
               dependencies=[Depends(get_user_is_admin_user)])
async def delete_appointment(session: SessionDep, appointment_id: uuid.UUID):
    db_appointment = crud.get_appointment_by_id(session=session, appointment_id=appointment_id)
    if not db_appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    crud.delete_appointment_by_id(session=session, appointment_id=appointment_id)
    return {"message": "Successfully deleted appointment"}

@router.get("/mine/{appointment_id}",
            response_model=AppointmentPublic)
async def read_appointment_mine(session: SessionDep, current_user: CurrentUser, appointment_id: uuid.UUID):
    db_appointment = crud.get_appointment_by_id(session=session, appointment_id=appointment_id)
    if not db_appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    if db_appointment.owner is not current_user:
        raise HTTPException(status_code=403, detail="You are not the owner of the appointment")
    return db_appointment

@router.patch("/mine/{appointment_id}", response_model=AppointmentPublic)
async def update_appointment_mine(session: SessionDep, current_user: CurrentUser, appointment_id: uuid.UUID,appointment_in: AppointmentUpdate):
    db_appointment = crud.get_appointment_by_id(session=session, appointment_id=appointment_id)
    if not db_appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    if db_appointment.owner is not current_user:
        raise HTTPException(status_code=403, detail="You are not the owner of the appointment")
    return crud.update_appointment(session=session, db_appointment=db_appointment, appointment_in=appointment_in)

@router.delete("/mine/{appointment_id}")
async def delete_appointment_mine(session: SessionDep, current_user: CurrentUser, appointment_id: uuid.UUID):
    db_appointment = crud.get_appointment_by_id(session=session, appointment_id=appointment_id)
    if db_appointment is None:
        raise HTTPException(status_code=404, detail="Appointment not found")
    if db_appointment.owner is not current_user:
        raise HTTPException(status_code=403, detail="You are not the owner of the appointment")
    crud.delete_appointment_by_id(session=session, appointment_id=appointment_id)
    return {"message": "Successfully deleted appointment"}

@router.get("/owner/{owner_id}",
            dependencies=[Depends(get_user_is_admin_user)],
            response_model=AppointmentsPublic)
async def read_appointments_by_owner(session: SessionDep, owner_id: int):
    db_user = get_user_by_id(session=session, user_id=owner_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.get_appointments_by_owner(session=session, owner_id=owner_id)

@router.post("/owner/{owner_id}",
             dependencies=[Depends(get_user_is_admin_user)],
             response_model=AppointmentPublic)
async def create_appointment_for_owner(session: SessionDep, owner_id: int, appointment_in: AppointmentCreate):
    return crud.create_appointment(session=session, appointment_in=appointment_in, owner_id=owner_id)