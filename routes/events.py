from fastapi import APIRouter, status, Depends, HTTPException
import models
from sqlalchemy.ext.asyncio import AsyncSession
from db_conn import get_db_session
import db_models
from sqlalchemy import select

router = APIRouter(
    prefix="/events",
    tags=["Events"]
)

# example event: {
#     "type": "user.created",
#     "payload": {
#         "user_id": 17,
#         "name": "John Doe"
#     }
# }



#GET /events/{e_id}/deliveries: See every delivery attempt for an event
@router.get("/{e_id}/deliveries")
async def all_delivery_attemps_for_an_event(e_id: int, db: AsyncSession = Depends(get_db_session)):
    deliv_results = await db.execute(select(db_models.Delivery).where(db_models.Delivery.e_id == e_id))
    deliveries = deliv_results.scalars().all()

    if not deliveries:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No delivery for event {e_id} found!")

    return deliveries



#POST /events: Submit an event, return 202 + event_id
@router.post("", status_code=status.HTTP_202_ACCEPTED)
async def user_posted_an_event(event: models.EventCreate, db: AsyncSession = Depends(get_db_session)):
    pass



