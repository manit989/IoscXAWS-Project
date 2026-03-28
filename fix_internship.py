import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.future import select
from app.model.models import Base, Internship, InternshipTypeEnum
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

async def fix_internship():
    engine = create_async_engine(DATABASE_URL, echo=False)
    async_session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with async_session_maker() as session:
        result = await session.execute(select(Internship).where(Internship.student_id == "TEST001"))
        if not result.scalar_one_or_none():
            internship = Internship(
                student_id="TEST001",
                internship_type=InternshipTypeEnum.Private,
                company_name="Tech Corp",
                duration="3 months",
                has_stipend=True,
                stipend_amount=15000.00
            )
            session.add(internship)
            await session.commit()
            print("Added internship to TEST001")
        
    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(fix_internship())
