from fastapi import APIRouter, Depends
from modules.shared.models import User, session, Guest
from passlib.context import CryptContext
from .schemas import UserModel
from modules.shared.response import Response
from modules.shared.exception import Exceptions
from modules.auth.utils import Utility as auth_utils
from modules.auth.service import AuthService
from .utils import Utility

users_router = APIRouter(
    prefix=('/users'),
    tags=['Users']
)

pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")
response = Response()
exception = Exceptions()
utility = Utility()
auth_utility = auth_utils()
auth_service = AuthService()

@users_router.get('/')
def get_users():
    # print('current user:', current_user)
    users = session.query(User).all()
    
    data = utility.user_to_dict(users)

    return response.success(data=data)

@users_router.post('/')
def create_user(payload: UserModel):
    password_hash = auth_utility.hash_password(payload.password)

    user_exist = session.query(User).filter(User.email==payload.email).first()

    if user_exist:
        return exception.bad_request(message="user already exists")

    new_user = User(full_name = payload.full_name, email = payload.email, phone_number = payload.phone_number, password = password_hash, is_church = payload.is_church, is_bouncer = payload.is_bouncer,  is_admin = payload.is_admin)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    print(new_user)

    return response.success(data=new_user.id)

@users_router.get('/admin')
def get_admin():
    admin = session.query(User).filter(User.is_admin).all()

    data = utility.user_to_dict(admin)

    return response.success(data=data)

@users_router.get('/churches')
def get_churches():
    church = session.query(User).filter(User.is_church).all()

    data = utility.user_to_dict(church)

    return response.success(data=data)

@users_router.get('/bouncer')
def get_bouncers():
    bouncer = session.query(User).filter(User.is_bouncer).all()

    data = utility.user_to_dict(bouncer)

    return response.success(data=data)

@users_router.patch('/{user_id}')
def get_single_user(user_id):
    user = session.query(User).filter(User.id == user_id).first()
    user.is_admin = not user.is_admin
    session.commit()

    return response.success(data= "users type updated successfully")


@users_router.get('/{user_id}')
def get_user(user_id):
    user = session.query(User).filter(User.id == user_id).first()
    
    users_data = {}
    users_data['id'] = user.id
    users_data['full_name'] = user.full_name
    users_data['email'] = user.email
    users_data['phone_number'] = user.phone_number
    users_data['is_active'] = user.is_active
    users_data['is_church'] = user.is_church
    users_data['is_admin'] = user.is_admin
    users_data['is_bouncer'] = user.is_bouncer

    return response.success(data=users_data)



@users_router.delete('/{user_id}')
def delete_user(user_id: int):
    user = session.query(User).filter(User.id == user_id).first()
    
    if not user:
        return response.error(message="User not found", status_code=404)

    session.delete(user)
    session.commit()

    return response.success(data="User deleted successfully")
