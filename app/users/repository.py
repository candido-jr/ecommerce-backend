from sqlalchemy import select
from sqlalchemy.orm import Session

from app.users.models import User


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_email(self, email: str) -> User | None:
        stmt = select(User).where(User.email == email)
        return self.db.execute(stmt).scalars().first()

    def get_by_id(self, user_id: int) -> User | None:
        return self.db.get(User, user_id)
