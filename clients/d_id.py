import requests

class DIdClient:
    def __init__(self, base_url="https://api.d-id.com", api_key=None):
        self.base_url = base_url
        self.api_key = api_key
        self.headers = {
            "Authorization": f"Basic {self.api_key}",
            "Content-Type": "application/json"
        }

    def create_talk(self, source_url, script_text):
        endpoint = "/talks"
        payload = {
            "source_url": source_url,
            "script": {
                "type": "text",
                "input": script_text
            }
        }
        response = requests.post(f"{self.base_url}{endpoint}", headers=self.headers, json=payload)
        return response.json()

    def get_talk(self, talk_id):
        endpoint = f"/talks/{talk_id}"
        response = requests.get(f"{self.base_url}{endpoint}", headers=self.headers)
        return response.json()

    def is_video_ready(self, talk_id):
        talk_data = self.get_talk(talk_id)
        return talk_data.get("status") == "done"

    def get_video_url(self, talk_id):
        talk_data = self.get_talk(talk_id)
        return talk_data.get("result_url") if self.is_video_ready(talk_id) else None


