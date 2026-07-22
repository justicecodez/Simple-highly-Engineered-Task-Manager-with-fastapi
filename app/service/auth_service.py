from fastapi import Depends, HTTPException, status
from app.model import user
from app.schema.auth_schema import register_schema_request, login_schema_request, auth_schema_response, access_token_schema_response, refresh_token_schema_request
from app.schema.user_schema import UserSchema
from app.utils.password_helper import password_helper
from app.repository.app_repository import DBRepository
from app.utils.db_dependency import get_db_repository
from app.model.user import User
from app.utils.jwt_helper import create_access_token, create_refresh_token, get_current_user_from_token, verify_refresh_token
from app.model.refresh_jwt_token import RefreshTokenRequest

async def register_service(data:register_schema_request, repo:DBRepository= Depends(get_db_repository))->auth_schema_response:
    check_username=repo.check_if_value_exist(User, User.username, data.username)
    check_email=repo.check_if_value_exist(User, User.email, data.email)
    if(check_email):
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail="Email already exist")
    if(check_username):
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail="Username already exist")
    password_util=password_helper()
    data.password=password_util.hash_helper(data.password)

    new_user_entry=User(
        email=data.email,
        name=data.name,
        username=data.username,
        password=data.password
    )
    create_new_user=repo.create_record(new_user_entry) 
    refresh_token, expire_at=create_refresh_token({
            "user_id":create_new_user.id,
    }) 
    new_refresh_token_entry=RefreshTokenRequest(
        user_id=new_user_entry.id,
        token_hash=refresh_token,
        expires_at=expire_at
    )
    create_refresh_token_record=repo.create_record(new_refresh_token_entry)
    access_token=create_access_token({
            "user_id":create_new_user.id,
    })
    
    return auth_schema_response(
        token_type="Bearer",
        access_token=access_token,
        refresh_token=refresh_token
    )
    
async def login_service(data:login_schema_request, repo:DBRepository= Depends(get_db_repository))->auth_schema_response:

    user=repo.get_record_by_value(User, User.email, data.email)
    if not user:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail="Invalid Email or password")
    password_util=password_helper()
    if not password_util.verify_hash_helper(data.password, user.password):
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail="Invalid Email or password")
    access_token=create_access_token({
            "user_id":user.id,
    })
    refresh_token, expires_at=create_refresh_token({
            "user_id":user.id,
    })
    new_refresh_token_entry=RefreshTokenRequest(
        user_id=user.id,
        token_hash=refresh_token,
        expires_at=expires_at
    )
    create_refresh_token=repo.create_record(new_refresh_token_entry)
    return auth_schema_response(
        token_type="Bearer",
        access_token=access_token,
        refresh_token=refresh_token
    )

async def get_current_user_service(user_id:str=Depends(get_current_user_from_token), repo:DBRepository= Depends(get_db_repository))->UserSchema:
    user=repo.get_record_by_value(User, User.id, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

async def refresh_token_service(data:refresh_token_schema_request, repo:DBRepository= Depends(get_db_repository))->access_token_schema_response:
    payload=verify_refresh_token(data.refresh_token)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
    password_util=password_helper()
    user_session=repo.get_record_by_value(RefreshTokenRequest, RefreshTokenRequest.user_id, payload.get("user_id"))
    if not user_session:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
    hashed_refresh_token=user_session.token_hash
    if not password_util.verify_hash_helper(data.refresh_token, hashed_refresh_token):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
    access_token=create_access_token({
            "user_id":payload.get("user_id"),
    })
    return access_token_schema_response(
        access_token=access_token,
        token_type="Bearer"
    )









