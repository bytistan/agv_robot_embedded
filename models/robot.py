from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from . import Base

class Robot(Base):
    __tablename__ = "robot"
    
    id = Column(Integer, primary_key=True)
    serial_number = Column(String, nullable=False)
    secret_key = Column(String, nullable=False)
    mode = Column(Integer, nullable=False)
    synchronized = Column(Boolean,default=False)

    created_date = Column(DateTime, default=datetime.utcnow)

    mission = relationship("Mission", back_populates="robot")
    qr_code = relationship("QRCode", back_populates="robot")
    settings = relationship("Settings", back_populates="robot")
    connection = relationship("Connection", back_populates="robot")
