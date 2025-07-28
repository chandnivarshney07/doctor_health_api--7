from pydantic_settings import BaseSettings



class Settings(BaseSettings):
    AIML_API_KEY: str
    AIML_API_URL: str 
    MONGODB_URI: str 
    ACCESS_TOKEN_EXPIRE_MINUTES: int 
    SECRET_KEY: str
    ALGORITHM: str
    
   
 

    class Config:
        env_file = ".env"

settings = Settings()
