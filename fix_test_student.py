import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.future import select
from app.model.models import (
    Base, Student, StudentClassification, CategoryEnum, 
    ParentDetails, AcademicRecords, Internship
)
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

async def fix_test_student():
    engine = create_async_engine(DATABASE_URL, echo=False)
    async_session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with async_session_maker() as session:
        # Check if classification exists
        result = await session.execute(select(StudentClassification).where(StudentClassification.student_id == "TEST001"))
        if not result.scalar_one_or_none():
            classification = StudentClassification(
                student_id="TEST001",
                is_hosteller=True,
                category=CategoryEnum.General,
                sports_quota=False,
                is_disabled=False,
                is_single_child=False,
                ncc=True,
                nss=False
            )
            session.add(classification)
        
        result = await session.execute(select(ParentDetails).where(ParentDetails.student_id == "TEST001"))
        if not result.scalar_one_or_none():
            parent = ParentDetails(
                student_id="TEST001",
                parent_name="Richard Doe",
                profession="Engineer",
                contact_number="9876543211",
                email="richard.doe@example.com"
            )
            session.add(parent)
            
        result = await session.execute(select(AcademicRecords).where(AcademicRecords.student_id == "TEST001"))
        if not result.scalar_one_or_none():
            academic = AcademicRecords(
                student_id="TEST001",
                sem1_cgpa=8.5, sem1_backlogs=0,
                sem2_cgpa=8.8, sem2_backlogs=0,
                sem3_cgpa=9.1, sem3_backlogs=0,
                sem4_cgpa=8.9, sem4_backlogs=0,
                attendance_status="Good"
            )
            session.add(academic)
            
        await session.commit()
        print("Fixed TEST001 relationships")
        
    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(fix_test_student())
