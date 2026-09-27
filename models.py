from pydantic import BaseModel
from enum import Enum
from datetime import datetime
from typing import Any




#Events:
class EventCreate(BaseModel):
    e_type: str
    i_key: str
    payload: dict[str, Any]

class EventResponse(BaseModel):
    e_id: int
    i_key: str
    e_type: str
    payload: dict[str, Any]
    created_at: datetime





#Webhooks:
class WebhookCreate(BaseModel):
    address: str

class WebhookResponse(BaseModel):
    w_id: int
    address: str
    is_active: bool
    created_at: datetime





#Delivery:

class DeliveryStatus(str, Enum):
    QUEUED = "queued"
    DELIVERING = "delivering"
    SUCCESS = "success"
    FAILED = "failed"


class Delivery(BaseModel):
    d_id: int
    e_id: int
    w_id: int
    status: DeliveryStatus
    attempts: int
    last_status_code: int | None
    error: str | None
    next_retry_at: datetime | None
    created_at: datetime
