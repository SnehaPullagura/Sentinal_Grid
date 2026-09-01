from __future__ import annotations
import hashlib
import uuid
from typing import Optional, Dict
from sqlalchemy.orm import Session
from backend.app.auth.models import User

class AuthService:
    @staticmethod
    def hash_password(password: str) -> str:
        return hashlib.sha256(password.encode("utf-8")).hexdigest()

    @staticmethod
    def verify_password(plain: str, hashed: str) -> bool:
        return AuthService.hash_password(plain) == hashed

    @staticmethod
    def authenticate_user(db: Session, username: str, password: str) -> Optional[User]:
        user = db.query(User).filter(User.username == username).first()
        if not user or not AuthService.verify_password(password, user.hashed_password):
            return None
        return user

    @staticmethod
    def register_user(db: Session, username: str, email: str, password: str, is_admin: bool = False) -> User:
        user = User(
            username=username,
            email=email,
            hashed_password=AuthService.hash_password(password),
            is_admin=is_admin
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
