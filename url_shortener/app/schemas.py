from pydantic import BaseModel, HttpUrl
from datetime import datetime

class URLBase(BaseModel):
    original_url: str

class URLCreate(URLBase):
    pass

class URLInfo(URLBase):
    short_code: str
    clicks: int
    created_at: datetime

    class Config:
        from_attributes = True
