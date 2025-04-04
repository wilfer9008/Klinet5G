"""
Smartphone Inova Class
Created:
    06.09.2024

Author:
    Rajevan Raveendran

Copyright:
    MotionMiners GmbH, Emil-Figge Str. 80, 44227 Dortmund, 2021
"""

import collections
import datetime
import json

import plotly.graph_objects as go


class Smartphone:
    def __init__(self, file_path: str, sensor: str = "inova", device: str = "inova_device"):
        self.file_path = file_path
        self.device_filter = device
        self.sensor = sensor

    def load_data(self):
        with open(self.file_path, "rb") as f:
            data = f.readlines()

        data_timestamp = []  # list for timestamp in seconds
        cell_nr_per_timestamp_unique_id = (
            []
        )  # list with number of seen cells per timestamp
        cells_dict_rssi_with_time = collections.defaultdict(
            list
        )  # unique cell id key  with corresponding time and rssi value

        for line in data:
            json_line_data = json.loads(line)
            if json_line_data["device"] == self.device_filter:
                cells = json_line_data["data"]["data"]["data"] # TODO:add that to normal data then later and exception 

                # get the timestamp
                timestamp = datetime.datetime.strptime(
                    json_line_data["time"], "%Y-%m-%dT%H:%M:%S.%f"
                ) + datetime.timedelta(hours=2)
                timestamp = timestamp.timestamp()

                if cells == None:
                    continue

                data_timestamp.append(timestamp)

                # loop over cell in cells list

                cell_ids = []
                print(cells)
                print(cells)
                for cell in cells:
                    print("letsgoo2")
                    print(f"{cell['rssi'] =}")
                    print(f"{type(cell['rssi']) = }")
                    cells_dict_rssi_with_time[cell["cellUniqueId"]].append(
                        {timestamp: cell["rssi"]}
                    )
                    cell_ids.append(cell["cellUniqueId"])

                cell_nr_per_timestamp_unique_id.append(len(set(cell_ids)))

        self.data_timestamp = data_timestamp
        self.cell_nr_per_timestamp_unique_id = cell_nr_per_timestamp_unique_id
        self.cells_dict_rssi_with_time = cells_dict_rssi_with_time

    def show_data(self):
        pass

    def show_figure(self):
        fig_rssi = go.Figure()
        for cell in self.cells_dict_rssi_with_time:
            time = []
            rssi = []

            pair_values = self.cells_dict_rssi_with_time[cell]
            lenght = len(pair_values)
            for pair in pair_values:
                for key, value in pair.items():
                    time.append(key)
                    rssi.append(value)

            time_datetime = [datetime.datetime.fromtimestamp(ts) for ts in time]

            fig_rssi.add_trace(
                go.Scatter(
                    x=time_datetime, y=rssi, mode="markers", name=f"{cell}:{lenght}"
                )
            )

        fig_rssi.update_layout(
            title=f"Inova 5G Recording : rssi per cell over timestamp | FILE: {self.file_path}",
            xaxis_title="time",
            yaxis_title="rssi[dBm]",
        )

        fig_rssi.show()

        return fig_rssi

    def main(self):
        self.load_data()
        self.show_figure()

        
