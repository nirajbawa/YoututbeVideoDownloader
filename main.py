from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
template = Jinja2Templates(directory="templates")
from config import db

from routes.appHome import appHome
app.include_router(appHome)

from routes.auth import auth
app.include_router(auth, prefix="/auth")