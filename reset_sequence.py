import asyncio
from app.core.database import SessionLocal
from sqlalchemy import text

async def fix_sequence():
    async with SessionLocal() as db:
        result = await db.execute(text("SELECT MAX(id) FROM users"))
        max_id = result.scalar()

        await db.execute(text(f"SELECT setval('users_id_seq', {max_id})"))
        await db.commit()

        print(f"Max existing ID  : {max_id}")
        print(f"Sequence reset to: {max_id}")
        print(f"Next insert ID   : {max_id + 1}")

asyncio.run(fix_sequence())