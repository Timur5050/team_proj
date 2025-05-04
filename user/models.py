from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, unique=True, index=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    date_joined = Column(DateTime, default=datetime.now)
    is_superuser = Column(Boolean, default=False)
    password = Column(String)