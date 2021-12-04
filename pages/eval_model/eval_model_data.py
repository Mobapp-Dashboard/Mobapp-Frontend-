#!/usr/bin/env ipython

from app import app
from dash.dependencies import Input, Output, State

import requests
import pandas as pd

from environment.settings import BACKEND
from app import cache
from utils.extract_data import get_traj



def score_by_route(route):
    url = f"http://{BACKEND}/api/v1/dublin_model/scores/{route}"
    df = get_traj(url, sort_by=None)
    return df

def traj_by_rota_traj(rota, traj):
    url = f"http://{BACKEND}/api/v1/dublin_model/model_points/?trajectory_id={traj}&rota={rota}"
    df = get_traj(url, sort_by="index")
    return df

def trajs_by_rota(rota):
    url = f"http://{BACKEND}/api/v1/dublin_model/model_points/?rota={rota}"
    df = get_traj(url, sort_by="index")
    print(len(df))
    return df

def get_eval(rota):
    models = ["riobusdata", "gmvsae", "iboat", "transformer"]
    dfs = []
    for m in models:
        url = f"http://{BACKEND}/api/v1/dublin_model/evals/{m}/{rota}"
        dfs.append(get_traj(url, sort_by="index"))
    df = pd.concat(dfs)
    return df
