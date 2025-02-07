# This file contains the definiton for the User model

import enum

from app.database import ( database )
from datetime import datetime
from sqlalchemy import ( DateTime, Integer, String )
from sqlalchemy.orm import ( Mapped, mapped_column )

class UserRoleEnum(enum.Enum):
    '''
    Defines the enumerations for the users role column
    '''
    EDITOR = "editor"

class User(database.Model):
    '''
    Defines the user model for the Blog Zero site
    '''

    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(
        Integer(),
        primary_key=True,
        autoincrement=True
    )
    username: Mapped[str] = mapped_column(
        String(150),
        unique=True,
        nullable=False
    )
    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False
    )
    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )
    role: Mapped[UserRoleEnum]
    created_at: Mapped[datetime] = mapped_column(
        DateTime(),
        default=datetime.now
    )

    def __repr__(self):
        _description = f"User '{self.username}'."
        return _description