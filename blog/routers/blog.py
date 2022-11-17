from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status
from typing import List
from blog import schemas, models
from blog.database import get_db

router = APIRouter()


@router.get('/blog', status_code=status.HTTP_200_OK, response_model=list[schemas.ShowBlog], tags=['blogs'])
def all_blogs(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs
