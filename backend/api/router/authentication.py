from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from core.config import settings
from core.security import create_access_token
from crud.user import authenticate
from schema.jwt import Token
from api.deps import SessionDep

router = APIRouter(prefix="/authentication", tags=["authentication"])

@router.post("/access-token", response_model=Token)
def login_access_token(session: SessionDep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = authenticate(
        session=session, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=420, detail="Incorrect email or password")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return Token(access_token=create_access_token(user.id, expires_delta=access_token_expires))