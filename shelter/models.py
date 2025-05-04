from datetime import datetime
from enum import Enum

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy import Enum as SqlEnum
from sqlalchemy.orm import relationship
from database import Base

class ShelterStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


class Shelter(Base):
    __tablename__ = "shelters"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, unique=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    address = Column(String, nullable=True)
    description = Column(String, nullable=True)
    contacts = Column(String)
    status = Column(SqlEnum(ShelterStatus, default=ShelterStatus.PENDING))
    animals = relationship("Animal", back_populates="shelter", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "address": self.address,
            "contacts": self.contacts,
            "status": self.status,
            "user_id": self.user_id
        }