# Import necessary library
import requests

# Define DIdClient class
class DIdClient:
    def __init__(self, base_url="https://api.d-id.com", api_key=None):
        # Initialize class variables
        self.base_url = base_url
        self.api_key = api_key
        self.headers = {
            "Authorization": f"Basic {self.api_key}",
            "Content-Type": "application/json"
        }

    # Function to create a talk
    def create_talk(self, source_url, script_text):
        endpoint = "/talks"
        payload = {
            "source_url": source_url,
            "script": {
                "type": "text",
                "input": script_text
            }
        }
        # Send POST request to create a talk
        response = requests.post(f"{self.base_url}{endpoint}", headers=self.headers, json=payload)
        return response.json()

    # Function to get a talk
    def get_talk(self, talk_id):
        endpoint = f"/talks/{talk_id}"
        # Send GET request to retrieve a talk
        response = requests.get(f"{self.base_url}{endpoint}", headers=self.headers)
        return response.json()

    # Function to check if a video is ready
    def is_video_ready(self, talk_id):
        talk_data = self.get_talk(talk_id)
        return talk_data.get("status") == "done"

    # Function to get a video URL
    def get_video_url(self, talk_id):
        talk_data = self.get_talk(talk_id)
        return talk_data.get("result_url") if self.is_video_ready(talk_id) else None


