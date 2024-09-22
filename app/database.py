from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings


#orm make us no need to key sql


SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

                                              


engine = create_engine(SQLALCHEMY_DATABASE_URL)   # to connect to the database url

SessionLocal = sessionmaker(autocommit=False,autoflush=False, bind=engine)   #to communucate/talking to the database 

Base = declarative_base() #to make the table

def get_db():
    db = SessionLocal()   #to talking/communicate with the database
    try:
        yield db
    finally:
        db.close()





# import psycopg2
# from psycopg2.extras import RealDictCursor # to get the column name
# #to connect postgres database, need to use sql
# try:
#         conn = psycopg2.connect(host='localhost',database='fastapi',user='postgres',
#                             password='socorro!',cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print('Database connection was successfull!')
        
# except Exception as error:
#         print('connection to database failedo')
#         print('Error',error)