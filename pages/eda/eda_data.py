#!/usr/bin/env ipython

import pandas as pd
import requests

from app import app, cache
from dash.dependencies import Input, Output, State
from environment.settings import BACKEND
from utils.extract_data import get_traj


def traj_by_traj(traj):
    url = f"http://{BACKEND}/api/v1/gps_points/trajectory/{traj}"
    df = get_traj(url)
    return df


def traj_by_journey(journey):
    url = f"http://{BACKEND}/api/v1/gps_points/?dataset=dublin&journey_id={journey}"
    df = get_traj(url)
    return df


def traj_by_journey_date(journey, start_date, end_date):
    url = f"http://{BACKEND}/api/v1/gps_points/?dataset=dublin&journey_id={journey}&start_date={start_date}&end_date={end_date}"
    print(url)
    df = get_traj(url)
    return df


def get_from_store(json_df):
    df = pd.read_json(json_df, orient="split")
    return df


@app.callback(
    Output("DataFrames", "data"),
    Input("submit-button", "n_clicks"),
    [
        State("dropdown-journey", "value"),
        State("date-range", "start_date"),
        State("date-range", "end_date"),
    ],
)
def store_dataframe(n_clicks, journey, start_date, end_date):
    print(start_date)
    df = traj_by_journey_date(journey, start_date, end_date)
    return df.to_json(date_format="iso", orient="split")
