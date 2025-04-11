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


st.set_page_config(page_title="Data Uploader & Viewer", layout="wide")
sign()

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

            for device in item.keys():
                col1, col2 = st.columns([1, 10])
                col2.markdown(f"**{device}**")
                for data_type in item[device].keys():
                    if data_type == "5g":
                        col1, col2 = st.columns([2, 10])
                        col2.markdown(f"**{data_type}**")
                        col1, col2 = st.columns([3, 10])
                        col2.code(item[device][data_type], language="text")
                    elif data_type == "ble":
                        col1, col2 = st.columns([2, 10])
                        col2.markdown(f"**{data_type}**")
                        col1, col2 = st.columns([3, 10])
                        col2.code(item[device][data_type], language="text")
                    elif data_type == "rssi":
                        col1, col2 = st.columns([2, 10])
                        col2.markdown(f"**{data_type}**")
                        col1, col2 = st.columns([3, 10])
                        col2.code(item[device][data_type], language="text")
                    elif data_type == "rsrp":
                        col1, col2 = st.columns([2, 10])
                        col2.markdown(f"**{data_type}**")
                        col1, col2 = st.columns([3, 10])
                        col2.code(item[device][data_type], language="text")


st.header("🔍 Data Visualization")
st.markdown("Enter the **absolute** file path to the data in the respective pages.")
st.markdown(
    "Navigate through the sidebar menu to the corresponding data source to view the plots."
)

st.sidebar.header("📁 Navigation")
st.sidebar.markdown("- Select a page to visualize the respective data.")
