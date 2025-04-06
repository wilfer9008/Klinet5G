"""
Documentation Page from Streamlit to load info.json file from dataset and get all the necessary information shown
Created:
    03.04.2025

Author:
    Rajevan Raveendran

Copyright:
    MotionMiners GmbH, Emil-Figge Str. 80, 44227 Dortmund, 2021
"""

import json
import streamlit as st
from utils.sign import sign

# ╭──────────────────────────────────────────────────────────╮
# │              special constant in info.json               │
# ╰──────────────────────────────────────────────────────────╯
# devices = ["5g_rpi1","5g_rpi2","5g_inova"]

sign()
st.set_page_config(page_title="Data Uploader & Viewer", layout="wide")

st.title("📊 Streamlit Application for Raw Data Analysis")
st.markdown(
    "This application allows you to upload and visualize raw data from various sources:"
)
st.markdown("- TurtleBot")
st.markdown("- Raspberry Pi Bluetooth")
st.markdown("- Raspberry Pi 5G")
st.markdown("- Inova 5G")

st.header("📂 Data Sources Overview")
info_path = st.text_input(
    "Enter the **absolute** path to the `info.json` file from your dataset:"
)

data_paths = {}
if info_path:
    try:
        with open(info_path, "r") as f:
            data_paths = json.load(f)
        st.success("Data loaded successfully!")
    except Exception as e:
        st.error(f"Error loading file: {e}")

if data_paths:
    for key, item in data_paths.items():

        if key == "devices":
            st.markdown(f"**{key} raw data in:**")
            st.code(item["raw"], language="text")
            del item["raw"]
            st.markdown(f"This file contains data for: {item.keys()} ")

            # TODO: check if raspi has 5g and ble data
            # if "5g_rpi1" in item.keys():
            #     st.markdown(f"5g_rpi1 has data collected for: {item.keys()} ")
            #
            # if "5g_rpi2" in item.keys():
            #     st.markdown(f"5g_rpi1 has data collected for: {item.keys()} ")


st.header("🔍 Data Visualization")
st.markdown("Enter the **absolute** file path to the data in the respective pages.")
st.markdown(
    "Navigate through the sidebar menu to the corresponding data source to view the plots."
)

st.sidebar.header("📁 Navigation")
st.sidebar.markdown("- Select a page to visualize the respective data.")
