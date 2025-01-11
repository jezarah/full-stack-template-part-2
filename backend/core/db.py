from sqlmodel import Session, create_engine, select

from crud.user import create_user
from core.config import settings
from model.models import User
from schema.user import UserCreate


engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))

# make sure all SQLModel models are imported (app.models) before initializing DB
# otherwise, SQLModel might fail to initialize relationships properly
# for more details: https://github.com/fastapi/full-stack-fastapi-template/issues/28


def init_db(session: Session) -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next lines
    # from sqlmodel import SQLModel

    # This works because the models are already imported and registered from app.models
    # SQLModel.metadata.create_all(engine)

    user = session.exec(
        select(User).where(User.email == settings.FIRST_ADMIN_EMAIL)
    ).first()
    if not user:
        user_in = UserCreate(
            email=settings.FIRST_ADMIN_EMAIL,
            name=settings.FIRST_ADMIN_NAME,
            password=settings.FIRST_ADMIN_PASSWORD,
            role=1,
            access_token=None
        )
        user = create_user(session=session, user_create=user_in)