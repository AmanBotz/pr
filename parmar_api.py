import requests
from config import Config

class ParmarAPI:
    def __init__(self):
        self.headers = {
            "Authorization": Config.PARMAR_AUTH,
            "Auth-Key": "appxapi",
            "Client-Service": "Appx"
        }
    
    async def get_courses(self):
        try:
            response = requests.get(
                f"{Config.HOST}/get/courselist?exam_name=&start=0",
                headers=self.headers
            )
            return response.json().get("data", [])
        except Exception as e:
            logging.error(f"Course error: {e}")
            return []
