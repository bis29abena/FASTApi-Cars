from sqlmodel import SQLModel
from db import engine
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.cars import CarRouter
from routers.web import WebRouter
from routers.user import UserRouter

from contextlib import asynccontextmanager

import uvicorn


@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield


# instantiate the routers
car_router = CarRouter()
web_router = WebRouter()
user_router = UserRouter()

app = FastAPI(lifespan=lifespan)

# add your routers to the app
app.include_router(car_router)
app.include_router(web_router)
app.include_router(user_router)

# set cors middle wear
origins = [
    "http://localhost:8000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)




if __name__ == "__main__":
    uvicorn.run("carsharing:app", reload=True)
