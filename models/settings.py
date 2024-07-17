from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean ,Float
from sqlalchemy.orm import relationship
from datetime import datetime
from .base_model import BaseModel 

class Settings(BaseModel):
    __tablename__ = "settings"
    
    id = Column(Integer, primary_key=True)

    robot_id = Column(Integer, ForeignKey("robot.id"))

    speed = Column(Integer,nullable=False)

    synchronized = Column(Boolean,default=False)

    updated_date = Column(DateTime, default=datetime.utcnow)

    robot = relationship("Robot", back_populates="settings")
