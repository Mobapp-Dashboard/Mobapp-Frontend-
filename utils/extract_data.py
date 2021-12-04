#!/usr/bin/env ipython
import pandas as pd
import requests
from app import cache

from environment.settings import BACKEND

def get_metatraj(journey, start_date, end_date):

    @cache.memoize()
    def query_and_serialize_metatraj(journey, start_date, end_date):
        url = f"http://{BACKEND}/api/v1/dublin_points/points/?journey_id={journey}&start_date={start_date}&end_date={end_date}"
        r = requests.get(url).json()
        df = pd.DataFrame(r)
        return df.to_json()

    return pd.read_json(query_and_serialize_metatraj(journey, start_date, end_date))


def get_journey_by_date(start_date, end_date):

    @cache.memoize()
    def query_and_serialize_journeys(start_date, end_date):
        url = f"http://{BACKEND}/api/v1/dublin_meta/journeys_by_date/?start_date={start_date}&end_date={end_date}"
        r = requests.get(url).json()
        df = pd.DataFrame(r)
        return df.to_json()

    return pd.read_json(query_and_serialize_journeys(start_date, end_date))


def get_traj_by_journey_date(journey, start_date, end_date):

    @cache.memoize()
    def query_and_serialize_trajs(journey, start_date, end_date):
        url = f"http://{BACKEND}/api/v1/dublin_meta/trajs_by_journey_date/?journey_id={journey}&start_date={start_date}&end_date={end_date}"

        r = requests.get(url).json()
        df = pd.DataFrame(r)
        return df.to_json()

    return pd.read_json(query_and_serialize_trajs(journey, start_date, end_date))


def get_traj(url, sort_by="instant"):
    @cache.memoize()
    def query_serialize_traj(url, sort_by="instant"):
        r = requests.get(url).json()
        df = pd.DataFrame(r)
        if (sort_by is not None):
            df = df.sort_values(sort_by)
        if (sort_by == "instant"):
            df = feat_eng(df)
        return df.to_json()

    return pd.read_json(query_serialize_traj(url, sort_by=sort_by))


def feat_eng(df):
    df = pd.concat(
        [cumsum_by_traj(_df) for _, _df in df.groupby("trajectory_id")]
    )
    return df


def cumsum_by_traj(df):
    df["cum_dist"] = df['delta_dist'].cumsum(axis=0)
    df["cum_time"] = df['delta_time'].cumsum(axis=0)
    df["speed"] = df["speed"] * 3.6
    df = df[df["speed"] < 100]
    df["cum_time"] = df["cum_time"] / 60
    return df
