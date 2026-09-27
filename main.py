from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks, Query, status, Response
from contextlib import asynccontextmanager
from db_conn import async_engine, AsyncSessionLocal
import db_models
import models
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select




@asynccontextmanager
async def lifespan(app: FastAPI):
    async with async_engine.begin() as conn:
        await conn.run_sync(
            db_models.Base.metadata.create_all
        )
        yield
        await async_engine.dispose()




app = FastAPI(lifespan=lifespan, title="Webhook Delivery API")




async def get_db_session():
    db = AsyncSessionLocal()
    try:
        yield db
    finally:
        await db.close()





#POST /subscriptions: Register a webhook URL
@app.post("/subscriptions", status_code=status.HTTP_201_CREATED, response_model=models.WebhookResponse)
async def register_a_webhook_url(data: models.WebhookCreate, db: AsyncSession = Depends(get_db_session)):

    webhook = db_models.Webhook(address=data.address)

    db.add(webhook)
    await db.commit()
    await db.refresh(webhook)
    
    return webhook





#GET /subscriptions: List registered webhooks
@app.get("/subscriptions", response_model=list[models.WebhookResponse])
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






#DELETE /subscriptions/{id}: Remove one
@app.delete("/subscriptions/{id}")
async def delete_a_webhook(id: int, db: AsyncSession = Depends(get_db_session)):
    webhook = await db.scalar(select(db_models.Webhook).where(db_models.Webhook.w_id == id))
    
    if webhook is None:
        raise HTTPException(404, f"Subscription {id} not found")

    await db.delete(webhook)
    await db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)





#POST /events: Submit an event, return 202 + event_id
@app.post("/events", status_code=202)
async def user_posted_an_event(db: AsyncSession = Depends(get_db_session)):
    pass






#GET /events/{e_id}/deliveries: See every delivery attempt for an event
@app.get("/events/{e_id}/deliveries")
async def all_delivery_attemps_for_an_event(e_id: int, db: AsyncSession = Depends(get_db_session)):
    pass





#GET /deliveries: Filter/paginate delivery history
@app.get("/deliveries")
async def get_all_deliveries(db: AsyncSession = Depends(get_db_session)):
    pass






#POST /deliveries/{id}/retry: Manually retry a failed delivery
@app.post("/deliveries/{d_id}/retry")
async def retry_a_delivery(e_id: int, db: AsyncSession = Depends(get_db_session)):
    pass








# example event: {
#     "type": "user.created",
#     "payload": {
#         "user_id": 17,
#         "name": "John Doe"
#     }
# }



