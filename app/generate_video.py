import streamlit as st
import asyncio
from clients.d_id import DIdClient
from clients.heygen import create_heygen_video

d_id_client = DIdClient(api_key=st.session_state.get('D_ID_API_KEY', ''))

async def check_video_status_async(d_id_client, talk_id):
    with st.spinner("Video is being processed..."):
        while not d_id_client.is_video_ready(talk_id):
            await asyncio.sleep(10)
    return d_id_client.get_video_url(talk_id)

def generate_video(edited_script, source_url):
    # Initialization
    if 'video_engine' not in st.session_state:
        st.session_state['video_engine'] = 'D-ID'
    video_engine_choice = st.session_state['video_engine']

    st.write(f"Generating Video with {video_engine_choice} for ", query)

    # Decide which trend search function to use
    if video_engine_choice == "Heygen":
        video_url = create_heygen_video(edited_script)
        if video_url:
            st.write(f"Video created successfully! [Watch here]({video_url})")
        else:
            st.error("Failed to create video.")
    else:
        st.write("Video Generation with D-ID")

        talk = d_id_client.create_talk(source_url, edited_script)
        talk_id = talk.get("id")
        print(f"Talk ID: {talk_id}")

        # Check if the video is ready
        video_url = asyncio.run(check_video_status_async(d_id_client, talk_id))
        if video_url:
            st.write(f"Video URL: {video_url}")
            # Preview the video
            st.video(video_url)
        else:
            st.error("Failed to create video.")

    return video_url
