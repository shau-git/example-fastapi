from .. import models,schemas,oauth2  #. means current directory , ..means go back one folder
from fastapi import FastAPI,Response,status,HTTPException, Depends, APIRouter
from ..database import   get_db
from sqlalchemy.orm import Session
from typing import  List, Optional
from sqlalchemy import func   #func is like COUNT,MAX,MIN,LENGHT etc


router=APIRouter(prefix='/posts',# prefix makes u no needa keep typing '/posts' in every function decorator, just need to use '/'
                 tags = ['Posts']
 )  

#router replace app






#@router.get('/')
@router.get('/' , response_model=List[schemas.PostOut])    #schemas.Post can only return 1 at a time, but we need all the things, so need import List from typing module to store all the things in List
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),
              limit: int=10, skip: int=0, 
              search: Optional[str] = ""): # the limit is like set it for user to searching ({{URL}}posts?limit=2) the default value is 10, skip is the skip certain post, default value is 0
                            #example ({{URL}}posts?limit=1&skip=1&search=po)    %20 is space for searching, if want search 'my n'(my name is....) == {{URL}}posts?limit=1&skip=1&search=my%20n
  
   # print(limit)   #skip is like each web page contain 20 content, when going to next page it will skip/offset the 10 contents, here print the limit input by the user
    
    #posts_1 = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()      #filter(models.Post.owner_id==current_user.id).all()      #.all()  means grab/return all the (relevant) query
                            #the search is it will find the input and filter if the input in the title({{URL}}posts?search=po)  wil return("post4","po5","posss6")
                                #.filter(models.Post.id==current_user.id) means only the owner of the post can read the post,make ur post private
   
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote,models.Post.id ==models.Vote.post_id, isouter=True).group_by(models.Post.id).filter(
                  models.Post.title.contains(search)).limit(limit).offset(skip).all()
                    #join by default is left join  , SELECT posts.*,COUNT(votes.user_id) AS votes FROM posts LEFT JOIN votes ON posts.id = votes.post_id GROUP BY posts.id ;
    return posts
#both are the same ,above and below

#@app.get('/posts')
#def get_posts():
    # cursor.execute("""SELECT * FROM posts""")
    # posts =cursor.fetchall() # to return the query
    # return {'data':posts}


    




@router.post('/',status_code=status.HTTP_201_CREATED , response_model=schemas.Post) 
def create_posts(post:schemas.PostCreate, db: Session = Depends(get_db) , current_user: int = Depends(oauth2.get_current_user)):
   # new_post=models.Post(title=post.title, content=post.content, published=post.published)   #models is file name models.py
    print(current_user.id)
    print(current_user.email)      
    new_post = models.Post(owner_id=current_user.id ,**post.dict())  #replace the title=post.title...... this thing automatically unpack all the attributes, dont have to key in 1by1
                                   #owner_id=current_user.id ==set/add the owner_id to current_user.id because request format (schemas.PostCreate) dont have owner_id but response format have , so do tat can solve the issue
    db.add(new_post)          #add the new post to database
    db.commit() 
    db.refresh(new_post)      # similar to RETURNING *
    return new_post
#both are the same ,above and below

# @app.post('/posts',status_code=status.HTTP_201_CREATED)                                            #pydantic model
# def create_posts(post:Post): #the post from left para is different from app.post, can be anyname
#     cursor.execute("""INSERT INTO posts (title, content, published) VALUES 
#                    (%s ,%s,%s) RETURNING * """,(post.title,post.content,post.published))
#     new_post = cursor.fetchone()                                                                    # to return the query
#     conn.commit()                                                                                   #to save/acknowledge the updating
#     return {'data' : new_post} #to get the newly created post from just now









@router.get('/{id}',response_model=schemas.PostOut)   #prefix '/{id}' == /posts/{id}
def get_post(id:int,  db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # post = db.query(models.Post).filter(models.Post.id == id).first()  # filter == WHERE , .first() means grab/return the first instance it sees 
    
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote,models.Post.id ==models.Vote.post_id, isouter=True).group_by(
            models.Post.id).filter(models.Post.id == id).first()
    
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail = f'post with id {id} was not found') 
    # if post.owner_id !=  current_user.id:             #to make ur post private
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
    #                         detail = f'Not authorized to perform action')       
    return post
#both are the same ,above and below

# @app.get('/posts/{id}')
# def get_post(id:int):# ,response:Response):  
#     cursor.execute("""SELECT * FROM posts WHERE id = %s
#                     """,(str(id)))                       #str(id) because the select statement is a str so need convert the id to str
#     post = cursor.fetchone()# to return the query
#     if post == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail = f'post {id} was not found')       
#     return {'post_detail': post}











@router.delete('/{id}',status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:                                  #if deleted_post.first() == None:  means if the first item with the target id is none:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail = f'post with {id} does not exist') 
    
    if post.owner_id !=  current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail = f'Not authorized to perform action') 
    post_query.delete(synchronize_session=False)
    db.commit()    
    return Response(status_code=status.HTTP_204_NO_CONTENT)

#both are the same ,above and below

# @app.delete('/posts/{id}',status_code=status.HTTP_204_NO_CONTENT)
# def delete_post(id:int):
#     cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING *""",(str(id)))
#     deleted_post = cursor.fetchone()
#     conn.commit()
#     if deleted_post == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail = f'post with {id} does not exist')       # the detail para will just op if post==None
#     return Response(status_code=status.HTTP_204_NO_CONTENT)








@router.put("/{id}", response_model=schemas.Post)     #schemas is from schemas.py
def update_post(id:int, post:schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    
    if post_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail = f'post with {id} does not exist') 
    if post_query.first().owner_id !=  current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail = f'Not authorized to perform action') 
    post_query.update(post.dict(),
                      synchronize_session=False)    
    db.commit()    
    return post_query.first()
#both are the same ,above and below

# @app.put("/posts/{id}")
# def update_post(id:int,post:Post):
#     cursor.execute("""UPDATE posts SET title = %s , content=%s, published=%s WHERE id = %s RETURNING * """,
#                    (post.title,post.content,post.published,str(id)))
#     updated_post = cursor.fetchone()
#     conn.commit()   
#     if updated_post == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail = f'post with {id} does not exist')      
#     return {'data': updated_post}