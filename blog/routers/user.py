from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from blog import schemas
from blog.database import get_db
from ..repository import user

router = APIRouter(
    prefix='/user',
    tags=['users']
)


@router.post('/', response_model=schemas.ShowUser)
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    return user.create(request, db)


@router.get('/', response_model=list[schemas.ShowUser])
def all_users(db: Session = Depends(get_db)):
    return user.get_all(db)


@router.get('/{id}', response_model=schemas.ShowUser)
def show_user(id, db: Session = Depends(get_db)):
    return user.get_single(id, db)
