from enum import Enum

class ReactionType(str, Enum):
    like = "like"
    love = "love"
    haha = "haha"
    wow = "wow"
    sad = "sad"
    angry = "angry"

class PostType(str, Enum):
    video = "video"
    audio = "audio"
    image = "image"
    text = "text"

class PostVisibility(str, Enum):
    public = "public"
    private = "private"
    follwer_only = "folloer only"

class PostStatus(str, Enum):
    draft = "draft"
    deleted = "deleted"
    updated = "updated"
    published = "published"
    archived = "archived"