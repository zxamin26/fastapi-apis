from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from .. import models,schemas,oauth2
from ..database import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix='/vote',tags=['VOTE'])

@router.post('/')
def vote(vote: schemas.Vote,db: Session = Depends(get_db),current_user: schemas.UserData = Depends(oauth2.get_current_user)):

    if db.get(models.Post, vote.post_id) == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='post not found')

    existing = db.get(models.Vote, (current_user.id, vote.post_id))

    if vote.vote_dir == 1:
        if existing:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=f'User {current_user.id} has already voted.')
        db.add(models.Vote(user_id=current_user.id, post_id=vote.post_id))
        db.commit()

        return {'message': 'Upvoted'}

    if not existing:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'User {current_user.id} has not voted.')
    db.delete(existing)
    db.commit()
    return {'message':'Downvoted'}
        
