"""
5G data from RasperryPi Modul Streamlit Page
Created:
    27.03.2025

Author:
    Rajevan Raveendran

Copyright:
    MotionMiners GmbH, Emil-Figge Str. 80, 44227 Dortmund, 2021
"""

import streamlit as st

from devices.antenna import Sensor5g
from utils.sign import sign

sign()
st.title("Website for 5g Data")


filepath = st.text_input("Insert path to folder from 5G Sensor(recording.data type).")

raspberry_nr = st.selectbox(
    "Which device you want to see?", ("klinet-rpi-1", "klinet-rpi-2")
)


if filepath and raspberry_nr:
    antenna5g = Sensor5g(file_path=filepath, device=raspberry_nr)
    antenna5g.main()
    fig = antenna5g.show_fig()
    st.plotly_chart(fig)
