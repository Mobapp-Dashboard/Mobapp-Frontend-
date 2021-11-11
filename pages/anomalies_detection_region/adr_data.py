#!/usr/bin/env ipython

from app import app
from dash.dependencies import Input, Output, State

import requests
import pandas as pd

from environment.settings import BACKEND
from app import cache
from utils.extract_data import get_traj

def anom_by_model_route(model, route):
    url = f"http://{BACKEND}/api/v1/dublin_model/predictions/{model}/{route}"
    df = get_traj(url, sort_by="index")
    return df


def extract_anon_idx(df, traj):
    dft = df[df["trajectory_id"] == traj]
    anoms = dft["anon_predictions"].unique()[0]
    anoms = anoms.replace("{","[").replace("}","]")
    anoms = eval(anoms)
    return anoms

def traj_by_rota_traj(rota, traj):
    url = f"http://{BACKEND}/api/v1/dublin_model/meta_trajectory/?trajectory_id={traj}&routes={rota}"
    df = get_traj(url, sort_by="index")
    return df

def trajs_by_rota(rota):
    url = f"http://{BACKEND}/api/v1/dublin_model/meta_trajectory/?routes={rota}"
    df = get_traj(url, sort_by="index")
    return df

def get_eval(rota):
    models = ["transformer", "riobusdata", "gmvsae"]
    dfs = []
    for m in models:
        url = f"http://{BACKEND}/api/v1/dublin_model/evals/{m}/{rota}"
        dfs.append(get_traj(url, sort_by="index"))
    return pd.concat(dfs)
