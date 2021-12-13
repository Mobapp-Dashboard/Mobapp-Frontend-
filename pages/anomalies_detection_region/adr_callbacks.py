#!/usr/bin/env ipython

import dash_bootstrap_components as dbc
import dash
import plotly.express as px
import plotly.graph_objects as go
from app import app
from dash.dependencies import Input, Output, State

from . import adr_data as data


def trajectory_2_fig(df, dfa, dfr):

    # fig = px.scatter_mapbox()
    #        df, lat="lat", lon="lng", mode="marker+line",
    #        height=600)
    #
    #    fig.add_trace(go.Scattermapbox(

    fig = go.Figure(
        go.Scattermapbox(
            name="Trajetória Realizada",
            lat=df["lat"],
            lon=df["lng"],
            mode="markers+lines",
            marker=go.scattermapbox.Marker(size=8, color="rgb(0, 100, 142)", opacity=1),
        )
    )
    fig.add_trace(
        go.Scattermapbox(
            name="Ponto Inicial",
            lat=[df["lat"].iloc[0]],
            lon=[df["lng"].iloc[0]],
            mode="markers",
            marker=go.scattermapbox.Marker(
                size=18, color="rgb(0, 100, 142)", opacity=1,
            ),
        )
    )
    fig.add_trace(
        go.Scattermapbox(
            name="Trajeto Esperado",
            lat=dfr["lat"],
            lon=dfr["lng"],
            mode="markers+lines",
            visible="legendonly",
            marker=go.scattermapbox.Marker(
                size=8, color="rgb(175, 100, 42)", opacity=0.5
            ),
        )
    )
    fig.add_trace(
        go.Scattermapbox(
            name="Anomalias",
            lat=dfa["lat"],
            lon=dfa["lng"],
            mode="markers+lines",
            marker=go.scattermapbox.Marker(
                size=11, color="rgb(175, 0, 42)", opacity=0.5
            ),
        )
    )

    fig.update_layout(
        mapbox_style="open-street-map",
        mapbox_zoom=11,
        mapbox_center_lat=df["lat"].iloc[100],
        mapbox_center_lon=df["lng"].iloc[100],
        height=700,
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        legend_orientation="h",
    )

    return fig



@app.callback(
    Output("map_adr", "figure"),
    Input("button_adr", "n_clicks"),
    [State("drop_rota", "value"),
     State("drop_traj", "value"),
     State("drop_model_name", "value")],
)
def update_graph_model(n_clicks, rota, traj, model):
    dfa = data.anom_by_model_route(model, rota)

    dft = data.traj_by_rota_traj(rota, traj)

    if traj >= 50:
        df1 = data.traj_by_rota_traj(rota, traj % 50)
    else:
        df1 = dft

    anon_idx = data.extract_anon_idx(dfa, traj)
    #compare = list(map(lambda x, y: x != y, dft["predicted"], dft["input_token"]))
    dft.reset_index(inplace=True)
    compare = dft.index.isin(anon_idx)
    return trajectory_2_fig(dft, dft[compare], df1)
