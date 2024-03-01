"""
Database Models File
"""

from sqlalchemy import Column,Integer, String, Boolean, ForeignKey
from database_config import Base
from sqlalchemy.orm import relationship



class User(Base):
    __tablename__= 'User'

    id= Column(Integer, primary_key=True, index= True)
    name= Column(String)
    email= Column(String)
    password= Column(String)

    blogs= relationship("Blog", back_populates="creator")



class Blog(Base):
    __tablename__ = 'Blog'

    id = Column(Integer, primary_key= True, index=True)
    title = Column(String)
    content = Column(String)
    published = Column(Boolean)
    
    user_id= Column(Integer, ForeignKey('User.id'))
    creator= relationship("User", back_populates="blogs")

