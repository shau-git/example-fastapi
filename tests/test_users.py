import pytest
from app import schemas
#from .database import client, session #if no session imported will error   , both of these are pytest.fixture
from jose import jwt
from app.config import settings
# now no import pytest.fixture also can works becuase of the special conftest.py file

def test_root(client):
    res = client.get('/')
    print(res.json())   #OP:{'message': 'hello world'}
    print(res.json().get('message'))   #hello world
    assert res.json().get('message') == 'hello world' #here if at the main.py if changed the message to 'hello world!'  here will error
    assert res.status_code == 200 #the def root():dont have defined status code so it default to 200, if we have set it to 201 at the main file, but here we set to 200 will error


def test_create_user_1(client):
    res = client.post('/users/',json={'email':'mark@gmail.com', "password":'password789'})  #test create_user() the json is the schemas.UserCreate  so we input email and password to test
    print(res.json())  # the (-s, print) should be in the schemas.UserOut format : {'id': 3, 'email': 'mark@gmail.com', 'created_at': '2024-09-10T21:11:32.573378+08:00'}
    assert res.json().get('email') == 'mark@gmail.com' #can do this to check if the email is match
    assert res.status_code == 201  #201 because at the create_user() will show 201 if successfully  #after terminal shows passed can go postgres to check
                                  # if use the existing email will error (maybe we've set the email col to be unique)


def test_create_user_2(client):
    res = client.post('/users/',json={'email':'haha@gmail.com', "password":'password789'})
    new_user = schemas.UserOut(**res.json())     #**res.json to unpack it so it is in the right format to create UserOut model, and just checking if it has id,email & created_at field, if 1 is missing wil error
    assert new_user.email == 'haha@gmail.com'
    assert res.status_code == 201  
    


def test_login_user(test_user,client):         #the field for login is not called email, but username  #the reeason you put test_user here is because u wanna create a user in database so u can test the login
    res = client.post('/login',data={'username':test_user['email'], "password":test_user['password']})  #here use data instead of json is because when logging in in POSTMAN,we use form-data in the body
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms=[settings.algorithm])
    id: str = payload.get('user_id')
   # print(res.json()) #if you have error, can print this to check
    assert id == test_user['id']
    assert login_res.token_type == 'bearer'
    assert res.status_code == 200


@pytest.mark.parametrize('email,password,status_code',[
    ('wrongemail@gmail,com','password789',403),
    ('haha@gmail.com','wrongpassword',403),
    ('wrongemail@gmail.com','wrongpassword',403),
    (None,'password789',422),
    ('haha@gmail.com',None,422)
 ])
def test_incorrect_login(test_user,client,email,password,status_code):
    res = client.post('/login',data={'username':email, "password":password})
    assert res.status_code == status_code
    #assert res.json().get('detail') == 'Invalid Credentials'
# def test_incorrect_login(test_user,client):
#     res = client.post('/login',data={'username':test_user['email'], "password":'wrongpassword'})
#     assert res.status_code == 403
#     assert res.json().get('detail') == 'Invalid Credentials'



