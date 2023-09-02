import streamlit as st
import json
from datetime import datetime
import os


st.title("Schedule a Post")

# User input for topic, date, and time
topic = st.text_input("Topic")
date = st.date_input("Date", min_value=datetime.today())
time = st.time_input("Time")

if st.button("Confirm"):

    # Check if the file exists, if not, create it
    if not os.path.isfile('scheduled_posts.json'):
        with open('scheduled_posts.json', 'w') as file:
            json.dump({}, file)

    with open('scheduled_posts.json', 'r+') as file:
        # First we load existing data into a dict.
        file_data = json.load(file)
        # Join new_data with file_data
        file_data[topic] = {"date": str(date), "time": str(time)}
        # Sets file's current position at offset.
        file.seek(0)
        # convert back to json.
        json.dump(file_data, file, indent=4)

# Display scheduled posts and delete option
with open('scheduled_posts.json', 'r') as file:
    scheduled_posts = json.load(file)
    for topic in list(scheduled_posts.keys()):
        details = scheduled_posts[topic]
        st.write(f"Topic: {topic}, Date: {details['date']}, Time: {details['time']}")
        if st.button(f"Delete {topic}"):
            # Delete the scheduled post from the JSON file
            del scheduled_posts[topic]
            with open('scheduled_posts.json', 'w') as file:
                json.dump(scheduled_posts, file, indent=4)
