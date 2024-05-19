from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config.config import settings

# SQLALCHEMY_DATABASE_URL = 'postgresql://admin:admin@localhost:5432/fastapi'
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

# Create engine(sqlalchemy db engine) from database url
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# This helps to create session from engine
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base helps to create sqlalchemy "base" model using declarative_base
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
