# postgredb_runfirst.py

from app.database import engine, Base
from app import models  # ✅ This import registers all tables
import asyncio

async def create_all():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅ All tables created successfully.")

asyncio.run(create_all())
