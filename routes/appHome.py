from fastapi import APIRouter
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, FileResponse
from main import template
from middlewares.auth import get_current_user
from fastapi.responses import RedirectResponse
import starlette.status as status
from utilities.youtube_video_downloader.download_video import getYoutubeVideoFormatDetails, sanitize_link, downloadVideo
import os

appHome = APIRouter()



@appHome.get("/", response_class=HTMLResponse)
async def home(request:Request):
    token = await get_current_user(request)
    if token:
        return template.TemplateResponse("home.html", {"request":request, "signin":"true"})
    else:
        return RedirectResponse(url="/auth/signin", status_code=status.HTTP_303_SEE_OTHER)

    
@appHome.post("/video/download")
async def videoDetils(request:Request):
    data = await request.json()
    print(data["format"])
    print(data["resolution"])
    link = await sanitize_link(data["link"])
    video = await downloadVideo(link, data["format"], data["resolution"])
    return video


@appHome.get("/video/download/file")
async def videoDetils(request:Request):
    data = request.query_params
    print(data)
    if os.path.exists(os.path.join(os.getcwd(), "videos")):
        return FileResponse(os.path.join(os.getcwd(), "videos", data["fileName"]), headers={"Content-Disposition": f"attachment; filename={data['fileName']}"})
    else:
        return {"message": "File not found"}