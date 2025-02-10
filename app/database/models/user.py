# This file contains the definiton for the User model

import enum

from app.database import ( database )
from app.extensions import ( login_manager )
from datetime import datetime
from flask_login import ( UserMixin )
from sqlalchemy import ( DateTime, Integer, String )
from sqlalchemy.orm import ( Mapped, mapped_column, relationship )
from typing import ( List )
from werkzeug.security import ( check_password_hash, generate_password_hash )

class UserRoleEnum(enum.Enum):
    '''
    Defines the enumerations for the users role column
    '''
    EDITOR = "editor"

class User(database.Model, UserMixin):
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
    posts: Mapped[List["Post"]] = relationship(
        back_populates="author"
    )

    def __repr__(self):
        _description = f"User '{self.username}'."
        return _description
    
    def hash_user_password(password:str)->str:
        '''
        Centralized function for hashing the user's password.

        Parameters:
            password(int) - the plaintext password to be hashed.
        
        Returns:
            hashed_password(str) - the hash for the input plaintext password.
        '''

        _hash = generate_password_hash(password=password)
        return _hash

    def verify_user_password(password_hash:str, password:str)->bool:
        '''
        Centralized function for verifying the legitimacy of the provided password
        against the hash saved in the database.

        Parameters:
            password_hash(str) - The hashed password saved on the database.
            password(str) - The password to be verified against the hashed passsword.

        Returns:
            is_valid(bool) - boolean representing if the password provided matches the hash.
        '''
        _is_valid = check_password_hash(pwhash=password_hash, password=password)
        return _is_valid

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)