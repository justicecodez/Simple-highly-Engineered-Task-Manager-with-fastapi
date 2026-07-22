from fastapi import APIRouter, Depends
from fastapi_limiter.depends import RateLimiter

from app.schema.auth_schema import auth_schema_response, register_schema_request, login_schema_request, refresh_token_schema_request, access_token_schema_response
from app.service.auth_service import register_service, login_service, get_current_user_service, refresh_token_service
from app.schema.user_schema import UserSchema

router=APIRouter()

@router.post('/register', response_model=auth_schema_response, dependencies=[Depends(RateLimiter(times=5, seconds=60))])
async def register(data:register_schema_request, service=Depends(register_service))-> auth_schema_response:
    return  service

@router.post('/login', response_model=auth_schema_response, dependencies=[Depends(RateLimiter(times=5, seconds=60))])
async def login(data:login_schema_request, service =Depends(login_service))-> auth_schema_response:
    return  service

@router.post('/refresh/token', response_model=access_token_schema_response, dependencies=[Depends(RateLimiter(times=5, seconds=60))])
async def refresh_token(data:refresh_token_schema_request, service=Depends(refresh_token_service))-> access_token_schema_response:
    return  service

@router.get('/profile', response_model=UserSchema)
async def get_current_user(service=Depends(get_current_user_service))-> UserSchema:
    return  service