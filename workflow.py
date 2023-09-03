import logging
from app.get_trends import get_trends
from app.create_video_script import create_video_script
from app.generate_video import generate_video
from app.upload_video import upload_video

logging.basicConfig(level=logging.INFO)

def automatic_workflow(query, session_state):
    logging.info('Starting automatic workflow...')
    # Initialize trend_engine if it doesn't exist in session_state
    session_state['trend_engine'] = session_state.get('trend_engine', 'GPT')
    logging.info(f'Set trend_engine to {session_state["trend_engine"]}')
    # Initialize video_engine if it doesn't exist in session_state
    session_state['video_engine'] = session_state.get('video_engine', 'D-ID')
    logging.info(f'Set video_engine to {session_state["video_engine"]}')
    # Initialize last_uploaded_image if it doesn't exist in session_state
    session_state['last_uploaded_image'] = session_state.get('last_uploaded_image', '')
    logging.info(f'Set last_uploaded_image to {session_state["last_uploaded_image"]}')
    trends = get_trends(query, session_state)
    selected_trend = trends[0]
    logging.info(f'Selected trend: {selected_trend}')
    script = create_video_script(selected_trend)
    logging.info('Created video script')
    source_url = session_state.get('last_uploaded_image', '')
    #video_url = generate_video(script, source_url)
    #logging.info('Generated video')
    #upload_video(video_url)
    #logging.info('Uploaded video')
    logging.info('Finished automatic workflow')
