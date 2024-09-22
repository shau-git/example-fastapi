from jose import JWTError, jwt     #pip install python-jose[cryptography]
from datetime import datetime, timedelta
from . import schemas,database,models
from fastapi import FastAPI,Response,status,HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')


SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes#60

def create_access_token(data: dict):    #data == payload
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token:str, credentials_exception):
    try:    
        payload = jwt.decode(token,SECRET_KEY, algorithms=[ALGORITHM])
        #print(f"Payload: {payload}")
        id:str = payload.get("user_id")   #auth.py's  access_token = oauth2.create_access_token(data = {'user_id': user.id})
        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=str(id))
    except JWTError: #as e: 
       # print(f"JWT Error: {str(e)}")
        raise  credentials_exception
    return token_data    


# function that require user to be logged in, if logged in will not return someting
# if POST method have this func need to go (POST login User)'s Body/form-data to login, then POST Create Post)'s Headers -> key:Authorization, value: Bearer +(the token code eyJh.....)
#if CRUD without logged in, it will show "detail": "Not authenticated", if enter expired or wrong token will show detail='Could not validate credentials'
def get_current_user(token:str = Depends(oauth2_scheme) , db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                         detail='Could not validate credentials',
                                         headers={'WWW-Authenticate': "Bearer"})
    token = verify_access_token(token,credentials_exception)
    user = db.query(models.User).filter(models.User.id == token.id).first()
    print(user.email)
    return user









