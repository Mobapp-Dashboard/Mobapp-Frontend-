#!/usr/bin/env ipython

from app import app
from dash.dependencies import Input, Output, State

import requests
import pandas as pd

from environment.settings import BACKEND
from app import cache
from utils.extract_data import get_traj

def traj_by_traj(traj):
    url  = f"http://{BACKEND}/api/v1/dublin_points/trajectory/{traj}"
    df = get_traj(url)
    return df

def traj_by_journey(journey):
    url = f"http://{BACKEND}/api/v1/dublin_points/points/?journey_id={journey}"
    df = get_traj(url)
    return df

def traj_by_journey_date(journey, start_date, end_date):
    url = f"http://{BACKEND}/api/v1/dublin_points/points/?journey_id={journey}&start_date={start_date}&end_date={end_date}"
    df = get_traj(url)
    print("~")
    print(df["day"].unique())
    return df

def get_from_store(json_df):
    df = pd.read_json(json_df, orient='split')
    print (len(df))
    return df

@app.callback(
    Output("DataFrames", "data"),
    Input("submit_button", "n_clicks"),
    [State('radio_journey_1', 'value'),
     State('radio_traj_1', 'value'),
     State("radio_grao", "value"),
     State('date-range', 'start_date'),
     State('date-range', 'end_date')]
)
def store_dataframe(n_clicks, journey, traj, grao, start_date, end_date):
    if grao:
        df = traj_by_journey_date(journey, start_date, end_date)
    print(df.iloc[100])
    return df.to_json(date_format='iso', orient='split')
