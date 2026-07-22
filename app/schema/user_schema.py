from pydantic import BaseModel, EmailStr, Field

class UserSchema(BaseModel):
    id: int
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=30)
    name: str = Field(..., min_length=3, max_length=30)

    class Config:
        orm_mode = True