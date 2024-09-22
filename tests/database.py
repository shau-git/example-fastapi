'''this file is useless now since all database codes are in conftest.py but just leave it here'''
from fastapi.testclient import TestClient     #testclient is like pytest to test our fastapi code
from app.main import app
from app import schemas
from app.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.database import get_db,Base
from app import models
from alembic import command
import pytest



#so it wont affect our develop database (create another database just for testing purpose)       #technically the database name should different,but here use the same as development
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"     #=> fastapi_test(databasename)                      

engine = create_engine(SQLALCHEMY_DATABASE_URL)   # to connect to the database url

TestingSessionLocal = sessionmaker(autocommit=False,autoflush=False, bind=engine)   #to communucate/talking to the database 

#Base.metadata.create_all(bind=engine)  #as we already done it inside session()

#Base = declarative_base() #to make the table

# def override_get_db():
#     db = TestingSessionLocal()   #to talking/communicate with the database
#     try:
#         yield db
#     finally:
#         db.close()


#to swap the dependency out 
#becuase we inherit the app, so it will link to get_db(), with this when running 'pytest -v -s tests\test_users.py' it will use/swap override_get_db instead of get_db
#app.dependency_overrides[get_db] = override_get_db   #already did it inside 'client(session)'



#to manipulate database
@pytest.fixture#(scope='module')   #if here provides 'function' will be destroyed after finishing testing per function
def session():

    Base.metadata.drop_all(bind=engine)#if you want to see the data then put it before create_all() so you will able to see the data
                                        #if you put after create_all() will drop the table after executing, so when going back to the databse it wont generate/find any data 
    Base.metadata.create_all(bind=engine) 
    db = TestingSessionLocal()   #to talking/communicate with the database
    try:
        yield db
    finally:
        db.close()



#client = TestClient(app)
@pytest.fixture#(scope='module')  #will be destroyed after all the codes within the module is done, because if is "function" will drop all the table which cause 403 when testing login with this can avoid that
def client(session):    #to manipulate client side, for testing
    def override_get_db():       
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db  
    yield TestClient(app)
    


#@pytest.fixture    
# def client():     # with this we dont have to keep deleting the parameters before retesting the same thing, as the data might already exist in the databse
#     Base.metadata.drop_all(bind=engine)
#     Base.metadata.create_all(bind=engine)
#     yield TestClient(app)

# @pytest.fixture    #alternative way for using alembic method
# def client():
#     command.upgrade('head')
#     yield TestClient(app)
#     command.downgrade('base')

