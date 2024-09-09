from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import database,schemas,models,utils, oauth2


router = APIRouter(tags=['Authentication'])



#uers have to provide thier credentials
#to login    #user_credentials = schemas.UserLogin
# when using POST method in postman have to Body/form-data/ key:username , value:ur@gamil.com  ; key:password , value:password123
@router.post('/login',response_model=schemas.Token)    #user_credentials: OAuth2PasswordRequestForm= Depends() only have username and password field , it dont have email field,so models.User.email == user_credentials.email need change to user_cre..username
def login(user_credentials: OAuth2PasswordRequestForm= Depends() , db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    if not user :
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN,
                            detail= f'Invalid Credentials')
    
    if not utils.verify(user_credentials.password, user.password ):
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN,
                            detail= f'Invalid Credentials')
    
    access_token = oauth2.create_access_token(data = {"user_id": user.id})
    return {"access_token" : access_token , "token_type": "bearer"}