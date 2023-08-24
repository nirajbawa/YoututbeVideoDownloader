from pytube import YouTube
import asyncio
import os
from urllib.parse import urlparse, parse_qs
import uuid

async def getYoutubeVideoFormatDetails(videoId:str) -> dict:
    video_url = f"https://www.youtube.com/watch?v={videoId}"
    yt = YouTube(video_url)

    supported_formats_resolutions = set()

    for stream in yt.streams:
        if stream.resolution:
            format_resolution = f"{stream.mime_type.split('/')[1]} - {stream.resolution}"
        else:
            format_resolution = f"{stream.mime_type.split('/')[1]} - Audio"
        
        supported_formats_resolutions.add(format_resolution)

    # Convert the set to a list for JSON serialization
    supported_formats_resolutions_list = list(supported_formats_resolutions)

    # Create a dictionary for JSON output
    output_dict = {
        "totalSupportedCombinations": len(supported_formats_resolutions_list),
        "supportedFormatsResolutions": supported_formats_resolutions_list,
        "status":"success"
    }

    return output_dict

# print(getYoutubeVideoFormatDetails("GXo2vv0oxB4"))

async def downloadVideo(videoId:str, extension:str, resolution:str) -> dict:

    video_url = f"https://www.youtube.com/watch?v={videoId}"
    yt = YouTube(video_url)

    # Get the streams with different formats and resolutions
    streams = yt.streams.filter(progressive=True, file_extension=extension)

    # Choose a specific format and resolution
    chosen_stream = streams.get_by_resolution(resolution)  # Adjust resolution as needed

    if chosen_stream:
        download_path = os.path.join(os.getcwd(), 'videos')
        unique_identifier = str(uuid.uuid4().hex)
        file_name = f"{unique_identifier}.{extension}"
        
        file_path = chosen_stream.download(output_path=download_path, filename=file_name)

        return {"file_name": file_name, "status": "success"}


async def sanitize_link(url:str) -> str:
    parsed_url = urlparse(url)
    if parsed_url.netloc == 'youtu.be':
        video_id = parsed_url.path.lstrip('/')
    elif parsed_url.netloc == 'www.youtube.com':
        query_params = parse_qs(parsed_url.query)
        video_id = query_params.get('v', [None])[0]
    else:
        Exception("invalid url")
    return video_id

    
# async def main(): 
#     print(await downloadVideo("bON-KPiiNCk", "mp4", "720p"))
    
# asyncio.run(main())


