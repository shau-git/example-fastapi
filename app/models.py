from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import null,text
from sqlalchemy.orm import relationship


#to create table in postgres:   
#after clcking safe at vs code & refreshing postgres , your table will be available in postgres
class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer , primary_key = True, nullable = False)  #When you define a column as Integer and primary_key=True, SQLAlchemy automatically configures it to be an auto-incrementing column,sqlalchemy autoincrement start at 1
    title = Column(String, nullable = False)
    content = Column(String, nullable = False)
    published = Column(Boolean, server_default= 'True', nullable = False)
    created_at = Column(TIMESTAMP(timezone=True),nullable = False, server_default=text('now()'))
    owner_id = Column(Integer, ForeignKey("users.id", ondelete='CASCADE'), nullable=False)
     # if add another column here have to drop the 'posts' table in postgres then save vs code and refresh postgres table
    owner = relationship('User')    #create a relationship between 'Post' and 'User' so that when getting post will show the created user
    





class User(Base):
    __tablename__ = 'users'    

    id = Column(Integer , primary_key = True, nullable = False)
    email =Column(String, nullable=False,unique=True)            #string cannot use acronym because all this type are import from sqlalchemy
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),nullable = False, server_default=text('now()'))
    phone_number = Column(String)



class Vote(Base):
    __tablename__ = 'votes'

    user_id = Column(Integer, ForeignKey("users.id", ondelete='CASCADE'), primary_key=True)#, nullable=False)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete='CASCADE'), primary_key=True)#, nullable=False)