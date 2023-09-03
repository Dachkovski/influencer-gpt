from app.get_trends import get_trends
from app.create_video_script import create_video_script
from app.generate_video import generate_video
from app.upload_video import upload_video

def automatic_workflow(query, session_state):
    # Initialize trend_engine if it doesn't exist in session_state
    session_state['trend_engine'] = session_state.get('trend_engine', 'GPT')
    # Initialize video_engine if it doesn't exist in session_state
    session_state['video_engine'] = session_state.get('video_engine', 'D-ID')
    # Initialize last_uploaded_image if it doesn't exist in session_state
    session_state['last_uploaded_image'] = session_state.get('last_uploaded_image', '')
    trends = get_trends(query, session_state)
    selected_trend = trends[0]
    script = create_video_script(selected_trend)
    source_url = session_state.get('last_uploaded_image', '')
    video_url = generate_video(script, source_url)
    upload_video(video_url)
