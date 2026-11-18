from fastapi import status,HTTPException,Depends,APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from ..database import get_db
from sqlalchemy.orm import Session
from .. import models,utils,oauth2

router = APIRouter()

@router.post("/login")
def authenticate(user_creds: OAuth2PasswordRequestForm = Depends(),db: Session=Depends(get_db)):

    user = db.query(models.User).filter(models.User.email == user_creds.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='Invalid credentials')
    
    verified = utils.verify_pass(user_creds.password,user.password)

    if not verified:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='Invalid credentials')

    access_token = oauth2.create_access_token(data={'user_id': user.id})
    
    return {'access token': access_token,'token_type': 'bearer'}
