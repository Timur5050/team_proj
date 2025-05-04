from datetime import datetime
from decimal import Decimal
from enum import Enum

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, DECIMAL
from sqlalchemy import Enum as SqlEnum
from sqlalchemy.orm import relationship
from database import Base

class AnimalGender(str, Enum):
    FEMALE = "female"
    MALE = "male"

class AnimalStatus(str, Enum):
    AVAILABLE = "available"
    ADOPTED = "adopted"


class Animal(Base):
    __tablename__ = "animals"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(SqlEnum(AnimalGender))
    description = Column(String, nullable=True)
    shelter_id = Column(Integer, ForeignKey("shelters.id", ondelete="CASCADE"))
    breed = Column(String(100), nullable=False)
    character_traits = Column(String(100), nullable=False)
    weight = Column(DECIMAL, nullable=False)
    height = Column(DECIMAL, nullable=False)
    status = Column(SqlEnum(AnimalStatus))
    shelter = relationship("Shelter", back_populates="animals", passive_deletes=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "age": self.age,
            "gender": self.gender,
            "description": self.description,
            "shelter_id": self.shelter_id,
            "breed": self.breed,
            "character_traits": self.character_traits,
            "weight": str(self.weight),
            "height": str(self.height),
            "status": self.status
        }

