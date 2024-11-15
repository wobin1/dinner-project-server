from fastapi import APIRouter, FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from .utils import Utility
from .service import AuthService
from modules.users.schemas import GetUsersModel
from modules.users.utils import Utility as user_utils
from modules.shared.response import Response



auth_router = APIRouter(
    prefix="/auth",
    tags= ["Authentication"]
)

utility = Utility()
user_utility = user_utils()
service = AuthService()
response = Response()



@auth_router.post("/login")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = service.authenticate_user(form_data.username, form_data.password)
    user
    print('user email', user)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = utility.create_access_token({'sub': user.email})
    user_data = {}
    user_data['id'] = user.id
    user_data['email'] = user.email
    user_data['is_active'] = user.is_active
    user_data['is_church'] = user.is_church
    user_data['is_bouncer'] = user.is_bouncer
    user_data['is_admin'] = user.is_admin

    token = {"access_token": access_token, "token_type": "bearer"}
    user_data['token'] = token

    return response.success(data = user_data)



@auth_router.get("/current-user", )
async def get_current_user():
    current_user = await service.get_current_active_user()
    return current_user


# @auth_router.post("/logout")
# async def logout(current_user: dict = Depends()):
#     print('current_user', current_user)