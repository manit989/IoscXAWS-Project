import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from app.model.models import (
    Base, Student, StudentClassification, CategoryEnum, 
    ParentDetails, AcademicRecords, FinancialInfo,
    Documents, NocRecords, Placement, AcademicDocuments,
    Internship, ResearchPaper
)
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

async def create_test_student():
    engine = create_async_engine(DATABASE_URL, echo=False)
    async_session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with async_session_maker() as session:
        # Check if student exists
        from sqlalchemy.future import select
        result = await session.execute(select(Student).where(Student.roll_number == "TEST001"))
        existing = result.scalar_one_or_none()
        
        if existing:
            print("Student TEST001 already exists!")
            return
            
        student = Student(
            roll_number="TEST001",
            name="John Doe",
            branch="Computer Science",
            year=3,
            email="johndoe@example.com",
            mobile="9876543210",
            address="123 Test Ave, Demo City"
        )
        session.add(student)
        await session.commit()
        
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
        
        parent = ParentDetails(
            student_id="TEST001",
            parent_name="Richard Doe",
            profession="Engineer",
            contact_number="9876543211",
            email="richard.doe@example.com"
        )
        
        academic = AcademicRecords(
            student_id="TEST001",
            sem1_cgpa=8.5, sem1_backlogs=0,
            sem2_cgpa=8.8, sem2_backlogs=0,
            sem3_cgpa=9.1, sem3_backlogs=0,
            sem4_cgpa=8.9, sem4_backlogs=0,
            attendance_status="Good"
        )
        
        internship = Internship(
            student_id="TEST001",
            company_name="Tech Corp",
            role="Software Engineer Intern",
            duration="3 months",
            stipend="15000"
        )

        session.add_all([classification, parent, academic, internship])
        await session.commit()
        print("Successfully created test student TEST001 with full profile data!")
        
    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(create_test_student())
