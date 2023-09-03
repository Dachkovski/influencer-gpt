import openai
import streamlit as st

# Authenticate OpenAI API
openai.api_key = st.session_state.get('YOUR_OPENAI_API_KEY', '')

# generate video script with openai gpt api 
def create_video_script(topic):

    completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": f"create a viral shortform video skript for a talking head about: {topic}. Give just the script to say, no meta desciption or anything else."}
    ]
    )
    script = completion.choices[0].message.get("content")
    return script
