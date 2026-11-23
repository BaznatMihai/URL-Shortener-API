from datetime import datetime

from pydantic import BaseModel, HttpUrl, EmailStr, ConfigDict

class URLCreate (BaseModel):
    original_url: HttpUrl

class URLResponse(BaseModel):
    id: int
    original_url: str
    short_url: str

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr

class UserLogin(BaseModel):
    username: str
    password: str

class URLListResponse(BaseModel):
    id: int
    original_url: str
    short_code: str
    user_id: int | None
    model_config = ConfigDict(from_attributes=True)

class URLStatsResponse(BaseModel):
    short_code: str
    original_url: str
    click_count: int
    created_at: datetime
    model_config= ConfigDict(from_attributes=True)