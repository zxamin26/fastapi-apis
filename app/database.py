from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .config import settings

engine = create_engine(settings.sqlalchemy_database_url)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)

class Base(DeclarativeBase):
    pass

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# while True:
#     try:
#         conn = psycopg2.connect(host='localhost',password='zamin123',database='fastapidb',user='postgres',cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print('Connected')
#         break
#     except Exception as error:
#         print('Error verifying details')
#         print('Error details: ', error)
#         time.sleep(3)

# def find_index(id: int):
#     for index,post in enumerate(db):
#         if post['id'] == id:
#             return index
#     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Post does not exist')

# @app.get("/posts/latest",status_code=status.HTTP_302_FOUND)
# def get_latest_post():
#     cursor.execute("""SELECT * FROM posts""")
#     posts = cursor.fetchall()
#     return posts