from pydantic import BaseModel, EmailStr, Field, constr
from datetime import date
from typing import Optional
from bson import ObjectId

# Phone number constraint
PhoneStr = constr(pattern=r'^\+?\d{10,15}$', min_length=10, max_length=15)

# MongoDB-compatible ObjectId field
class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return str(v)

# Request schema for registration
class UserCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    age: int = Field(..., gt=0, lt=120)
    dob: date
    phone_no: PhoneStr
    email: EmailStr
    password: str = Field(..., min_length=6)

# Response schema
class UserOut(BaseModel):
    id: str = Field(..., alias="_id")  # Use Mongo's _id as id
    name: str
    age: int
    dob: date
    phone_no: str
    email: EmailStr

    class Config:
        populate_by_name = True
        from_attributes = True  # Optional if you're validating from ORM/ODM objects

# Login schema
class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str  
    user: UserOut  
