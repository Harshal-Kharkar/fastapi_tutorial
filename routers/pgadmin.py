from fastapi import APIRouter
from pydantic import BaseModel
from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select

Router = APIRouter(prefix="/pgadmin", tags=["pgadmin"])

class Hero(SQLModel, table=True,):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    age: int | None = Field(default=None, index=True)
    secret_name: str

    __table_args__ = {'extend_existing': True} # This is where it's applied

# PostgreSQL connection setup
postgresql_url = "postgresql://username:password@localhost:5432/heroes_db"
engine = create_engine(postgresql_url,)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def clear_db():
    SQLModel.metadata.drop_all(engine)
    print("Database cleared!")

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

@Router.on_event("startup")
def on_startup():
    print("creating database connection ")
    create_db_and_tables()

@Router.on_event("shutdown")
def shutdown_event():
    print("commented the clear data")

@Router.post("/heroes/")
def create_hero(hero: Hero, session: SessionDep) -> Hero:
    session.add(hero)
    session.commit()
    session.refresh(hero)
    return hero

@Router.get("/heroes/")
def read_heroes(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[Hero]:
    heroes = session.exec(select(Hero).offset(offset).limit(limit)).all()
    return heroes

@Router.get("/heroes/{hero_id}")
def read_hero(hero_id: int, session: SessionDep) -> Hero:
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    return hero

@Router.delete("/heroes/{hero_id}")
def delete_hero(hero_id: int, session: SessionDep):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    session.delete(hero)
    session.commit()
    return {"ok": True}
