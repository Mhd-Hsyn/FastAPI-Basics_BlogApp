# FastAPI Blog API

This FastAPI project manages and retrieves blog entries, including user-related functionality.

## Features

- Create a new blog entry
- Retrieve all blog entries
- Retrieve a specific blog entry by ID
- Delete a blog entry by ID
- Update a blog entry by ID
- Retrieve all blog entries with response models
- Create a new blog entry with user relations
- Retrieve a blog entry with user relations by ID
- User sign-up API

## Endpoints

- **POST /blog/**
  - Create a new blog entry.

- **GET /blog/**
  - Retrieve all blog entries.

- **GET /blog/{id}**
  - Retrieve a specific blog entry by ID.

- **DELETE /blog/{id}**
  - Delete a blog entry by ID.

- **PUT /blog/{id}**
  - Update a blog entry by ID.

- **GET /blog/blogs-resp-model/**
  - Retrieve all blog entries with response models.

- **GET /blog/blogs-resp-model/{id}**
  - Retrieve a specific blog entry with response models by ID.

- **POST /blog/blog-with-relation/**
  - Create a new blog entry with user relations.

- **GET /blog/get-blog-with-relation/{id}**
  - Retrieve a blog entry with user relations by ID.

- **POST /user/user-signup**
  - User sign-up.

- **GET /user/get-user-by_id/{id}**
  - Retrieve user by ID.

## Dependencies

- FastAPI
- SQLAlchemy
- Pydantic

## How to Run

1. Clone the repository: `git clone https://github.com/Mhd-Hsyn/FastAPI-Basics_BlogApp.git`
2. Install dependencies: `pip install -r requirements.txt`
3. Run the FastAPI application: `uvicorn main:app --reload`

## Database Configuration

- The project uses SQLAlchemy for database operations.
- Database models are defined in `models.py`.

## Author

Syed Muhammad Hussain
