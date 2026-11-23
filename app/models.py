from app.database import  Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, DateTime, ForeignKey
from datetime import datetime, timezone

class URL(Base):
    __tablename__ = "urls"
    id:Mapped[int] = mapped_column(primary_key=True)
    original_url:Mapped[str] =mapped_column(String(2048), nullable=False)
    short_code:Mapped[str] = mapped_column(String(20), nullable=False, unique=True)
    user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    user: Mapped["User| None"] = relationship(back_populates="urls")
    click_count: Mapped[int] = mapped_column(default=0, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    urls: Mapped[list["URL"]] = relationship(back_populates="user")