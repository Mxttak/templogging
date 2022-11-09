from flask import Flask, abort, request, render_template
import os
import json
import copy
import datetime
import pandas as pd

import plotly
import plotly.graph_objects as go

from utils import get_logger, STATUS, Data, Config

logger = get_logger("app_logger")


this_dir = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(this_dir, "config.json")) as f:
    config = Config(**json.load(f))


app = Flask(__name__)


def _unix_time_to_string(unix_time: float) -> str:
    return datetime.datetime.utcfromtimestamp(unix_time).strftime("%Y-%m-%d %H:%M:%S")


@app.route("/")
def hello():
    if os.path.exists(os.path.join(config.path_to_database)):
        data = pd.read_csv(config.path_to_database, sep=";")
        all_symbols = list(data["room"].unique())
        # data = data[data["room"].isin(all_symbols)]
        fig_temperature = go.Figure()
        fig_humidity = go.Figure()
        for symbol in all_symbols:
            fig_temperature.add_trace(
                go.Scatter(
                    x=[
                        _unix_time_to_string(d)
                        for d in data[data["room"] == symbol]["timestamp"]
                    ],
                    y=data[data["room"] == symbol]["temperature"],
                    name=symbol,
                )
            )
            fig_humidity.add_trace(
                go.Scatter(
                    x=[
                        _unix_time_to_string(d)
                        for d in data[data["room"] == symbol]["timestamp"]
                    ],
                    y=data[data["room"] == symbol]["humidity"],
                    name=symbol,
                )
            )

        fig_temperature.update_layout(
            title="Temperature",
            xaxis_title="timestamp",
            yaxis_title="temperature in °C",
            legend_title="Rooms",
            font=dict(family="Courier New, monospace", size=18, color="RebeccaPurple"),
        )

        fig_humidity.update_layout(
            title="Humidity",
            xaxis_title="timestamp",
            yaxis_title="humidity in RH%",
            legend_title="Rooms",
            font=dict(family="Courier New, monospace", size=18, color="RebeccaPurple"),
        )

        temperature_graph = json.dumps(
            fig_temperature, cls=plotly.utils.PlotlyJSONEncoder
        )
        humidity_graph = json.dumps(fig_humidity, cls=plotly.utils.PlotlyJSONEncoder)
        return render_template(
            "index.html",
            temperature_graph_json=temperature_graph,
            humidity_graph_json=humidity_graph,
        )
    return "No data to display"


@app.route("/api_v1/<token>/upload_data", methods=["POST"])
def upload_data(token):
    if token not in config.admissible_tokens:
        logger.error(f"Not admitted token={token} requested post")
        abort(STATUS.FORBIDDEN)

    logger.info(f"Admitted token={token} requested post: {request.json}")

    # add time stamp to received data
    stamped_data = copy.deepcopy(request.json)
    stamped_data["timestamp"] = datetime.datetime.timestamp(datetime.datetime.utcnow())

    # write data to databse
    data = Data(**stamped_data)
    if not os.path.exists(config.path_to_database):
        with open(config.path_to_database, "w") as f:
            f.write(data.data_keys + "\n")
    with open(config.path_to_database, "a") as f:
        f.write(data.data_to_row + "\n")
        response = ({}, STATUS.CREATED)
        return response
    logger.error(f"Failed to write data for token={token}")
    abort(STATUS.FAIL)
