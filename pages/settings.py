# settings.py
# Import necessary libraries
import streamlit as st
import json


# Display header and description
st.header("Settings")
st.write("Here you can adjust the settings for the app.")

# Provide option to select Trend Search Engine
st.subheader("Trend Search Engine")
st.session_state['trend_engine'] = st.selectbox(
    "Select Trend Search Engine",
    ("X", "GPT")
)

# Provide option to select Video Generation Engine
st.subheader("Video Generation Engine")
st.session_state['video_engine'] = st.selectbox(
    "Select Video Generation Engine",
    ("D-ID", "Heygen")
)

# Configure API Keys
st.subheader("API Key Configurations")
st.session_state['TWITTER_BEARER_TOKEN'] = st.text_input("Twitter Bearer Token", type="password")
st.session_state['YOUR_OPENAI_API_KEY'] = st.text_input("OpenAI API Key", type="password")
st.session_state['HEYGEN_API_KEY'] = st.text_input("HeyGen API Key", type="password")
st.session_state['D_ID_API_KEY'] = st.text_input("D-ID API Key", type="password")
st.session_state['YOUTUBE_API_KEY'] = st.text_input("YouTube API Key", type="password")

# Provide option to select YouTube video category
st.subheader("YouTube Video Category")
st.session_state['YOUTUBE_VIDEO_CATEGORY'] = st.selectbox(
    "Select YouTube Video Category",
    ("Film & Animation", "Autos & Vehicles", "Music", "Pets & Animals", "Sports", "Travel & Events", "Gaming", "People & Blogs", "Comedy", "Entertainment", "News & Politics", "Howto & Style", "Education", "Science & Technology", "Nonprofits & Activism")
)

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


# Save button to persistently save the settings
if st.button("Save Settings"):
    settings_data = {
        'TWITTER_BEARER_TOKEN': st.session_state['TWITTER_BEARER_TOKEN'],
        'YOUR_OPENAI_API_KEY': st.session_state['YOUR_OPENAI_API_KEY'],
        'HEYGEN_API_KEY': st.session_state['HEYGEN_API_KEY'],
        'D_ID_API_KEY': st.session_state['D_ID_API_KEY'],
        'YOUTUBE_API_KEY': st.session_state['YOUTUBE_API_KEY'],
        'trend_engine': st.session_state['trend_engine'],
        'video_engine': st.session_state['video_engine'],
        'last_uploaded_image': st.session_state.get('last_uploaded_image', '')
    }
    
    # Save settings data to a JSON file
    with open("settings.json", "w") as f:
        json.dump(settings_data, f)
    
    # Display success message
    st.success("Settings saved successfully!")
