from fastapi import FastAPI, Depends, status, Response, HTTPException
from sqlalchemy.orm import Session
from . import schemas, models
from .database import engine, SessionLocal

from .hashing import Hash

app = FastAPI()

models.Base.metadata.create_all(engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/blog', status_code=status.HTTP_201_CREATED, tags=['blogs'])
def create_blog(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)

    return new_blog


@app.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=['blogs'])
def delete_blog(id, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)

    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Blog with id \'{id}\' is not available')

    blog.delete(synchronize_session=False)
    db.commit()

    return 'done'


@app.put('/blog/{id}', status_code=status.HTTP_202_ACCEPTED, tags=['blogs'])
def update_blog(id, request: schemas.Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)

    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Blog with id \'{id}\' is not available')

    blog.update(request.dict())
    db.commit()

    return 'done updates'


@app.get('/blog', status_code=status.HTTP_200_OK, response_model=list[schemas.ShowBlog], tags=['blogs'])
def all_blogs(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


@app.get('/blog/{id}', status_code=status.HTTP_200_OK, response_model=schemas.ShowBlog, tags=['blogs'])
def single_blog(id, response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Blog with id \'{id}\' is not available')
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'detail': f'Blog with id \'{id}\' is not available'}
    return blog


@app.post('/user', response_model=schemas.ShowUser, tags=['users'])
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    new_user = models.User(name=request.name, email=request.email, password=Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@app.get('/user', response_model=list[schemas.ShowUser], tags=['users'])
def all_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users


@app.get('/user/{id}', response_model=schemas.ShowUser, tags=['users'])
def show_user(id, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'user with id \'{id}\' is not available')
    return user
