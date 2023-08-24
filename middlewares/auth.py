from typing import Annotated
from fastapi import Depends, HTTPException, status, Request
import jwt
from config.db import database
from schemas.users import hash_password, verify_password
from bson import ObjectId
import os

async def get_current_user(request: Request = Depends()):
    
    token = None
    collection = database["users"]

    # Retrieve token from cookies
    if "token" in request.cookies:
        token = request.cookies["token"]
        
        payload = jwt.decode(token, os.getenv("JWT_SALT"), algorithms=["HS256"])
        
        document = await collection.find_one({"_id": ObjectId(payload["id"])})

        if document and token == document["token"][0]:
            token = document
        else:
            return None


        if token is None:
            return None

    # Use your token validation logic here
    # e.g., decode and verify the token

    return token
    