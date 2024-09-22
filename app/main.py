from fastapi import FastAPI
from . import models #. means current directory
from .database import engine
from .routers import post,user,auth,vote
from .config import settings
from fastapi.middleware.cors import CORSMiddleware



print(settings.database_username)

#to connect the database.py file , dont need sql to query
#models.Base.metadata.create_all(bind=engine)    & Base.metadata.create_all(bind=engine)  are the same as both inherit the sam instance 'Base'; if Base1.metadata.create_all(bind=engine) & models.Base2.metadata.create_all(bind=engine) will get different OP

app = FastAPI()

origins=["*"]   #* means everything  so here is mean every website , if only want a specific web, for example only google.com then just put "https://google.com"

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# my_posts =[{'title': 'title of post 1' , 'content': 'content of post 1' , 'id':1}, 
#            {'title':"favourite foods","content" : 'I like pizza', "id":2}]

# def find_post(id):
#     for p in my_posts:
#         if p['id'] == id:
#             return p

# def find_index_post(id):
#     for i,e in enumerate(my_posts):
#         if e['id'] == id:
#             return i



app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get('/')
def root():
    return {'message' : 'hello world'}







# @app.get('/sqlalchemy')
# def test_post(db: Session = Depends(get_db)):
#     posts = db.query(models.Post)
#     print(posts)
#     return {'data':'sucessfull'}


# @app.get('/posts/latest')
# def get_latest_post():
#     post = my_posts[len(my_posts)-1]
#     return {"latest post" : post}










