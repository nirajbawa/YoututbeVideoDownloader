from fastapi import APIRouter
from fastapi import Request, Response
from fastapi.responses import RedirectResponse
from fastapi.responses import HTMLResponse
from main import template
from config.db import database
import starlette.status as status
import jwt
from schemas.users import hash_password, verify_password
from middlewares.auth import get_current_user
import os

auth = APIRouter()


@auth.get("/signin", response_class=HTMLResponse)
async def signin(request:Request):
    token = await get_current_user(request)
    if not token:
        return template.TemplateResponse("signin.html", {"request":request})
    else:
        return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)

@auth.get("/signup", response_class=HTMLResponse)
async def signup(request:Request):
    token = await get_current_user(request)
    if not token:
        return template.TemplateResponse("signup.html", {"request":request})
    else:
        return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)

@auth.post("/api/signin")
async def apiSignIn(request:Request):
    form = await request.form()
    formDict = dict(form)
    collection = database["users"]
    try:
        document = await collection.find_one({"email": formDict["email"]})
        ver_pass = verify_password(str(formDict["password"]),str(document["password"]))
        
        if document and ver_pass: 
            token = jwt.encode({"id":str(document["_id"])}, os.getenv("JWT_SALT"), algorithm="HS256")
            await collection.update_one({"_id": document["_id"]}, {"$set": {"token":[token]}})
            
            response = RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
            response.set_cookie(key="token", value=token) 
            
            return response
        else:
            msg = "Please Enter Valid Credentials"
            return template.TemplateResponse("signin.html", {"request":request, "msg":msg})
    except Exception as e:   
        print(e)
        msg = "Try Again"
        return template.TemplateResponse("signin.html", {"request":request, "msg":msg})



@auth.post("/api/signup")
async def apiSignUp(request:Request):
    form = await request.form()
    formDict = dict(form)
    collection = database["users"]
    try:

        documents = []
        async for doc in collection.find({"email":formDict["email"]}):
            documents.append(doc)
        if len(documents) == 0: 
            haskpass = hash_password(str(formDict["password"]))
            formDict["password"] = haskpass
            entry = await collection.insert_one(formDict)
            token = jwt.encode({"id":str(entry.inserted_id)}, os.getenv("JWT_SALT"), algorithm="HS256")
            await collection.update_one({"_id": entry.inserted_id}, {"$set": {"token":[token]}})
            
            response = RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
            response.set_cookie(key="token", value=token)
            
            return response
        else:
            msg = "User Already Exist Please Sign In"
            return template.TemplateResponse("signup.html", {"request":request, "msg":msg})
    except Exception as e:   
        print(e)
        msg = "Try Again"
        return template.TemplateResponse("signup.html", {"request":request, "msg":msg})

@auth.get("/api/signout/")
async def signOut(request:Request):
    token = await get_current_user(request)
    if token:
        response = RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
        response.delete_cookie(key="token")
        return response
    else:
        RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)