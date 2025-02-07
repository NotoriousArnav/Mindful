from pydantic import BaseModel, validator, Field
from typing import Optional
from datetime import datetime
from bson import ObjectId


class ObjectIdStr(str):
    """
    Helper class to handle ObjectId conversion to string.
    """

    @classmethod
    def __get_pydantic_json_schema__(cls, core_schema, handler):
        return {"type": "string", "example": "64f46b1ae736da7d8f73dcbd"}

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, value, *_):
        print(_)
        if isinstance(value, ObjectId):
            return str(value)
        if isinstance(value, str):
            return value
        raise ValueError("Invalid ObjectId")


class CSS(BaseModel):
    content: str

    class Config:
        json_schema_extra = {
            "example": {
                "content": "body { background-color: lightblue; }"
            }
        }

class Markdown(BaseModel):
    content: str
    style: Optional[CSS] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "content": "# Welcome to Markdown!",
                "style": {
                    "content": "h1 { color: red; }"
                }
            }
        }

class AbsUser(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    profile_image: str | None

class User(AbsUser):
    uid: ObjectIdStr = Field(alias="_id")

class UserCreate(AbsUser):
    password: str

class FullUser(User):
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class NoteCollection(BaseModel):
    uid: ObjectIdStr = Field(alias="_id")
    title: str
    created_at: datetime
    updated_at: datetime

class NoteCollectionCreate(NoteCollection):
    author: str

class Note(BaseModel):
    title: str
    content: Markdown
    created_at: datetime
    updated_at: datetime
    collection: Optional[ObjectIdStr] = None

class NoteCreate(Note):
    author: str

class NoteFetch(Note):
    uid: ObjectIdStr = Field(alias="_id")
    author: str
