from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from . import Base

class Mission(Base):
    __tablename__ = "mission"
    
    id = Column(Integer, primary_key=True)
    robot_id = Column(Integer, ForeignKey("robot.id"))

    completed = Column(Boolean, default=False)
    is_active = Column(Boolean, default=False)

    rank = Column(Integer, nullable=False,default=0)
    synchronized = Column(Boolean,default=False)

    end_time = Column(DateTime)
    created_date = Column(DateTime, default=datetime.utcnow)

    robot = relationship("Robot", back_populates="mission")
    location = relationship("Location", back_populates="mission")
    road_map = relationship("RoadMap", back_populates="mission")
    robot_information = relationship("RobotInformation", back_populates="mission")
