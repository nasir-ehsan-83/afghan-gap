# config/production.py
from .config import Settings

class ProductionSettings(Settings):
    DEBUG: bool
    LOG_LEVEL: str
    
    class Config:
        env_file = ".env.production"

prod_settings = ProductionSettings()