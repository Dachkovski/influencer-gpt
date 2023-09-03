import threading
import time
from workflow import automatic_workflow
import streamlit as st
from streamlit.runtime.scriptrunner import add_script_run_ctx

import json
from datetime import datetime
import os
import logging

logging.basicConfig(level=logging.INFO)


st.title("Schedule a Post")

# User input for topic, date, and time
topic = st.text_input("Topic")
date = st.date_input("Date", min_value=datetime.today())
time_input = st.time_input("Time")

if st.button("Confirm"):

    # Check if the file exists, if not, create it
    if not os.path.isfile('scheduled_posts.json'):
        with open('scheduled_posts.json', 'w') as file:
            json.dump({}, file)

    with open('scheduled_posts.json', 'r+') as file:
        # First we load existing data into a dict.
        file_data = json.load(file)
        # Join new_data with file_data
        file_data[topic] = {"date": str(date), "time": str(time_input)}
        # Sets file's current position at offset.
        file.seek(0)
        # convert back to json.
        json.dump(file_data, file, indent=4)

def check_schedules():
    logging.info("check_schedules function called")
    # Initialize trend_engine if it doesn't exist in st.session_state
    st.session_state['trend_engine'] = st.session_state.get('trend_engine', 'GPT')
    while True:
        with open('scheduled_posts.json', 'r') as file:
            scheduled_posts = json.load(file)
            for topic in list(scheduled_posts.keys()):
                details = scheduled_posts[topic]
                # Check if the current time is equal to or later than the scheduled time
                if datetime.now() >= datetime.strptime(details['date'] + ' ' + details['time'], '%Y-%m-%d %H:%M:%S'):
                    # Call the automatic_workflow function with the topic and st.session_state as the arguments
                    automatic_workflow(topic, st.session_state)
                    # Delete the scheduled post from the JSON file
                    del scheduled_posts[topic]
                    with open('scheduled_posts.json', 'w') as file:
                        json.dump(scheduled_posts, file, indent=4)
        time.sleep(60)  # Check every minute

# Start the check_schedules function in a new thread
def start_thread():
    logging.info("start_thread function called")
    if 'thread' not in st.session_state or not st.session_state['thread'].is_alive():
        logging.info("Starting a new thread")
        t1 = threading.Thread(target=check_schedules, daemon=True)
        add_script_run_ctx(t1)
        st.session_state['thread'] = t1
        st.session_state['thread'].start()

# Call the function to start the thread only if it's not already running
if 'thread' not in st.session_state or not st.session_state['thread'].is_alive():
    start_thread()

    

# Load the scheduled posts
with open('scheduled_posts.json', 'r') as file:
    scheduled_posts = json.load(file)

# Display the scheduled posts in separate rows with delete buttons
st.subheader("Scheduled Posts")
for topic in list(scheduled_posts.keys()):
    details = scheduled_posts.get(topic)
    cols = st.columns([4, 1])
    cols[0].markdown(f"**Topic:** {topic}  \n**Date:** {details['date']}  \n**Time:** {details['time']}")
    if cols[1].button("Delete", key=topic):
        # Delete the scheduled post from the JSON file
        del scheduled_posts[topic]
        with open('scheduled_posts.json', 'w') as file:
            json.dump(scheduled_posts, file, indent=4)
        st.success(f"Deleted scheduled post: {topic}")
