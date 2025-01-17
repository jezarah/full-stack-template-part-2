from typing import cast

from fastapi import APIRouter, Depends, HTTPException

import crud.user as crud
from schema.user import UsersPublic, UserCreate, UserPublic, UserUpdate, UserRegister
from api.deps import SessionDep, get_user_is_admin_user, CurrentUser

router = APIRouter(prefix="/users", tags=["users"])

@router.get(
"",
    dependencies=[Depends(get_user_is_admin_user)],
    response_model=UsersPublic)
async def read_users(session: SessionDep, skip: int = 0, limit: int = 100):
    return crud.get_all_users(session=session, offset=skip, limit=limit)

@router.post(
    "",
    dependencies=[Depends(get_user_is_admin_user)],
    response_model=UserPublic)
async def create_user(session: SessionDep, user_in: UserCreate):
    user = crud.get_user_by_email(session=session, email=cast(str, user_in.email))
    if user:
        raise HTTPException(
            status_code=409,
            detail="The user with this email already exists in the system",
        )
    return crud.create_user(session=session, user_create=user_in)

@router.post("/signup", response_model=UserPublic)
async def create_user_registration(session: SessionDep, user_in: UserRegister):
    user = crud.get_user_by_email(session=session, email=cast(str, user_in.email))
    if user:
        raise HTTPException(
            status_code=409,
            detail="The user with this email already exists in the system",
        )
    default_user_in = UserCreate(
        name=user_in.name,
        email=user_in.email,
        password=user_in.password,
        role=0
    )
    return crud.create_user(session=session, user_create=default_user_in)

@router.get("/me", response_model=UserPublic)
async def read_user_me(current_user: CurrentUser):
    return current_user

@router.patch("/me")
async def update_user_me(session: SessionDep, current_user: CurrentUser, user_in: UserUpdate):
    message = "Successfully updated user information"
    if user_in.email is not None and user_in.email != current_user.email:
        user = crud.get_user_by_email(session=session, email=cast(str, user_in.email))
        if user:
            user_in.email = current_user.email
            message = "A user with this email already exists in the system"
    updated_user = crud.update_user(session=session, db_user=current_user, user_in=user_in)
    public_user = UserPublic(
        id=updated_user.id,
        name=updated_user.name,
        email=updated_user.email,
        role=updated_user.role,
    )
    return { "data": public_user, "message": message }

@router.delete("/me")
async def delete_user_me(session: SessionDep, current_user: CurrentUser):
    crud.delete_user_by_id(session=session, user_id=current_user.id)
    return { "message": "Successfully deleted user"}

@router.get("/{user_id}",
    dependencies=[Depends(get_user_is_admin_user)],
    response_model=UserPublic)
async def read_user(user_id: int, session: SessionDep):
    return crud.get_user_by_id(session=session, user_id=user_id)

@router.patch(
"/{user_id}",
      dependencies=[Depends(get_user_is_admin_user)])
async def update_user(user_id: int, session: SessionDep, user_in: UserUpdate):
    message = "Successfully updated user information"
    db_user = crud.get_user_by_id(session=session, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    if user_in.email is not None and user_in.email != db_user.email:
        user = crud.get_user_by_email(session=session, email=cast(str, user_in.email))
        if user:
            user_in.email = cast(str, db_user.email)
            message = "A user with this email already exists in the system"
    updated_user = crud.update_user(session=session, db_user=db_user, user_in=user_in)
    public_user = UserPublic(
        id=updated_user.id,
        name=updated_user.name,
        email=updated_user.email,
        role=updated_user.role,
    )
    return {"data": public_user, "message": message }

@router.delete("/{user_id}",
    dependencies=[Depends(get_user_is_admin_user)])
async def delete_user(user_id: int, session: SessionDep):
    user = crud.get_user_by_id(session=session, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    crud.delete_user_by_id(session=session, user_id=user_id)
    return { "message": "Successfully deleted user" }