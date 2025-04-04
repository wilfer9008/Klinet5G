"""
Raspberry Class to init bluetooth Class
Created:
    06.09.2024

Author:
    Rajevan Raveendran

Copyright:
    MotionMiners GmbH, Emil-Figge Str. 80, 44227 Dortmund, 2021
"""

import datetime
import json
from collections import defaultdict

import plotly.graph_objs as go


class Raspberry:
    def __init__(self, file_path: str, device: str = "klinet-rpi-2"):
        self.file_path = file_path
        self.device_filer = device

    def load_layout_beacons(self, layout_json: str):
        with open(layout_json, "r") as f:
            layout = json.load(f)

        # create check_beacons with contains all beacon ids from layout to checkup later with recording
        layout_beacons = layout["beacons"]
        check_beacons = []
        for layout_beacon in layout_beacons:
            check_beacons.append(layout_beacon["id"])
        print(
            f"\nSeen Beacons in layout file: {check_beacons}. The Total number of beacons is: {len(check_beacons) = }"
        )
        self.check_beacons = check_beacons

    def load_data(self):
        # initate list
        timestamps, rssis, macs, majors, minors, uuids = [], [], [], [], [], []

        with open(self.file_path, "rb") as f:
            print("loading data ....")
            data = f.readlines()
        for line in data:
            # print(f"{line = }")
            try:
                json_line_data = json.loads(line)
            except Exception:
                continue

            if json_line_data["device"] == self.device_filer:
                beacons = json_line_data["data"].get("beacons", None)

                if beacons == None:
                    continue

                # get the timestamp
                timestamp = datetime.datetime.strptime(
                    json_line_data["time"], "%Y-%m-%dT%H:%M:%S.%f"
                ) + datetime.timedelta(hours=1)
                timestamp = timestamp.timestamp()

                # loop over beacons in one timeframe
                for i, beacon in enumerate(beacons):
                    try:
                        if int(beacon["uuid"]) not in self.check_beacons:
                            continue
                    except AttributeError:
                        pass

                    # with i we add some distrubution to the time , so not all beacon has the same timestamp
                    try:
                        timestamps.append(int(timestamp * 1000) + i)  # add timestamp
                        rssis.append(beacon["rssi"])
                        macs.append(beacon["address"])
                        majors.append(2)
                        minors.append(1)
                        uuids.append(beacon["uuid"])
                    except KeyError:
                        continue

        print(
            f"\nSeen Beacons in Klinet recorded file: {set(uuids) = }. \nThe Total number of beacons is: {len(set(uuids)) = }"
        )
        difference_beacon = list(set(self.check_beacons) - set(uuids))

        print(
            f"\nLayout Beacons which are not in Raspberry Pi Recording: {difference_beacon} "
        )

        self.timestamps = timestamps
        self.datetimes = [
            datetime.datetime.fromtimestamp(ts / 1000) for ts in timestamps
        ]
        self.rssis = rssis
        self.macs = macs
        self.majors = majors
        self.minors = minors
        self.uuids = uuids

    def show_data(self):
        """
        INFO: need to run load_data() first before using this method
        """
        print(f"\n")
        print(f"{len(self.timestamps) = }")
        print(f"{len(self.rssis) = }")
        print(f"\n")

    def rssi_time_per_beacon(self):
        beacon_rssi = defaultdict(list)
        beacon_time = defaultdict(list)

        for uuid, rssi, datetime in zip(self.uuids, self.rssis, self.datetimes):
            beacon_rssi[uuid].append(rssi)
            beacon_time[uuid].append(datetime)

        self.beacon_rssi = beacon_rssi
        self.beacon_time = beacon_time

    def show_figure(self):
        fig = go.Figure()

        for uuid in self.beacon_rssi.keys():
            fig.add_trace(
                go.Scatter(
                    x=self.beacon_time[uuid][::100],
                    y=self.beacon_rssi[uuid][:100],
                    mode="markers",
                    name=uuid,
                )
            )

        # fig.show()
        return fig

    def main(self, layout_json: str):
        self.load_layout_beacons(layout_json=layout_json)
        self.load_data()
        self.rssi_time_per_beacon()
