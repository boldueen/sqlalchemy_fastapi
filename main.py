import asyncio
import uvicorn
from fastapi import FastAPI
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError

from db import service
from db.models.base import get_session
from db.models.base import init_models


from exceptions.user_exceptions import DuplicatedEntryError

app = FastAPI()


class UserSchema(BaseModel):
    name: str


@app.on_event("startup")
def init_models_on_startup():
    asyncio.gather(init_models())


@app.get("/users", response_model=list[UserSchema])
async def get_biggest_cities(session: AsyncSession = Depends(get_session)):
    cities = await service.get_users(session)
    return [UserSchema(name=c.name) for c in cities]


@app.post("/suka")
async def add_users(user: UserSchema, session: AsyncSession = Depends(get_session)):
    created_user = service.add_users(session, user.name)
    try:
        await session.commit()
        return created_user
    except IntegrityError as ex:
        await session.rollback()
        raise DuplicatedEntryError("The user is already stored")


if __name__ == '__main__':
    uvicorn.run(app=app, host='0.0.0.0', port=8001)
