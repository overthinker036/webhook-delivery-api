from fastapi import APIRouter, status, Query, Depends, Response, HTTPException
import models
from db_conn import get_db_session
from sqlalchemy.ext.asyncio import AsyncSession
import db_models
from sqlalchemy import select


router = APIRouter(
    prefix="/subscriptions",
    tags=["Subscriptions"]
)


#GET /subscriptions: List registered webhooks
@router.get("", response_model=list[models.WebhookResponse])
async def list_registered_webhooks(
        skip: int = Query(default=0, ge=0), 
        limit: int = Query(default=10, ge=1, le=50), 
        db: AsyncSession = Depends(get_db_session)
    ):

    statement = (
        select(db_models.Webhook)
        .order_by(db_models.Webhook.w_id)
        .offset(skip)
        .limit(limit)
        )

    result = await db.scalars(statement)
    return result.all()



#POST /subscriptions: Register a webhook URL
@router.post("", status_code=status.HTTP_201_CREATED, response_model=models.WebhookResponse)
async def register_a_webhook_url(data: models.WebhookCreate, db: AsyncSession = Depends(get_db_session)):

    webhook = db_models.Webhook(address=data.address)

    db.add(webhook)
    await db.commit()
    await db.refresh(webhook)
    
    return webhook



#DELETE /subscriptions/{id}: Remove one
@router.delete("/{id}")
async def delete_a_webhook(id: int, db: AsyncSession = Depends(get_db_session)):
    webhook = await db.scalar(select(db_models.Webhook).where(db_models.Webhook.w_id == id))
    
    if webhook is None:
        raise HTTPException(404, f"Subscription {id} not found")

    await db.delete(webhook)
    await db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)





