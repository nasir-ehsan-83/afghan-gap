from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_HOSTNAME: str
    DATABASE_PORT: str
    DATABASE_USERNAME: str
    DATABASE_PASSWORD: str
    DATABASE_NAME: str
    
    ACCESS_TOKEN_SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    
    REFRESH_TOKEN_SECRET_KEY: str
    REFRESH_TOKEN_EXPIRE_DAYS: str

    ALGORITHM: str

    DEBUG: bool 
    ALLOWED_HOSTS: list 
    LOG_LEVEL: str

    class Config:
        env_file = ".env"
        env_file_ecncoding = "utf-8"

settings = Settings()