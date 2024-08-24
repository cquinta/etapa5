import os
from fastapi import FastAPI
from sqlmodel import Field, Session, SQLModel, create_engine, select
from config import settings


class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    secret_name: str
    age: int | None = Field(default=None, index=True)


engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/")
async def root():
    return{"message","hello-world"}

@app.get("/host")
async def gethost():
    message = dict()
    message['hostname'] = os.environ.get('HOSTNAME')
    return {"message": message}

@app.get("/variaveis")
async def variaveis():
    variaveis = dict()
    variaveis['version'] = os.environ.get('APP_VERSION')
    variaveis['token']=os.environ.get('TOKEN')
    variaveis['bancodev']=os.environ.get('BANCODEV')
   # variaveis['CONFIG'] = open('/app/config-dev.yaml', "r").read()
    return {"variaveis": variaveis}


@app.post("/heroes/")
def create_hero(hero: Hero):
    with Session(engine) as session:
        session.add(hero)
        session.commit()
        session.refresh(hero)
        return hero


@app.get("/heroes/")
def read_heroes():
    with Session(engine) as session:
        heroes = session.exec(select(Hero)).all()
        return heroes
