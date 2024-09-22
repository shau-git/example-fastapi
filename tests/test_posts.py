from typing import List
from app import schemas
import pytest
###  read here   ####
#  the OP: {'id': 1, 'email': 'haha@gmail.com', 'created_at': '2024-09-19T22:26:54.144607+08:00'} is because conftest.py's test_user(client) => print(res.json())
#   OP:  haha@gmail.com was from (oauth2.py -> get_current_user())  becuase '/posts/' in router.post.py got called get_current_user


#if you wanna test already login then use 'authorized_client', if wanna test without login then 'client'

def test_get_all_posts_1(authorized_client,test_posts):
    res = authorized_client.get('/posts/')
    print(res.json())
    assert len(res.json()) == len(test_posts)
    assert res.status_code == 200


def test_get_all_posts_2(authorized_client,test_posts):
    res = authorized_client.get('/posts/')
    def validate(post):        
        return schemas.PostOut(**post)    #checking if it has id,email & created_at field, if 1 is missing wil error
    posts_map = map(validate,res.json())
    print(list(posts_map))   #for i in list(posts_map), i is in sqlalchemy model format
    assert len(res.json()) == len(test_posts)
    assert res.status_code == 200



def test_get_all_posts_2_1(authorized_client,test_posts):
    print('before authorized')  #>>>>>>>>>>>>
    res = authorized_client.get('/posts/')
    print('after authorized')    #>>>>>>>>>>>>
    def validate(post):  
        print(post)    #>>>>>>>>>>>>>>>>
        return schemas.PostOut(**post)    #checking if it has id,email & created_at field, if 1 is missing wil error
    posts_map = map(validate,res.json())
    posts_list = list(posts_map)
    print(test_posts[0].title)   #op: first title>>>>>>>>>>>>>>>>>
    assert len(res.json()) == len(test_posts)
    assert res.status_code == 200
    

def test_unauthorized_user_get_all_posts(client,test_posts):      #use client because we wanna use user who not logging in
    res = client.get('/posts/')
    assert res.status_code == 401



def test_unauthorized_user_get_one_posts(client,test_posts):      
    res = client.get(f'/posts/{test_posts[0].id}')   #becuase it is in sqlalchemy model format, and also to get the first post
    assert res.status_code == 401




def test_get_one_post_not_exist(authorized_client, test_posts):
    res = authorized_client.get('/posts/888888')
    assert res.status_code == 404




def test_get_one_post(authorized_client, test_posts):
    res = authorized_client.get(f'/posts/{test_posts[0].id}')
    print(res.json())       #{'Post': {'title': 'first title', 'content': 'first content', 'published': True, 'id': 1, 'created_at': '2024-09-21T15:01:03.794720+08:00', 'owner_id': 1, 'owner': {'id': 1, 'email': 'haha@gmail.com', 'created_at': '2024-09-21T15:01:03.783958+08:00'}}, 'votes': 0}
    post = schemas.PostOut(**res.json())
    print(post)   #sqlalchemy format , Post=Post(title='first title', content='first content', published=True, id=1, created_at=datetime.datetime(2024, 9, 21, 15, 1, 3, 794720, tzinfo=TzInfo(+08:00)), owner_id=1, owner=UserOut(id=1, email='haha@gmail.com', created_at=datetime.datetime(2024, 9, 21, 15, 1, 3, 783958, tzinfo=TzInfo(+08:00)))) votes=0
    assert post.Post.id == test_posts[0].id    
    assert post.Post.content == test_posts[0].content





@pytest.mark.parametrize('title, content, published',[
    ('awesome title' , 'awesome content', True),
    ('great title' , 'great content', False),
    ('impressive title' , 'impressive content', True)
])
def test_create_post(authorized_client, test_user, test_posts, title,content,published):     #'test_post' is optional, if you want to have data exist in the database before testing your code
    res = authorized_client.post('/posts/',json={"title":title, "content":content, "published":published})
    create_post = schemas.Post(**res.json())
    assert res.status_code == 201
    assert create_post.title == title
    assert create_post.content == content
    assert create_post.published == published 
    assert create_post.owner_id == test_user['id']



# to test if default value for schemas.PostCreate.published works
def test_create_post_default_published_true(authorized_client,test_user, test_posts):
    res = authorized_client.post('/posts/',json={"title":"abc123", "content":"def456"})  #json={"title":"abc123", "content":"def456"}  this is body
    create_post = schemas.Post(**res.json())
    assert res.status_code == 201
    assert create_post.title == "abc123"
    assert create_post.content == "def456"
    assert create_post.published == True   #the default value is True 
    assert create_post.owner_id == test_user['id']




def test_unauthorized_user_create_post(client,test_posts,test_user):      #test_user is optional, is just that it will create a user, but wont login(authorized_client)
    res = client.post('/posts/',json={"title":"abc123", "content":"def456"})
    assert res.status_code == 401



def test_unauthorized_user_delete_post(client,test_posts,test_user):      #delete post without logging in
    res = client.delete(f'/posts/{test_posts[0].id}')
    assert res.status_code == 401


def test_delete_post_success(authorized_client,test_posts):
    res = authorized_client.delete(f'/posts/{test_posts[0].id}')
    assert res.status_code == 204



def test_delete_nonexist_post(authorized_client,test_posts,test_user):  #actually no need to put test_user here as test_post already called, but anyway
    res = authorized_client.delete('/posts/88888')
    assert res.status_code == 404




def test_delete_other_user_post(authorized_client,test_posts,test_user):  #authorized_client used user 1
    res = authorized_client.delete(f'/posts/{test_posts[3].id}')   #sqlalchemy autoincrement start at 1, but the test_post return as a list so 4th post is index 3.
    assert res.status_code == 403



def test_updated_post(authorized_client,test_posts,test_user):
    data ={
        'title' : 'updated 1st title',
        'content': 'updated 1st content',
        'id': test_posts[0].id
    }
    res = authorized_client.put(f'/posts/{test_posts[0].id}',json=data) # why '{test_posts[0].id}' ,it return 1st post with the id, example you want post id 1 then: '/posts/1'  
    updated_post = schemas.Post(**res.json())
    assert res.status_code == 200
    assert updated_post.title == data['title']
    assert updated_post.content == data['content']




def test_update_other_user_post(authorized_client,test_posts,test_user):  #to update post own by others, we login as haha, but update abc's post
    data = {
        'title' : 'new title',
        'content': 'new content',
        'id': test_posts[3].id
    }
    res = authorized_client.put(f'/posts/{test_posts[3].id}',json=data)
    assert res.status_code == 403





def test_unauthorized_user_update_post(client,test_posts):      #dupdate post without logging in
    data ={
        'title' : 'updated 1st title',
        'content': 'updated 1st content',
        'id': test_posts[0].id
    }
    res = client.put(f'/posts/{test_posts[3].id}',json=data)
    assert res.status_code == 401



def test_update_nonexist_post(authorized_client,test_posts,test_user):  #actually no need to put test_user here as test_post already called, but anyway
    data_1 ={   
        'title' : 'updated 1st title',
        'content': 'updated 1st content',
        'id': test_posts[0].id
    }      
    res = authorized_client.put('/posts/88888',json=data_1)
    assert res.status_code == 404