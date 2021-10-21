#!/usr/bin/env ipython

#!/usr/bin/env ipython

#!/usr/bin/env ipython
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
