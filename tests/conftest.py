'''is a special filename for pytest.fixture  , with this you no longer have to <from .database import client, session>, python will automtically come here to find the fixture '''
#you can create another folder in test folder and make another conftest.py for those subfile under the new folder since these outter file dont have the access to there
import pytest
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
from app.oauth2 import create_access_token
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





@pytest.fixture
def test_user(client):    #its independently set for login test, so we no need to create a user test just for login in test purpose, with  this u just edit form here will do
    user_data = {'email':'haha@gmail.com', "password":'password789'}
    res= client.post('/users/',json = user_data)
    assert res.status_code == 201
    print(res.json())         
    new_user = res.json()
    new_user['password']  = user_data['password']      #the res.json OP is refer to the response of '/users/' which is schemas..UserOut   it dont have password field so we do this 
    return new_user



@pytest.fixture
def test_user2(client):    #to cater for deleting post own by others
    user_data = {'email':'abc@gmail.com', "password":'password789'}
    res= client.post('/users/',json = user_data)
    assert res.status_code == 201
    print(res.json())         
    new_user = res.json()
    new_user['password']  = user_data['password']      
    return new_user




@pytest.fixture    #create token for testing
def token(test_user):
    print('doing token')  #>>>>>>>>>>>>
    return create_access_token({'user_id':test_user['id']})


#test its authorization
@pytest.fixture
def authorized_client(client,token):
    print('during authorized')  #>>>>>>>>>>>>
    client.headers={
        **client.headers, #to spread out all the headers,like username, password, client_id, client_secret etc ?!
        "Authorization": f'Bearer {token}'   #adding "Authorization": f'Bearer {token}' to client
    }
    return client



@pytest.fixture         #create test post
def test_posts(test_user,session, test_user2):
    posts_data = [{
        'title': 'first title',
        'content':'first content',
        'owner_id': test_user['id']
    },{
        'title': '2nd title',
        'content':'2nd content',
        'owner_id': test_user['id']
    },{
        'title': '3rd title',
        'content':'3rd content',
        'owner_id': test_user['id']
    },{
        'title': '4th title',
        'content':'4th content',
        'owner_id': test_user2['id']
       }]
    
    def create_post_model(post):
        return models.Post(**post)   #same as you do **post.dict(), is just that here is already dict format so no need .dict()
    print('doing test_posts')   #>>>>>>>>>>>>>>>>>>>>>>
    post_map = map(create_post_model,posts_data)    #for i in post , it map all the i to the model's field
    posts = list(post_map)   # to convert it into list format
    session.add_all(posts)
    # session.add_all([models.Post(title = 'first title', content= 'first content' , owner_id = test_user['id'])],
    #                 [models.Post(title = '2nd title', content= '2nd content' , owner_id = test_user['id'])],
    #                 [models.Post(title = '3rd title', content=  '3rd content', owner_id = test_user['id'])])
    session.commit()
    posts = session.query(models.Post).all()  # to see your data/post   if print it out the OP is in list format
    return posts















