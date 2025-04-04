"""
Bluetooth Data from Raspberry and Beacons connections Streamlit Page
Created:
    21.03.2025

Author:
    Rajevan Raveendran

Copyright:
    MotionMiners GmbH, Emil-Figge Str. 80, 44227 Dortmund, 2021
"""

import streamlit as st

from devices.raspberry import Raspberry
from utils.sign import sign

sign()
st.title("Website for Raspberry Pi Bluetooth Data")


filepath = st.text_input("Insert path to folder from Raspberry data.")
layout_json = st.text_input("Insert path from layout json from mpi.")

raspberry_nr = st.selectbox(
    "Which device you want to see?", ("klinet-rpi-1", "klinet-rpi-2")
)


if filepath and layout_json:
    raspberry = Raspberry(file_path=filepath, device=raspberry_nr)
    raspberry.main(layout_json=layout_json)
    fig = raspberry.show_figure()
    st.plotly_chart(fig)
