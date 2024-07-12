from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean ,Float
from sqlalchemy.orm import relationship
from datetime import datetime
from . import Base

class RoadMap(Base):
    __tablename__ = "road_map"
    
    id = Column(Integer, primary_key=True)
    mission_id = Column(Integer, ForeignKey("mission.id"))
    qr_code_id = Column(Integer, ForeignKey("qr_code.id"))

    active = Column(Boolean, default=False)
    reached = Column(Boolean, default=False)
    index = Column(Integer,nullable=True)

    synchronized = Column(Boolean,default=False)

    reached_time = Column(DateTime,nullable=True)
    created_date = Column(DateTime, default=datetime.utcnow)

    mission = relationship("Mission", back_populates="road_map")
    qr_code = relationship("QRCode", back_populates="road_map")

    @classmethod
    def from_dict(cls, data):
        return cls(**data)

