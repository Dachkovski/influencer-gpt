import os
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

class YoutubeClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.youtube = None

    def authenticate(self):
        self.youtube = build('youtube', 'v3', developerKey=self.api_key)

    def upload_video(self, video_file_path, title, description, category_id, tags):
        # Create a resource object for the video
        body=dict(
            snippet=dict(
                title=title,
                description=description,
                tags=tags,
                categoryId=category_id
            ),
            status=dict(
                privacyStatus='public'
            )
        )

        # Call the API's videos.insert method to create and upload the video
        insert_request = self.youtube.videos().insert(
            part=','.join(body.keys()),
            body=body,
            media_body=MediaFileUpload(video_file_path, chunksize=-1, resumable=True)
        )

        response = None
        while response is None:
            status, response = insert_request.next_chunk()
            if status:
                print("Uploaded %d%%." % int(status.progress() * 100))

        print("Upload Complete!")
        return response
