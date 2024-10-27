from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from .database import Base

class Post(Base):
    __tablename__ = 'posts'  
    
    id = Column(Integer, primary_key=True, nullable=False) 
    title = Column(String, nullable=False) 
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='TRUE', nullable=False) 
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    # Add this relationship to link Post to User
    owner = relationship("User", back_populates="posts")  # The owner of the post (i.e., the User)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, nullable=False) 
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    # Add this relationship to link User to Post
    posts = relationship("Post", back_populates="owner")  # The posts created by this user
    
class Vote(Base):
    __tablename__ = 'votes'
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"),primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id",ondelete="CASCADE"), primary_key=True)
