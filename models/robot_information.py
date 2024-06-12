from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean ,Float
from sqlalchemy.orm import relationship
from datetime import datetime
from . import Base

class RobotInformation(Base):
    __tablename__ = "robot_information"
    
    id = Column(Integer, primary_key=True)

    qr_code_id = Column(Integer, ForeignKey("qr_code.id"))
    mission_id = Column(Integer, ForeignKey("mission.id"))

    speed = Column(Integer,nullable=False)
    load = Column(Float, nullable=False)
    temperature = Column(Float, nullable=False)
    battery_level = Column(Integer, nullable=False)

    synchronized = Column(Boolean,default=False)

    created_date = Column(DateTime, default=datetime.utcnow)

    qr_code = relationship("QRCode", back_populates="robot_information")
    mission = relationship("Mission", back_populates="robot_information")
