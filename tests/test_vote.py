import pytest
from app import models

@pytest.fixture()   #make a voted post, in this case is post id 4
def test_vote(test_posts,session, test_user):#session just to change it directly
    new_vote = models.Vote(post_id = test_posts[3].id, user_id = test_user['id'])
    session.add(new_vote)
    session.commit()



#login as haha and vote for first post
def test_vote_post(authorized_client,test_posts):
    res = authorized_client.post(f'/vote/',json={'post_id':test_posts[3].id ,'dir':1})
    assert res.status_code == 201



def test_vote_same_post_twice(authorized_client,test_posts,test_vote):
    res = authorized_client.post(f'/vote/',json={'post_id':test_posts[3].id ,'dir':1})
    assert res.status_code == 409



def test_remove_vote(authorized_client,test_posts,test_vote):
    res = authorized_client.post(f'/vote/',json={'post_id':test_posts[3].id ,'dir':0})
    assert res.status_code == 201   #201 because we are posting a 0 to this


def test_remove_nonexisting_vote(authorized_client,test_posts):  #here dont have test_vote because we wanna delete unexisting post
    res = authorized_client.post(f'/vote/',json={'post_id':test_posts[3].id ,'dir':0})
    assert res.status_code == 404 


def test_vote_nonexisting_post(authorized_client,test_posts):  #here dont have test_vote because we wanna delete unexisting post
    res = authorized_client.post(f'/vote/',json={'post_id':test_posts[3].id ,'dir':0})
    assert res.status_code == 404 


def test_unauthorized_user_vote_post(client,test_posts):  #here dont have test_vote because we wanna delete unexisting post
    res = client.post(f'/vote/',json={'post_id':test_posts[3].id ,'dir':0})
    assert res.status_code == 401

