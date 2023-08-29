import os
#from dotenv import load_dotenv
import requests
import tweepy
import streamlit as st

# Laden Sie die Umgebungsvariablen
#load_dotenv()

# Twitter API Authentifizierung
twitter_api_key = os.getenv("TWITTER_API_KEY")
twitter_api_secret_key = os.getenv("TWITTER_API_SECRET_KEY")
twitter_access_token = os.getenv("TWITTER_ACCESS_TOKEN")
twitter_access_token_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
openai_api_key = os.getenv("YOUR_open_ai_api_key")

auth = tweepy.OAuthHandler(twitter_api_key, twitter_api_secret_key)
auth.set_access_token(twitter_access_token, twitter_access_token_secret)
twitter_api = tweepy.API(auth)

# HeyGen API Konfiguration
HEYGEN_API_ENDPOINT = "https://api.heygen.com/v1/video.generate"
HEYGEN_API_KEY = os.getenv("HEYGEN_API_KEY")

def search_twitter_trends(topic):
    trends = twitter_api.search(q=topic, count=10)
    return [trend.text for trend in trends]

# generate video script with openai gpt api 
def create_video_script(topic):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {openai_api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "messages": [
            {"role": "system", "content": "You are a script generator for heygen."},
            {"role": "user", "content": f"Create a script about {topic}."}
        ]
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    response_json = response.json()
    script = response_json["choices"][0]["message"]["content"]
    return script

def create_heygen_video(script):
    headers = {
        "Content-Type": "application/json",
        "X-Api-Key": HEYGEN_API_KEY
    }
    
    data = {
        "background": "#FAFAFA",
        "ratio": "16:9",
        "test": False,
        "version": "v1alpha",
        "caption_open": True,
        "clips": [
            {
                "avatar_id": "YOUR_AVATAR_ID",
                "avatar_style": "normal",
                "input_text": script
            }
        ]
    }
    
    response = requests.post(HEYGEN_API_ENDPOINT, headers=headers, json=data)
    
    if response.status_code == 200:
        return response.json().get("video_url")
    else:
        return None

def main():
    st.set_page_config(page_title="AI research agent", page_icon=":bird:")

    st.header("AI research agent :bird:")
    query = st.text_input("Research goal")

    if query:
        st.write("Searching Twitter trends for ", query)
        trends = search_twitter_trends(query)
        script = create_video_script(trends)
        st.write("Video Script: ", script)

        video_url = create_heygen_video(script)
        if video_url:
            st.write(f"Video created successfully! [Watch here]({video_url})")
        else:
            st.error("Failed to create video.")

if __name__ == '__main__':
    main()
