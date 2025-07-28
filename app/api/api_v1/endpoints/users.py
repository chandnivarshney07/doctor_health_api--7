from fastapi import APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder

from app.schemas.user import UserCreate, UserLogin, UserOut
from app.crud.user import create_user, get_user_by_email
from app.core.security import verify_password
from app.core.auth import create_access_token
from datetime import timedelta
from app.core.config import settings


router = APIRouter()

@router.post("/register")
async def register(user: UserCreate):
    existing = await get_user_by_email(user.email)
    if existing:
        raise HTTPException(status_code=400, detail="User already exists")

    new_user = await create_user(user)

    return {
        "message": "User registered successfully",
        "user": jsonable_encoder(new_user)
    }


@router.post("/login")
async def login(user: UserLogin):
    db_user = await get_user_by_email(user.email)
    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid email or password")

    if not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid email or password")

        # Generate access token
    access_token = create_access_token(
        data={"sub": db_user.email},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    

    # If db_user is a Pydantic/BaseModel or ODM model, use `.dict()` or `.model_dump()`
    user_dict = db_user.dict() if hasattr(db_user, "dict") else db_user

    # user_out = UserOut.model_validate(user_dict)
    user_out = UserOut.model_validate(jsonable_encoder(db_user))
    return {
        "message": "Login successful",
        "access_token": access_token,
        "token_type": "bearer",
        "user": user_out.model_dump(by_alias=True)
    }
