# Import necessary library
import requests

# Function to create a Heygen video
def create_heygen_video(script, HEYGEN_API_KEY, avatar_id, HEYGEN_API_ENDPOINT):
    # Define headers
    headers = {
        "Content-Type": "application/json",
        "X-Api-Key": HEYGEN_API_KEY
    }
    
    # Define data
    data = {
        "background": "#FAFAFA",
        "ratio": "16:9",
        "test": False,
        "version": "v1alpha",
        "caption_open": True,
        "clips": [
            {
                "avatar_id": avatar_id,
                "avatar_style": "normal",
                "input_text": script
            }
        ]
    }
    
    # Send POST request to create a video
    response = requests.post(HEYGEN_API_ENDPOINT, headers=headers, json=data)
    
    # Return video URL if successful, else return None
    if response.status_code == 200:
        return response.json().get("video_url")
    else:
        return None
