# config/development.py
from .config import Settings

class DevelopmentSettings(Settings):
    DEBUG: bool
    LOG_LEVEL: str = "DEBUG"
    
    class Config:
        env_file = ".env.development"

dev_settings = DevelopmentSettings()