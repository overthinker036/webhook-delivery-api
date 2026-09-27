from fastapi import APIRouter, status, Query, Depends
import models
from db_conn import get_db_session
from sqlalchemy.ext.asyncio import AsyncSession
import db_models
from sqlalchemy import select


router = APIRouter(
    prefix="/deliveries",
    tags=["Deliveries"]
)


#GET /deliveries: Filter/paginate delivery history
@router.get("", response_model=list[models.Delivery])
async def get_all_deliveries(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=50),
    delivery_status: models.DeliveryStatus | None = Query(default=None),
    db: AsyncSession = Depends(get_db_session)):
    
    query = select(db_models.Delivery)

    if delivery_status is not None:
        query = query.where(db_models.Delivery.status == delivery_status)

    query = query.order_by(db_models.Delivery.d_id).offset(skip).limit(limit)
     
    result = await db.execute(query)

    return result.scalars().all() 



#POST /deliveries/{id}/retry: Manually retry a failed delivery
@router.post("/{d_id}/retry")
async def retry_a_delivery(e_id: int, db: AsyncSession = Depends(get_db_session)):
    pass

