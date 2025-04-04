"""
5g Sensor Class from Raspi Modul
Created:
    11.10.2024

Author:
    Rajevan Raveendran

Copyright:
    MotionMiners GmbH, Emil-Figge Str. 80, 44227 Dortmund, 2021
"""

import datetime
import json

import plotly.graph_objects as go


class Sensor5g:
    def __init__(
        self, file_path: str, device: str = "klinet-rpi-2", sensor: str = "nr5g"
    ):
        self.file_path = file_path
        self.device_filer = device
        self.sensor = sensor

    def load_data(self):
        # initate list
        timestamps = []

        # ╭──────────────────────────────────────────────────────────╮
        # │                        rsrp data                         │
        # ╰──────────────────────────────────────────────────────────╯
        rsrp_prx, rsrp_drx = [], []

        # ╭──────────────────────────────────────────────────────────╮
        # │                        rsrq data                         │
        # ╰──────────────────────────────────────────────────────────╯

        rsrq_prx, rsrq_drx = [], []

        # ╭──────────────────────────────────────────────────────────╮
        # │                        sinr data                         │
        # ╰──────────────────────────────────────────────────────────╯

        sinr_prx, sinr_drx = [], []

        with open(self.file_path, "rb") as f:
            data = f.readlines()
        for line in data:
            json_line_data = json.loads(line)

            if (
                json_line_data["device"] == self.device_filer
                and json_line_data["sensor"] == self.sensor
            ):
                rsrp = json_line_data["data"].get("rsrp", None)
                rsrq = json_line_data["data"].get("rsrq", None)
                sinr = json_line_data["data"].get("sinr", None)

                if rsrp == None or rsrq == None or sinr == None:
                    continue

                for (
                    i,
                    (antenna_rsrq, antenna_rsrp, antenna_sinr),
                ) in enumerate(zip(rsrp, rsrq, sinr)):
                    # get the timestamp
                    timestamp = datetime.datetime.strptime(
                        json_line_data["time"], "%Y-%m-%dT%H:%M:%S.%f"
                    ) + datetime.timedelta(hours=1)
                    timestamp = timestamp.timestamp()
                    timestamps.append(
                        int(timestamp * 1000) + i
                    )  # add timestamp and disturbution

                    # add rsrp
                    rsrp_prx.append(antenna_rsrp["prx"])
                    rsrp_drx.append(antenna_rsrp["drx"])

                    # add rsrq
                    rsrq_prx.append(antenna_rsrq["prx"])
                    rsrq_drx.append(antenna_rsrq["drx"])

                    # add sinr
                    sinr_prx.append(antenna_sinr["prx"])
                    sinr_drx.append(antenna_sinr["drx"])

        self.timestamps = timestamps
        self.datetimes = [
            datetime.datetime.fromtimestamp(ts / 1000) for ts in timestamps
        ]
        self.rsrp_prx = rsrp_prx
        self.rsrp_drx = rsrp_drx
        self.rsrq_prx = rsrq_prx
        self.rsrq_drx = rsrq_drx
        self.sinr_prx = sinr_prx
        self.sinr_drx = sinr_drx

        print(f"\nTotal Values in Klinet recorded file: {len(rsrp_prx) = }.\n")

    def show_fig(self):
        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=self.datetimes[::100],
                y=self.rsrp_prx[::100],
                mode="markers",
                name="rsrp_prx",
            )
        )
        return fig

    def main(self):
        self.load_data()
        self.show_fig()
