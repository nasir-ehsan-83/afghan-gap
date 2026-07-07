from enum import Enum

class UserRole(str, Enum):
    ADMIN = "admin"
    SUPER_USER = "super_user"
    USER = "user"

class UserStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    BANNED = "banned"
    SUSPENDED = "suspended"  

class UserVisibility(str, Enum):
    PUBLIC = "public"
    PRIVATE = "private"
