#!/usr/bin/env ipython

from app import app
from dash.dependencies import Input, Output, State

import requests
import pandas as pd

from environment.settings import BACKEND
from app import cache
from utils.extract_data import get_traj


def traj_by_rota_traj(rota, traj):
    url = f"http://{BACKEND}/api/v1/dublin_model/meta_trajectory/?trajectory_id={traj}&routes={rota}"
    df = get_traj(url, sort_by="index")
    return df

def get_eval(rota):
    url = f"http://{BACKEND}/api/v1/dublin_model/evals/transformer/{rota}"
    df = get_traj(url, sort_by="index")
    return df
