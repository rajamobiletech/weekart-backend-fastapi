from fastapi import FastAPI
from app.db.database import SessionLocal, engine
from app.db import models
from app.routers import product, user, auth, vote
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()


# This line helps to create database schema
# models.Base.metadata.create_all(bind=engine)

origins = [
	"*"
]

app.add_middleware(
	CORSMiddleware,
	allow_origins=origins,
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)



app.include_router(product.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

