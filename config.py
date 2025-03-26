import os

class Config:
    API_ID = int(os.getenv("API_ID"))
    API_HASH = os.getenv("API_HASH")
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    PARMAR_AUTH = os.getenv("PARMAR_AUTH")
    USER_ID = os.getenv("USER_ID")
    MAX_SEGMENTS = int(os.getenv("MAX_SEGMENTS", 0))
    HOST = "https://parmaracademyapi.classx.co.in"
    
    HEADERS = {
        "Authorization": PARMAR_AUTH,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
        "Auth-Key": "appxapi",
        "Client-Service": "Appx"
    }
