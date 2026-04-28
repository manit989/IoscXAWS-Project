from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from app.core.database import get_db
from app.services.otp_services import send_otp, verify_otp
from app.services.authHelper import create_access_token, get_password_hash
from app.model.models import DBUser, RoleEnum
from datetime import timedelta

router = APIRouter(
    prefix="/auth/register",
    tags=["Registration"]
)

class SendOTPRequest(BaseModel):
    enrollment_number: str
    email: str

class VerifyOTPRequest(BaseModel):
    enrollment_number: str
    email: str
    otp: str

@router.post("/send-otp")
async def send_otp_route(request: SendOTPRequest, db: AsyncSession = Depends(get_db)):
    if not request.email.endswith("@std.ggsipu.ac.in"):
        raise HTTPException(status_code=400, detail="Email must end with @std.ggsipu.ac.in")

    if not request.enrollment_number.strip():
        raise HTTPException(status_code=400, detail="Enrollment number is required")

    from sqlalchemy.future import select
    existing = await db.execute(
        select(DBUser).where(DBUser.username == request.enrollment_number)
    )
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Account already exists for this enrollment number")

    try:
        await send_otp(db, request.enrollment_number, request.email)
        return {"message": "OTP sent successfully"}
    except ValueError as e:
        # Rate limit errors get 429, others get 400
        msg = str(e)
        status = 429 if "Too many" in msg else 400
        raise HTTPException(status_code=status, detail=msg)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/verify-otp")
async def verify_otp_route(request: VerifyOTPRequest, db: AsyncSession = Depends(get_db)):
    if not request.email.endswith("@std.ggsipu.ac.in"):
        raise HTTPException(status_code=400, detail="Email must end with @std.ggsipu.ac.in")

    try:
        await verify_otp(db, request.enrollment_number, request.email, request.otp)
    except ValueError as e:
        msg = str(e)
        status = 429 if "Too many" in msg else 400
        raise HTTPException(status_code=status, detail=msg)

    # create user account
    hashed_pw = await get_password_hash(request.enrollment_number)
    new_user = DBUser(
        username=request.enrollment_number,
        role=RoleEnum.student,
        password_hash=hashed_pw
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    # return token with must_change_password flag
    token = create_access_token(
        data={"sub": str(new_user.id)},
        expires_delta=timedelta(minutes=30)
    )
    return {
        "access_token": token,
        "token_type": "bearer",
        "must_change_password": True,
        "role": "student"
    }