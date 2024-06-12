from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean ,Float
from sqlalchemy.orm import relationship
from datetime import datetime
from . import Base

class Location(Base):
    __tablename__ = "location"
    
    id = Column(Integer, primary_key=True)
    mission_id = Column(Integer, ForeignKey("mission.id"))
    distance_traveled = Column(Float, nullable=False)
    direction_traveled = Column(Integer, nullable=False)
    synchronized = Column(Boolean,default=False)

    created_date = Column(DateTime, default=datetime.utcnow)

    mission = relationship("Mission", back_populates="location")
