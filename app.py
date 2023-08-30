# Import necessary libraries
import os
import openai
from dotenv import load_dotenv
import requests
import tweepy
import streamlit as st
import json
from clients.d_id import DIdClient
from clients.heygen import create_heygen_video
from clients.youtube import YoutubeClient
import asyncio

# Set Streamlit page configuration
st.set_page_config(page_title="Influencer GPT", page_icon=":bird:")

# Load environment variables
load_dotenv()

# Authenticate Twitter API
bearer_token = st.session_state.get('TWITTER_BEARER_TOKEN', '')
twitter_client = tweepy.Client(bearer_token)

# Authenticate OpenAI API
openai.api_key = st.session_state.get('YOUR_OPENAI_API_KEY', '')

# Configure HeyGen API
HEYGEN_API_ENDPOINT = "https://api.heygen.com/v1/video.generate"
HEYGEN_API_KEY = st.session_state.get('HEYGEN_API_KEY', '')
avatar_id = os.getenv("YOUR_AVATAR_ID")  # Assuming this is still from an env variable

# Authenticate D-ID API
D_ID_API_KEY = st.session_state.get('D_ID_API_KEY', '')
d_id_client = DIdClient(api_key=D_ID_API_KEY)

# Uploaded image for the talking head
uploaded_image = st.file_uploader("Upload an image for the talking head", type=["png", "jpg", "jpeg"])
if uploaded_image is not None:
    with open("uploaded_image.png", "wb") as f:
        f.write(uploaded_image.getbuffer())
    source_url = "uploaded_image.png"
    # Store the last uploaded image in a session variable
    st.session_state['last_uploaded_image'] = "uploaded_image.png"
else:
    # Option to reuse the last uploaded image
    if 'last_uploaded_image' in st.session_state and st.button("Click on the image to reuse it"):
        st.image(st.session_state['last_uploaded_image'])
        source_url = st.session_state['last_uploaded_image']
    else:
        source_url = "https://cdn.discordapp.com/attachments/1116787243634397345/1146111608129597450/hypercubefx_face_like_terminator_bb7255e5-efca-489d-bf9e-9aeb750a6bef.png"

def search_twitter_trends(topic):
    trends = twitter_client.search_recent_tweets(topic, max_results=10)
    return [trend.text for trend in trends]


def search_gpt_trends(topic):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a trend generator. Provide the top trends based on the given topic. Give each trend in a new line. Don't repeat the same trend.Don't write introduction and end, only write the trends."},
            {"role": "user", "content": f"What are the top trends about {topic}?"}
        ]
    )
    
    # Hier nehmen wir an, dass die Antwort des Modells eine kommagetrennte Liste von Trends ist.
    # Sie können die Antwortstruktur anpassen, je nachdem, wie Sie das Modell trainieren oder anweisen.
    trends = completion.choices[0].message["content"].split('\n')
    return trends



# generate video script with openai gpt api 
def create_video_script(topic):

    completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": topic}
    ]
    )
    script = completion.choices[0].message.get("content")
    return script



async def check_video_status_async(d_id_client, talk_id):
    with st.spinner("Video is being processed..."):
        while not d_id_client.is_video_ready(talk_id):
            await asyncio.sleep(10)
    return d_id_client.get_video_url(talk_id)



def main():
    # Load settings from file if it exists
    if os.path.exists("settings.json"):
        with open("settings.json", "r") as f:
            settings_data = json.load(f)
        
        for key, value in settings_data.items():
            st.session_state[key] = value
    st.header("Influencer GPT :bird:")
    query = st.text_input("Trend Topic")

    if query:
        # Initialization
        if 'trend_engine' not in st.session_state:
            st.session_state['trend_engine'] = 'GPT'
        trend_function_choice = st.session_state['trend_engine']

        st.write(f"Searching {trend_function_choice} for ", query)

        # Add clear button
        if st.button("Clear"):
            st.session_state.get().clear()

        # Entscheidung, welche Trendsuchfunktion zu verwenden ist
        if trend_function_choice == "X":
            trends = search_twitter_trends(query)
        else:
            trends = search_gpt_trends(query)

        # Lassen Sie den Benutzer einen Trend aus der Liste auswählen
        selected_trend = st.selectbox("Select a trend", trends)

        # Verwenden Sie den ausgewählten Trend, um das Skript zu generieren
        script = create_video_script(selected_trend)
        
        # Lassen Sie den Benutzer das generierte Skript bearbeiten
        edited_script = st.text_area("Edit the generated script:", script)
        
        # Button to confirm editing and proceed to video generation
        if st.button("Confirm and Generate Video"):
            # Use the edited script for video generation
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
                    preview_video(video_url)
                    # Ask the user to confirm the upload to YouTube
                    if st.button("Confirm and Upload to YouTube"):
                        # Initialize the YoutubeClient
                        youtube_client = YoutubeClient(st.session_state['YOUTUBE_API_KEY'])
                        youtube_client.authenticate()
                        # Upload the video to YouTube
                        youtube_client.upload_video(video_url, "Generated Video", "This video was generated using AI.", st.session_state['YOUTUBE_VIDEO_CATEGORY'], ["AI", "Generated Video"])
                        st.success("Video uploaded successfully to YouTube!")
                else:
                    st.error("Failed to create video.")


if __name__ == '__main__':
    main()

def preview_video(video_url):
    st.video(video_url)
