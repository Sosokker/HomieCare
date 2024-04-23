"""
Database Configuration and Connection Setup

This file contains the configuration and setup for connecting to the database using SQLAlchemy and MinIO.

Attributes:
    engine: SQLAlchemy engine for database connection.
    SessionLocal: SQLAlchemy session maker for database sessions.
    Base: SQLAlchemy base class for declarative ORM models.
    minio_client: MinIO client for interacting with MinIO storage.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from minio import Minio
from config import DB_HOST, DB_USER, DB_PASSWD, DB_NAME, MINIO_ENDPOINT, MINIO_ACCESS_KEY, MINIO_SECRET_KEY

engine = create_engine(f"mysql+pymysql://{DB_USER}:{DB_PASSWD}@{DB_HOST}/{DB_NAME}")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

USE_SSL = False
minio_client = Minio(
    endpoint=MINIO_ENDPOINT,
    access_key=MINIO_ACCESS_KEY,
    secret_key=MINIO_SECRET_KEY,
    secure=USE_SSL
)