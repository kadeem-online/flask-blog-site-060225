# Model for the posts table

import re

from app.database import ( database )
from datetime import ( datetime )
from enum import ( Enum )
from sqlalchemy import ( DateTime, Enum as EnumType, ForeignKey, Integer, String, Text )
from sqlalchemy.orm import ( Mapped, mapped_column, relationship )

class PostStatusEnum(Enum):
    '''
    Define enumerations for valid status values a post can have.
    '''
    DRAFT="draft"
    PUBLISHED="published"

class Post(database.Model):
    '''
    Defines the posts model corelating to the 'posts' table within the blog zero database.
    '''
    __tablename__ = "posts"

    id:Mapped[int] = mapped_column(
        Integer(),
        primary_key=True,
        autoincrement=True
    )
    title:Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        index=True
    )
    content:Mapped[str] = mapped_column(
        Text(),
        nullable=False
    )
    slug:Mapped[str] = mapped_column(
        String(128),
        nullable=True,
        unique=True,
        index=True
    )
    status:Mapped[PostStatusEnum] = mapped_column(
        EnumType(PostStatusEnum),
        nullable=False,
        default=PostStatusEnum.DRAFT,
        index=True
    )
    created_at:Mapped[datetime] = mapped_column(
        DateTime(),
        nullable=False,
        default=datetime.now
    )
    updated_at:Mapped[datetime] = mapped_column(
        DateTime(),
        nullable=False,
        default=datetime.now
    )
    author_id:Mapped[int] = mapped_column(
        ForeignKey("users.id")
    )
    author:Mapped["User"] = relationship(
        back_populates="posts"
    )

    def generate_slug(self):
        '''
        Generates a slug from the title
        '''
        _title = self.title.lower().strip()
        _slug = f"{self.id}-" + re.sub(r'[^\w]+', '-', _title)
        
        # remove any non-alphanumeric characters at the end
        _clean_slug = re.sub(r'[^\w]+$', "", _slug)

        self.slug = _clean_slug
        database.session.add(self)
        database.session.commit()
        return self