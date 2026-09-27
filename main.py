from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks, Query, status, Response
from contextlib import asynccontextmanager
from db_conn import async_engine, AsyncSessionLocal
import db_models
import models
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from routes import (deliveries, events, subscriptions)




@asynccontextmanager
async def lifespan(app: FastAPI):
    async with async_engine.begin() as conn:
        await conn.run_sync(
            db_models.Base.metadata.create_all
        )
        yield
        await async_engine.dispose()




app = FastAPI(lifespan=lifespan, title="Webhook Delivery API")

app.include_router(subscriptions.router)
app.include_router(events.router)
app.include_router(deliveries.router)




