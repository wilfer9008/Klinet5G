"""
Position Data from Turtlebot Streamlit Page
Created:
    21.03.2025

Author:
    Rajevan Raveendran

Copyright:
    MotionMiners GmbH, Emil-Figge Str. 80, 44227 Dortmund, 2021
"""

import streamlit as st

from devices.turlebot import Turtlebot
from utils.sign import sign

sign()
st.title("Website for Turtlebot Data")


file_path: str = st.text_input("Insert path to file from turtlebot pos_data.json")

if file_path:
    turtlebot = Turtlebot(file_path=file_path)
    turtlebot.load_data()
    fig, start_time, end_time = turtlebot.plot_path_turtlebot()
    st.markdown(f"### Start Time of turtlebot: {start_time}")
    st.markdown(f"### End Time: {end_time}")

    st.plotly_chart(fig)
