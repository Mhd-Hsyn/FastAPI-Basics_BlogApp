"""
Main project file 
"""

from fastapi import FastAPI, status, Depends, Response, HTTPException
from typing import Optional, List
import uvicorn
import scheema
import models
from database_config import engine, SessionLocal
from sqlalchemy.orm import Session
from passlib.context import CryptContext


models.Base.metadata.create_all(bind= engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



app = FastAPI()

@app.get('/')
def index():
    return {
        "status": True,
        "message": "Start Application . . . "
    }


# Path Parameters
# http://localhost:8001/blog/1
@app.get('/blog/get-blog/{id}')
def get_blog(id: int):
    return {"status": True, "ID": id}


# Query Parameters
# http://localhost:8001/blog/?limit=100&published=True&sort=latest
@app.get('/blog/')
def get_blogs(limit:int = 10, published:bool = False, sort: Optional[str] = None):

    sort_status = sort if sort is not None else ". . . No sorting . . ."
    publish_status = "published" if published else "not published"
    message = f"{sort_status} {limit} Blogs are {publish_status}"
    return {"status": True , "message" : message}



# Use Both Methods Path paras + Query params
# http://localhost:8001/blog/1/comment?limit=100
@app.get('/blog/{id}/comment')
def get_blogs(id:int, limit:int = 10):

    message = f"{limit} Comments are in Blog ID ___{id}____"
    return {"status": True , "message" : message}




@app.post('/blog/', status_code = status.HTTP_201_CREATED)
def add_blog(blog: scheema.Blog, db : Session= Depends(get_db)):
    new_blog = models.Blog(
        title = blog.title,
        content = blog.content,
        published = blog.published
    )
    db.add(new_blog)
    db.commit()
    db.refresh

    return {"message": f"Blog created with title as '{blog.title}'", "scheema": blog}



@app.get('/blog/')
def get_all_blog(db : Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    print(blogs)

    all_blogs = []
    for blog in blogs:
        blog_detail = {
            "blog_id": blog.id,
            "blog_title": blog.title,
            "blog_content": blog.content,
            "blog_published": blog.published
        }
        all_blogs.append(blog_detail)
    
    print (all_blogs)
    return {"DB_data": blogs, "my_data": all_blogs}





"""
Response Method
"""

# @app.get('/get-blog/{id}', status_code= 200)
# def get_blog_by_id(id : int, db: Session= Depends(get_db), response: Response = None):
#     blog = db.query(models.Blog).filter(models.Blog.id == id).first()
#     if not blog:
#         response.status_code= status.HTTP_404_NOT_FOUND
#         return {'status': False, "error": "ID not found"}
#     return {'status': True, 'blog': blog}


"""
raise HTTP-Response
"""
@app.get('/blog/{id}', status_code= 200)
def get_blog_by_id(id : int, db: Session= Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(
            detail= {
                'status': False, 
                "error": "ID not found"
                },status_code= status.HTTP_404_NOT_FOUND
            )
    return {'status': True, 'blog': blog}



@app.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(id: int, db: Session= Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(
            detail= {
                "status": False,
                "error": f"{id} ID not Found"
            }, status_code= status.HTTP_404_NOT_FOUND
        )
    blog.delete()
    db.commit()
    db.refresh
    # Because of status_code HTTP_204_NO_CONTENT you can't see any respone message in dictionary
    return {'status': True, 'message': f'{id} Deleted Successfully . . .'}



@app.put('/blog/{id}', status_code= status.HTTP_202_ACCEPTED)
def update_blog(id: int, new_blog: scheema.Blog, db: Session=Depends(get_db)):

    # print(new_blog)
    old_blog= db.query(models.Blog).filter(models.Blog.id== id)
    if not old_blog.first():
        raise HTTPException (
            detail= {
                "status": False,
                "error": f"{id} ID not found"
            }, status_code= status.HTTP_404_NOT_FOUND
        )
    
    old_blog.update(new_blog.dict())
    db.commit()
    return {"status": True, "message":"Updated Successfully"}


# Response Model
# 02:08
"""
Response Model is the custom Model Inherit from BaseModel 
Custom Model SCHEEMA "ShowBlogTitle", which return only title of the Blogs  
"""

@app.get('/blog/blogs-resp-model/', status_code=200, response_model=  List[scheema.ShowBlogTitle])
def get_all_blog_resp_model(response: Response , db : Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    print(blogs)

    return blogs



@app.get('/blog/blogs-resp-model/{id}', status_code=200, response_model=  scheema.ShowBlogTitle)
def get_all_blog_resp_model(id, db : Session = Depends(get_db)):
    fetch_blog = db.query(models.Blog).filter(models.Blog.id==id).first()
    print(fetch_blog)

    return fetch_blog



# for hashing password 
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)




# For User
@app.post('/user/user-signup', status_code= 201)
def user_signup(request: scheema.User, db: Session= Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.email == request.email).first()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    new_user = models.User(
        name= request.name,
        email= request.email,
        password= pwd_context.hash(request.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# Check scheema for both POST and GET request
# in above POST, Scheema are in request
# in below GET, Scheema are in response_model

# GET USER 
@app.get('/user/get-user-by_id/{id}', status_code=200, response_model= scheema.ShowUserAllBlogs)
def get_user(id: int , db: Session= Depends(get_db)):
    fetch_user= db.query(models.User).filter(models.User.id == id).first()
    if fetch_user:
        return fetch_user
    else:
        raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST,
            detail= {
                "status": False,
                "message": "No user found"
            }
        )



# WITH  USER RELATIONS
    


@app.post('/blog/blog-with-relation', status_code = status.HTTP_201_CREATED)
def add_blog(blog: scheema.Blog, db : Session= Depends(get_db)):
    new_blog = models.Blog(
        title = blog.title,
        content = blog.content,
        published = blog.published,
        user_id= 1
    )
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)

    return {"message": f"Blog created with title as '{blog.title}'", "data": new_blog}




@app.get('/blog/get-blog-with-relation/{id}', status_code=status.HTTP_200_OK, response_model= scheema.UserBlog)
def get_blog(id, response: Response, db: Session = Depends(get_db)):
    blog= db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "status":False,
                "message": "No Blog found"
            }
        )
    return blog
























if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)
