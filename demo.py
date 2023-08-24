def add(firstName: str, lastName: str):
    firstName.capitalize()
    return firstName + " " + lastName

n = "niraj"
b = "bava"
name = add(n, b)
print(name)


from typing import Union
from pydantic import BaseModel


class User(BaseModel):
    id:int
    signup_ts:str 
    friends: list = []

external_data = {
    "id":123,
    "signup_ts":"2017-06-01 12:22",
    "friends":[1, "b"]
}

user = User(**external_data)
print(user)

print(user.id)