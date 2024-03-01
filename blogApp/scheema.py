"""
Scheemas for Database Model

"""


from typing import Optional, List
from pydantic import BaseModel


class Blog(BaseModel):
    title : str
    content : str
    published: Optional[bool] = False


class ShowBlogTitle(BaseModel):
    title : str
    id : int
    class Config():
        orm_mode = True  # its necessary because of doing query in main.py



class User(BaseModel):
    name: str
    email: str
    password: str


class ShowUser(BaseModel):
    name: str
    email: str
    class Config():
        orm_mode = True  # its necessary because of doing query in main.py

    

class UserBlog(ShowBlogTitle):
    # creator : User 
    creator : ShowUser 
    
    class Config():
        orm_mode = True  # its necessary because of doing query in main.py



class ShowUserAllBlogs(BaseModel):
    name: str
    email: str
    blogs : List[Blog]
    # class Config():
    #     orm_mode = True  # its necessary because of doing query in main.py not necessary in only respose model

    
