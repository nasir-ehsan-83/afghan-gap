# server/src/config/__init__.py
import os
from .development import dev_settings
from .production import prod_settings

ENV = os.getenv("ENVIRONMENT", "development")

if ENV == "production":
    settings = prod_settings
else:
    settings = dev_settings

__all__ = ["settings"]