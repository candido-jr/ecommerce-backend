from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import BaseColumns


class User(BaseColumns):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(320), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
