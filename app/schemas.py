from pydantic import BaseModel, EmailStr#, conint
from datetime import datetime
from typing import Optional
from pydantic.types import conint

class PostBase(BaseModel):   #pydantic model
    title: str
    content: str
    published : bool =True #default to True if no provided any value
   # rating: Optional[int] = None #value assign is optional ,only accept int.If no provided will output None(wont op anything)


class PostCreate(PostBase):   
    pass


class UserOut(BaseModel):   # def how the structure we want the response  respond to new user
    id: int
    email: EmailStr
    created_at : datetime
    class config:
        orm_mode = True



class Post(PostBase):       #it contains PostBase classes's attributes
    id:int
    created_at : datetime
    owner_id: int
    owner: UserOut
    class config:
        orm_mode = True   #the new_post variable in create_post func is sql model , this is to tell pydantic to read the data even is not a dict
    
    
#post with vote
class PostOut(BaseModel):
    Post: Post  #the latter Post ==Post class
    votes: int    
    class config:
        orm_mode = True
#the vote(post.py's def get_posts()'s (return result) ) op from postman is expect to be like:  so we have to set it be like tat
#{
#    "Post":{
#        "id":1
#        "published":True
#        "owner_id":23
#        "title": "fdgnhg"
#        "content": "dhg"
#       "created_at": "2021-08-25T22:38:44.511524-04:00"
#    },
#    "votes":0
#}





class UserCreate(BaseModel):
    email: EmailStr   #to validate if is proper email (hdhdhd) will throw "value is not a valid email address:
    password: str



class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token : str
    token_type: str

class TokenData(BaseModel):
    id:Optional[str] = None


class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)
    #dir here means like or dislike ,(le=1) means only allow number <= 1, not include -ve num, so only(1,0)






