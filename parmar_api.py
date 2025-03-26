import requests
from config import Config

class ParmarAPI:
    def __init__(self):
        self.config = Config
        
    async def fetch_data(self, url):
        try:
            response = requests.get(url, headers=self.config.HEADERS, timeout=10)
            response.raise_for_status()
            return response.json().get("data", [])
        except Exception as e:
            print(f"API Error: {str(e)}")
            return []

    async def get_courses(self):
        return await self.fetch_data(f"{self.config.HOST}/get/courselist?exam_name=&start=0")

    async def get_subjects(self, course_id):
        return await self.fetch_data(f"{self.config.HOST}/get/allsubjectfrmlivecourseclass?courseid={course_id}&start=-1")

    async def get_topics(self, course_id, subject_id):
        return await self.fetch_data(f"{self.config.HOST}/get/alltopicfrmlivecourseclass?courseid={course_id}&subjectid={subject_id}&start=-1")

    async def get_videos(self, course_id, subject_id, topic_id):
        return await self.fetch_data(f"{self.config.HOST}/get/livecourseclassbycoursesubtopconceptapiv3?courseid={course_id}&subjectid={subject_id}&topicid={topic_id}&conceptid=&windowsapp=false&start=-1")

    async def get_video_details(self, course_id, video_id):
        try:
            response = requests.get(
                f"{self.config.HOST}/get/fetchVideoDetailsById?course_id={course_id}&video_id={video_id}&ytflag=0&folder_wise_course=1",
                headers=self.config.HEADERS,
                timeout=10
            )
            data = response.json().get("data", {})
            return {
                'iv': data.get("ivb6", ""),
                'token': data.get("video_player_token", ""),
                'qualities': data.get("available_qualities", ["360p"]),
                'encrypted_links': data.get("encrypted_links", {})
            }
        except Exception as e:
            print(f"Video Details Error: {str(e)}")
            return {}
