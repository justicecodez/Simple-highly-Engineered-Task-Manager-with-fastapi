from pydantic import BaseModel, Field, EmailStr, field_validator, model_validator
import re

class login_schema_request(BaseModel):

    username:str=Field(
        min_length=3,
        max_digits=30,
    ),

    password:str=Field(
        min_length=8,
        max_length=30,
    )

    @field_validator("username") #field validator is used to validate a single field, 
    @classmethod
    def validate_username(cls, value: str) -> str:
        value = value.lower()

        if not re.fullmatch(r"[a-z0-9_]+", value):
            raise ValueError(
                "Username can only contain letters, numbers and underscores"
            )

        return value

class register_schema_request(BaseModel):
    email:EmailStr
    name:str=Field(
        min_length=3,
        max_length=30
    )
    username:str=Field(
        min_length=3,
        max_length=30,
    )
    password:str=Field(
        min_length=8,
        max_length=30,
    )
    confirm_password:str=Field(
        min_length=8,
        max_length=30,
    )

    @model_validator(mode='after') #while model_validator is used to validate the entire model.
    def password_match(cls, self):
        if self.password!=self.confirm_password:
            raise ValueError("Password do not match")
        return self

    @field_validator("username")
    @classmethod
    def validate_username(cls, value: str) -> str:
        value = value.lower()

        if not re.fullmatch(r"[a-z0-9_]+", value):
            raise ValueError(
                "Username can only contain letters, numbers and underscores"
            )

        return value

class refresh_token_schema_request(BaseModel):
    refresh_token:str

class access_token_schema_response(BaseModel):
    access_token: str
    token_type: str = "bearer"

class auth_schema_response(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"