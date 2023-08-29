import requests

def create_heygen_video(script, HEYGEN_API_KEY, avatar_id, HEYGEN_API_ENDPOINT):
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
                "avatar_id": avatar_id,
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
