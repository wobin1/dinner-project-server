from modules.shared.models import session, User
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from .utils import Utility

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


utility = Utility()

class AuthService():
    
    # Authenticate user by verifying their credentials
    def authenticate_user(self, email: str, password: str):
        user = session.query(User).filter(User.email == email).first()
        print('user data', user)
        if not user:
            return False
        if not utility.verify_password(password, user.password):
            return False
        return user
    
    def get_current_user(self, token):
        email = utility.verify_access_token(token)
        user = session.query(User).filter(User.email == email).first()
        user_data = {}
        user_data['id'] = user.id
        user_data['email'] = user.email
        user_data['is_active'] = user.is_active
        user_data['is_staff'] = user.is_staff
        user_data['is_admin'] = user.is_admin
        if not user:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        return user_data
    

    def get_current_active_user(self, token: str = Depends(oauth2_scheme)):
        current_user = self.get_current_user(token)
        return current_user
