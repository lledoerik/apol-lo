from sqlalchemy.orm import Session
from fastapi import HTTPException
from ..models.dao.userDAO import UserDAO
from ..utils.security import verify_password, hash_password
from ..utils.jwtHandler import create_access_token


class AuthService:
    @staticmethod
    def register(db, dto):
        if UserDAO.get_by_username(db, dto.username):
            raise HTTPException(status_code=400, detail="El nom d'usuari ja existeix")
        if dto.email and UserDAO.get_by_email(db, dto.email):
            raise HTTPException(status_code=400, detail="El correu electrònic ja existeix")
        hashed = hash_password(dto.password)
        return UserDAO.create(db, dto, hashed)
    
    @staticmethod
    def authenticate(db, username, password):
        user = UserDAO.get_by_username(db, username)
        if not user or not verify_password(password, user.hashed_password):
            return None
        token = create_access_token({"sub": user.username, "role": user.role})
        return token, user
