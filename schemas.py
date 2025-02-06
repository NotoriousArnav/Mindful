from pydantic import BaseModel, validator
from typing import Optional
from datetime import datetime
from bson import ObjectId


class ObjectIdStr(str):
    """
    Helper class to handle ObjectId conversion to string.
    """
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, value):
        if isinstance(value, ObjectId):
            return str(value)
        if isinstance(value, str):
            return value
        raise ValueError("Invalid ObjectId")


class CSS(BaseModel):
    content: str

class Markdown(BaseModel):
    content: str
    style: Optional[CSS] = None




class AbsUser(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    profile_image: str | None

class User(AbsUser):
    uid: ObjectIdStr

class UserCreate(AbsUser):
    password: str

class FullUser(User):
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class NoteCollection(BaseModel):
    uid: ObjectIdStr
    title: str
    created_at: datetime
    updated_at: datetime


class Note(BaseModel):
    uid: ObjectIdStr
    author: User
    title: str
    content: Markdown
    created_at: datetime
    updated_at: datetime
    collection: Optional[NoteCollection] = None
