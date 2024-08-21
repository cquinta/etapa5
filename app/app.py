import os
from fastapi import FastAPI
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello Carlos"}

@app.get("/variaveis")
async def variaveis():
    variaveis = dict()
    variaveis['version'] = os.environ.get('APP_VERSION')
    variaveis['token']=os.environ.get('TOKEN')
    return {"variaveis": variaveis}

