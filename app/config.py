#from pydantic import BaseSettings
from pydantic_settings import BaseSettings 



class Settings(BaseSettings):   # environment variables, so that e dont have to exposed our password or secret key
    database_hostname: str
    database_port: str
    database_password: str #= 'localhost'    # = 'localhost' just assign it a default value
    database_name: str # the database we wanna connect   
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int 

    class Config:
        env_file = ".env"




settings = Settings()


