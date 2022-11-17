from fastapi import APIRouter, Depends, HTTPException
from fastapi.openapi.models import Response
from sqlalchemy.orm import Session
from starlette import status
from typing import List
from blog import schemas, models
from blog.database import get_db
from ..repository import blog

router = APIRouter(
    prefix='/blog',
    tags=['blogs']
)


@router.get('/', status_code=status.HTTP_200_OK, response_model=list[schemas.ShowBlog])
def all_blogs(db: Session = Depends(get_db)):
    return blog.get_all(db)


@router.post('/', status_code=status.HTTP_201_CREATED)
def create_blog(request: schemas.Blog, db: Session = Depends(get_db)):
    return blog.create(request, db)


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(id, db: Session = Depends(get_db)):
    return blog.delete(id, db)


@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update_blog(id, request: schemas.Blog, db: Session = Depends(get_db)):
    return blog.update(request, id, db)


@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.ShowBlog)
def single_blog(id, response: Response, db: Session = Depends(get_db)):
    return blog.get_single(id, db)
