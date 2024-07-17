from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean ,Float
from sqlalchemy.orm import relationship
from datetime import datetime
from .base_model import BaseModel 

class QRCode(BaseModel):
    __tablename__ = "qr_code"
    
    id = Column(Integer, primary_key=True)
    robot_id = Column(Integer, ForeignKey("robot.id"))

    vertical_coordinate = Column(Float, nullable=False)
    horizontal_coordinate = Column(Float, nullable=False)
    
    area_name = Column(String,nullable=True)

    synchronized = Column(Boolean,default=False)

    created_date = Column(DateTime, default=datetime.utcnow)

    robot = relationship("Robot", back_populates="qr_code")
    robot_information = relationship("RobotInformation", back_populates="qr_code")
    road_map = relationship("RoadMap", back_populates="qr_code")
