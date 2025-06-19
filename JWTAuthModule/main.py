from fastapi import FastAPI
from database import database, metadata
from api import routes
from sqlalchemy import create_engine
from constants import DATABASE_URL


app = FastAPI()

app.include_router(routes.router)


engine = create_engine(DATABASE_URL)
metadata.create_all(engine)


@app.on_event("startup")
async def startup():
    await database.connect()
    
@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
    


