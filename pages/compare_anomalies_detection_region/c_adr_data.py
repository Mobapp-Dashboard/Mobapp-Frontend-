#!/usr/bin/env ipython

import pandas as pd
import requests

from app import app, cache
from dash.dependencies import Input, Output, State
from environment.settings import BACKEND
from utils.extract_data import get_traj


def score_by_route(route):
    url = f"http://{BACKEND}/api/v1/anomaly_detection_models/scores/{route}"
    df = get_traj(url, sort_by=None)
    return df


def anom_by_model_route(model, route):
    url = f"http://{BACKEND}/api/v1/anomaly_detection_models/predictions/{model}/{route}"
    df = get_traj(url, sort_by="index")
    return df


def extract_anon_idx(df, traj):
    dft = df[df["trajectory_id"] == traj]
    anoms = dft["anom_predictions"].unique()[0]
    anoms = anoms.replace("{", "[").replace("}", "]")
    anoms = eval(anoms)
    return anoms


def traj_by_rota_traj(rota, traj):
    url = f"http://{BACKEND}/api/v1/anomaly_detection_models/model_points/?trajectory_id={traj}&rota={rota}"
    df = get_traj(url, sort_by="index")
    return df


def trajs_by_rota(rota):
    url = f"http://{BACKEND}/api/v1/anomaly_detection_models/model_points/?rota={rota}"
    df = get_traj(url, sort_by="index")
    return df


def get_eval(rota):
    models = ["riobusdata", "gmvsae", "transformer", "iboat"]
    dfs = []
    for m in models:
        url = (
            f"http://{BACKEND}/api/v1/anomaly_detection_models/evals/{m}/{rota}"
        )
        dfs.append(get_traj(url, sort_by="index"))
    return pd.concat(dfs)
