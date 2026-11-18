from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from .. import models,schemas,utils
from ..database import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix='/user',tags=['Users'])

@router.post("/signup",response_model=schemas.UserData,status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.CreateUser, db: Session = Depends(get_db)):

    hashed_pass = utils.hasher(user.password)
    user.password = hashed_pass
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/{id}",response_model=schemas.UserData,status_code=status.HTTP_200_OK)
def get_user(id: int,db: Session = Depends(get_db)):
    user_query = db.query(models.User).filter(models.User.id == id)

    if user_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='User not found')

    user = db.query(models.User).filter(models.User.id == id).first()
    return user