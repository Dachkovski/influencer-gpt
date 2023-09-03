import streamlit as st
from clients.youtube import YoutubeClient

def upload_video(video_url):
    # Ask the user to confirm the upload to YouTube
    if st.button("Confirm and Upload to YouTube"):
        # Initialize the YoutubeClient
        youtube_client = YoutubeClient(st.session_state['YOUTUBE_API_KEY'])
        youtube_client.authenticate()
        # Upload the video to YouTube
        youtube_client.upload_video(video_url, "Generated Video", "This video was generated using AI.", st.session_state['YOUTUBE_VIDEO_CATEGORY'], ["AI", "Generated Video"])
        st.success("Video uploaded successfully to YouTube!")
