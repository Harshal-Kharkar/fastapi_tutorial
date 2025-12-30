from fastapi import APIRouter
from pydantic import BaseModel
import requests
from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select


Router = APIRouter(prefix="/database",tags=["database"])

class HeroBase(SQLModel):
    name: str
    age: int | None = None
    secret_name: str

class Hero(HeroBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    

# Code above omitted 👆

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)

# Code below omitted 👇

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
    # clear_db()
    # print("clearing database")
    print("commented the clear data")
    
@Router.post("/heroes/", response_model=Hero)
def create_hero(hero: HeroBase, session: SessionDep) -> Hero:
    db_hero = Hero.model_validate(hero)   # Convert HeroBase → Hero
    session.add(db_hero)
    session.commit()
    session.refresh(db_hero)
    return db_hero



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