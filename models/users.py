from pydantic import BaseModel
from fastapi import Form

class Users(BaseModel):
    fullName:str
    email:str
    password:str