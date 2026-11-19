from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from .. import models,schemas,oauth2
from ..database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import func

router = APIRouter(prefix='/posts',tags=['Posts'])

@router.get("/{id}",response_model=schemas.PostOut)
def get_post(id: int,db: Session = Depends(get_db),current_user: models.User = Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""",str(id))
    # fetched_post = cursor.fetchone()
    fetched_post = (
        db.query(models.Post, func.count(models.Vote.post_id).label("votes"))
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)
        .group_by(models.Post.id)
        .filter(models.Post.id == id)
        .first()
    )
    if not fetched_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='Post not found')
    return fetched_post

@router.get("/",response_model=list[schemas.PostOut])
def get_posts(db: Session = Depends(get_db),
              current_user: models.User = Depends(oauth2.get_current_user),
              limit: int = 3,
              skip: int = 0,
              search: str = ''):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    results = (
db.query(models.Post, func.count(models.Vote.post_id).label("votes"))
.join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)
.group_by(models.Post.id)
.filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
)
    return results

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.ResponsePost)
def create_post(post: schemas.CreatePost,db: Session = Depends(get_db),
                current_user: models.User = Depends(oauth2.get_current_user)):
    # cursor.execute("""INSERT INTO posts (title,content) VALUES (%s,%s) RETURNING *""", (post.title,post.content))
    # new_post = cursor.fetchone()
    # conn.commit()
    new_post = models.Post(
        user_id=current_user.id,
        **post.model_dump()
        )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int,db: Session = Depends(get_db),
                 current_user: models.User = Depends(oauth2.get_current_user)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""",str(id))
    # deleted_post = cursor.fetchone()
    deleted_post = db.query(models.Post).filter(models.Post.id == id).first()

    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Post of id: {id} does not exist')
    # deleted_post.delete(synchronize_session=False)
    if deleted_post.user_id == current_user.id:
        db.delete(deleted_post)
        db.commit()
        # conn.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Not authorized to make this action'
        )

@router.put("/{id}",response_model=list[schemas.PostOut])
def update_post(id: int,post: schemas.CreatePost,db: Session = Depends(get_db),
                current_user: models.User = Depends(oauth2.get_current_user)):
    # cursor.execute("""UPDATE posts SET title=%s,content=%s,published=%s WHERE id =%s RETURNING *""",(post.title,post.content,post.published,str(id)))
    # updated_post = cursor.fetchone()
    updated_post_query = db.query(models.Post).filter(models.Post.id == id)
    updated_post = updated_post_query.first()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Post of id: {id} does not exist')
    # conn.commit()
    if updated_post.user_id == current_user.id:
        updated_post_query.update(post.model_dump(),synchronize_session=False)
        db.commit()
        return Response(status_code=status.HTTP_202_ACCEPTED)
    raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Not authorized to make this action'
            )
