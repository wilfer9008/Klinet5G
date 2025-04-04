"""
5G data from Inova Streamlit Page
Created:
    28.03.2025

Author:
    Rajevan Raveendran

Copyright:
    MotionMiners GmbH, Emil-Figge Str. 80, 44227 Dortmund, 2021
"""

import streamlit as st

from devices.smartphone import Smartphone
from utils.sign import sign

sign()
st.title("Website for Inova Data")

file_path = st.text_input("Insert path to recording from Inova (recording.data type).")

device_name = st.text_input(
    "Input the device name from inova in the recordings (usually: inova_device)"
)

if file_path and device_name:
    smartphone = Smartphone(file_path, device=device_name)
    smartphone.load_data()
    fig = smartphone.show_figure()

    st.plotly_chart(fig)
