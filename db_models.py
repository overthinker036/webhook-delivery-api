from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, JSON, Enum, DateTime
from models import DeliveryStatus
from datetime import datetime




Base = declarative_base()





class Event(Base):
    __tablename__= "events"

    e_id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    i_key = Column(String, nullable=False, unique=True)
    e_type = Column(String, nullable=False)
    payload = Column(JSON, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    deliveries = relationship("Delivery", back_populates="event")







class Webhook(Base):
    __tablename__= "webhooks"

    w_id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    address = Column(String, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    deliveries = relationship("Delivery", back_populates="webhook")






class Delivery(Base):
    __tablename__= "deliveries"

    d_id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    e_id = Column(Integer, ForeignKey("events.e_id"), nullable=False)
    w_id = Column(Integer, ForeignKey("webhooks.w_id"), nullable=False)
    status = Column(Enum(DeliveryStatus), nullable=False, default=DeliveryStatus.QUEUED)
    attempts = Column(Integer, nullable=False, default=0)
    last_status_code = Column(Integer, nullable=True)   
    error = Column(String, nullable=True)
    next_retry_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    event = relationship("Event", back_populates="deliveries")
    webhook = relationship("Webhook", back_populates="deliveries")
