from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Float, Integer, String
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from db.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    hashed_refresh_token = Column(String, nullable=True)