"""
Turlebot Class to get data from pos_data.json recording
Created:
    06.09.2024

Author:
    Rajevan Raveendran

Copyright:
    MotionMiners GmbH, Emil-Figge Str. 80, 44227 Dortmund, 2021
"""

import datetime
import json
from pathlib import Path

import plotly.graph_objects as go
from rosbags.highlevel import AnyReader


class Turtlebot:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def load_data(self):
        with open(
            self.file_path,
            "r",
        ) as f:
            data = json.load(f)

        self.turtlebot_timestamp = data["timestamps"]
        self.turtlebot_x_coordinate = [float(x) for x in data["x"]]
        self.turtlebot_y_coordinate = [float(y) for y in data["y"]]
        self.plot_path_turtlebot()

    def load_rosbag_data(self, folder):

        # create reader instance and open for reading
        with AnyReader([Path(folder)]) as reader:
            connections = [x for x in reader.connections if x.topic == "/amcl_pose"]
            (
                turtlebot_timestamp,
                turtlebot_x_coordinate,
                turtlebot_y_coordinate,
                turtlebot_z_coordinate,
            ) = (
                [],
                [],
                [],
                [],
            )
            for connection, timestamp, rawdata in reader.messages(
                connections=connections
            ):
                msg = reader.deserialize(rawdata, connection.msgtype)

                turtlebot_timestamp.append(int(timestamp / 1e6))
                turtlebot_x_coordinate.append(msg.pose.pose.position.x)
                turtlebot_y_coordinate.append(msg.pose.pose.position.y)
                turtlebot_z_coordinate.append(msg.pose.pose.position.z)

            self.turtlebot_timestamp = turtlebot_timestamp

            self.turtlebot_x_coordinate = turtlebot_x_coordinate
            self.turtlebot_y_coordinate = turtlebot_y_coordinate
            self.turtlebot_z_coordinate = turtlebot_z_coordinate

        self.plot_path_turtlebot()

    def plot_path_turtlebot(
        self,
    ) -> tuple[go.Figure(), datetime.datetime, datetime.datetime]:
        fig = go.Figure()
        data_timestamp = [timestamp / 1000 for timestamp in self.turtlebot_timestamp]
        data_datetime = [datetime.datetime.fromtimestamp(ts) for ts in data_timestamp]

        fig.add_trace(
            go.Scatter(
                x=self.turtlebot_x_coordinate,
                y=self.turtlebot_y_coordinate,
                hovertext=data_datetime,
                hoverinfo="text",
                mode="markers+text",
                name="turtlebot path",
            )
        )

        # start point
        fig.add_trace(
            go.Scatter(
                x=[self.turtlebot_x_coordinate[0]],
                y=[self.turtlebot_y_coordinate[0]],
                marker_symbol="x",
                marker_size=15,
                name="start point",
            )
        )

        # end point
        fig.add_trace(
            go.Scatter(
                x=[self.turtlebot_x_coordinate[-1]],
                y=[self.turtlebot_y_coordinate[-1]],
                marker_symbol="x",
                marker_size=15,
                name="end point",
            )
        )
        start_time = data_datetime[0]
        end_time = data_datetime[-1]

        return fig, start_time, end_time

    def main(self, folder):
        self.load_rosbag_data(folder)
        fig, start_time, end_time = self.plot_path_turtlebot()

        return fig, start_time, end_time
