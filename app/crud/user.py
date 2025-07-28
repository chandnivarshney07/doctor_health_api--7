from datetime import datetime, date, time
from app.schemas.user import UserCreate
from app.models.user import UserModel 
from app.database.mongodb import db
from app.core.security import get_password_hash

async def create_user(user: UserCreate) -> UserModel:
    hashed_pw = get_password_hash(user.password)
    
    user_dict = user.dict()
    user_dict["hashed_password"] = hashed_pw
    del user_dict["password"]

    # Convert dob from date to datetime if needed
    dob_value = user_dict.get("dob")
    if isinstance(dob_value, date) and not isinstance(dob_value, datetime):
        user_dict["dob"] = datetime.combine(dob_value, time.min)

    result = await db.users.insert_one(user_dict)
    user_dict["_id"] = str(result.inserted_id)

    return UserModel(**user_dict)

async def get_user_by_email(email: str) -> UserModel | None:
    user = await db.users.find_one({"email": email})
    if user:
        user["_id"] = str(user["_id"])
        return UserModel(**user)
    return None
