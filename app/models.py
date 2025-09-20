from typing import Text
from sqlalchemy.orm import relationship
from sqlalchemy import TIMESTAMP, Column, ForeignKey,Integer,String,Boolean,Update,Delete
from sqlalchemy.sql.expression import null
from .database import Base

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable= False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='True', nullable=False)
    created_at=Column(TIMESTAMP(timezone=True),nullable= False,server_default=Text('now()'))
    owner_id=Column(Integer,ForeignKey("Users.id",ondelete="CASCADE"),nullable=False)   

    owner= relationship("User")


class User(Base):
    __tablename__="Users"

    id = Column(Integer,primary_key=True, nullable= False)
    email = Column(String, nullable=False,unique=True)
    password=Column(String, nullable=False)
    created_at=Column(TIMESTAMP(timezone=True),nullable= False,server_default=Text('now()'))   

