#!/usr/bin/env ipython

#!/usr/bin/env ipython

#!/usr/bin/env ipython

from environment.settings import BACKEND

from dash.dependencies import Input, Output, State

from app import app
from utils import request_functions as rf
from utils import figure_functions as ff

import requests
import pandas as pd
import plotly.express as px

import plotly.graph_objects as go

def trajectory_2_fig(df, dfa, dfr):

    #fig = px.scatter_mapbox()
#        df, lat="lat", lon="lng", mode="marker+line",
#        height=600)
#
#    fig.add_trace(go.Scattermapbox(

    fig = go.Figure(go.Scattermapbox(
        name="Trajetória Realizada",
        lat=df["lat"],
        lon=df["lng"],
        mode = "markers+lines",
        marker=go.scattermapbox.Marker(
            size=8,
            color='rgb(0, 100, 142)',
            opacity=1
        ),
    ))
    fig.add_trace(go.Scattermapbox(
        name="Ponto Inicial",
        lat=[df["lat"].iloc[0]],
        lon=[df["lng"].iloc[0]],
        mode = "markers",
        marker=go.scattermapbox.Marker(
            size=18,
            color='rgb(0, 100, 142)',
            opacity=1,
        ),
    ))
    fig.add_trace(go.Scattermapbox(
        name="Trajeto Esperado",
        lat=dfr["lat"],
        lon=dfr["lng"],
        mode = "markers+lines",
        visible = "legendonly",
        marker=go.scattermapbox.Marker(
            size=8,
            color='rgb(175, 100, 42)',
            opacity=0.5
        ),
    ))
    fig.add_trace(go.Scattermapbox(
        name="Anomalias",
        lat=dfa["lat"],
        lon=dfa["lng"],
        mode = "markers+lines",
        marker=go.scattermapbox.Marker(
            size=11,
            color='rgb(175, 0, 42)',
            opacity=0.5
        ),
    ))



    fig.update_layout(
        mapbox_style="open-street-map",
        mapbox_zoom=11,
        mapbox_center_lat = df["lat"].iloc[100],
        mapbox_center_lon = df["lng"].iloc[100],
        height=700,
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        legend_orientation="h")


    return fig

def get_traj(rota, traj):
    url = f"http://{BACKEND}/api/v1/dublin_model/meta_trajectory/?trajectory_id={traj}&routes={rota}"
    r = requests.get(url).json()
    df = pd.DataFrame(r)
    df = df.sort_values("index")
    return df


@app.callback(
    Output('map_ad', 'figure'),
    Input('model_button', 'n_clicks'),
    [State('rota_model', 'value'),
     State('traj_model', 'value')]
)
def update_graph_model(n_clicks, rota, traj):
    df = get_traj(rota, traj)
    if (traj >= 50):
        df1 = get_traj(rota, traj % 50)
    else:
        df1 = df

    compare = list(map(lambda x, y: x != y,
                       df["predicted"],
                       df["input_token"]))

    return trajectory_2_fig(df, df[compare], df1)

#@app.callback(
#    Output('map_ad_gt', 'figure'),
#    Input('model_button', 'n_clicks'),
#    [State('rota_model', 'value'),
#     State('traj_model', 'value')
#     ])
#def update_graph_model2(n_clicks, rota, traj):
#    traj = traj % 50
#    print(f"traj: {traj}")
#    url = f"http://{BACKEND}/api/v1/dublin_model/meta_trajectory/?trajectory_id={traj}&routes={rota}"
#    r = requests.get(url).json()
#    df = pd.DataFrame(r)
#    df = df.sort_values("index")
#    return trajectory_2_fig(df, None)
