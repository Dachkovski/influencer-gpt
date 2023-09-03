from app import get_trends, create_video_script, generate_video, upload_video

def automatic_workflow(query, session_state):
    # Initialize trend_engine if it doesn't exist in session_state
    if 'trend_engine' not in session_state:
        session_state['trend_engine'] = 'GPT'
    # Initialize video_engine if it doesn't exist in session_state
    if 'video_engine' not in session_state:
        session_state['video_engine'] = 'D-ID'
    # Initialize last_uploaded_image if it doesn't exist in session_state
    if 'last_uploaded_image' not in session_state:
        session_state['last_uploaded_image'] = ''
    trends = get_trends(query)
    selected_trend = trends[0]
    script = create_video_script(selected_trend)
    source_url = session_state.get('last_uploaded_image', '')
    video_url = generate_video(script, source_url)
    upload_video(video_url)
