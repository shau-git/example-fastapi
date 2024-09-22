from passlib.context import CryptContext #pip install passlib[bcrypt]

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")  #(hash password)use bcrypt algorithm to hash the password(##), deprecated mean abort expired token

def hash(password:str):
    return pwd_context.hash(password)



def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)