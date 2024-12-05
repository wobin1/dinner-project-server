from passlib.context import CryptContext
from fastapi import HTTPException
from typing import Union
import os
from datetime import datetime, timedelta
from jose import JWTError, jwt
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your_secret_key_here")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Defining the password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



class Utility():

    # Function to hash the password
    def hash_password(self, password: str):
        return pwd_context.hash(password)

    # Function to verify the password
    def verify_password(self, plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)
    
    def create_access_token(self, data: dict, expires_delta: Union[timedelta, None] = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    def verify_access_token(self, token: str):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            email: str = payload.get("sub")
            if email is None:
                raise HTTPException(status_code=401, detail="Invalid token")
            return email
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid token")
    
    def user_insance_to_dict(self, instance):
        pass
