from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import (
    create_access_token,
    create_refresh_token,
    verify_password,
)
from app.users.repository import UserRepository


class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.users = UserRepository(db)

    def login(self, email: str, password: str) -> tuple[str, str]:
        user = self.users.get_by_email(email)
        if user is None or not verify_password(password, user.password_hash):
            raise ValueError("Invalid credentials")

        access = create_access_token(
            subject=str(user.id),
            secret=settings.JWT_SECRET,
            expires_minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
        )
        refresh = create_refresh_token(
            subject=str(user.id),
            secret=settings.JWT_SECRET,
            expires_days=settings.REFRESH_TOKEN_EXPIRE_DAYS,
        )
        return access, refresh
