#!/usr/bin/env ipython
import requests
import pandas as pd

from environment.settings import BACKEND



def line_journey_2_trajectory(traj):
    url  = f"http://{BACKEND}/api/v1/dublin_points/trajectory/{traj}"
    r = requests.get(url).json()
    df = pd.DataFrame(r)
    return df.sort_values("instant")

def jouney_turno_2_trajectory(journey, turno):
    url = f"http://{BACKEND}/api/v1/dublin_points/points/?journey_id={journey}&turno={turno}"
    r = requests.get(url).json()
    df = pd.DataFrame(r)
    return df.sort_values("instant")
