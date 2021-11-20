#!/usr/bin/env ipython

import pandas as pd
import requests

import plotly.express as px
import plotly.graph_objects as go
from app import app
from dash.dependencies import Input, Output, State
from environment.settings import BACKEND
from utils import figure_functions as ff
from utils import request_functions as rf

from . import eval_model_data as data


def _rota_2_fig(df):
    dfn = df[df["trajectory_id"] < 50]
    dfa = df[df["trajectory_id"] >= 50]
    fig = go.Figure(
        go.Scattermapbox(
            name="Rotas sem Anomalias",
            lat=dfn["lat"],
            lon=dfn["lng"],
            mode="markers",
            marker=go.scattermapbox.Marker(size=8, color="rgb(0, 100, 142)", opacity=1),
        )
    )

    fig.add_trace(
        go.Scattermapbox(
            name="Trajetos com Anomalias",
            lat=dfa["lat"],
            lon=dfa["lng"],
            mode="markers",
            visible="legendonly",
            marker=go.scattermapbox.Marker(
                size=8, color="rgb(175, 0, 42)", opacity=0.5
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

def rota_2_fig(df):
    fig = px.scatter_mapbox(
        df, lat="lat", lon="lng",
        height=600, animation_frame="trajectory_id")

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
#
#    px.scatter(df, x="gdpPercap", y="lifeExp", animation_frame="year", animation_group="country",
#           size="pop", color="continent", hover_name="country",
#           log_x=True, size_max=55, range_x=[100,100000], range_y=[25,90])


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


@app.callback(Output("map-route", "figure"),
              Input("button-model", "n_clicks"),
              State("route-model", "value"))
def update_map_rota(n_clicks, rota):
    print("oi")
    df = data.trajs_by_rota(rota)
    fig = rota_2_fig(df)
    return fig


@app.callback(
    Output("map-ad", "figure"),
    Input("button-model", "n_clicks"),
    [State("route-model", "value"),
     State("traj-model", "value")],
)
def update_graph_model(n_clicks, rota, traj):
    df = data.traj_by_rota_traj(rota, traj)

    if traj >= 50:
        df1 = data.traj_by_rota_traj(rota, traj % 50)
    else:
        df1 = df

    compare = list(map(lambda x, y: x != y, df["predicted"], df["input_token"]))

    return trajectory_2_fig(df, df[compare], df1)


def df_to_pr_curve(dfs):
    fig = go.Figure()

    fig.add_shape(
        type='line', line=dict(dash='dash'),
        x0=0, x1=1, y0=1, y1=0
    )
    models = ["transformer", "riobusdata", "gmvsae"]

    for m in models:
        df = dfs[dfs["model"] == m]
        precision = df["precision"].values
        recall = df["recall"].values
        #auc = df["auc"].unique()[0]
        auc = 666

        fig.add_trace(go.Scatter(
            x=recall, y=precision,
            name= f"{m} (AUC={auc:.4f})",
            mode="lines+markers"
        ))
    fig.update_layout(
        xaxis_title='Recall',
        yaxis_title='Precision',
        yaxis=dict(scaleanchor="x", scaleratio=1),
        xaxis=dict(constrain='domain'),
        width=700, height=500
    )
        #fig = px.area(
        #    x=recall, y=precision,
        #    title=f'Precision-Recall Curve (AUC={auc:.4f})',
        #    labels=dict(x='Recall', y='Precision'),
        #    width=700, height=500
                   #)


    #fig.update_yaxes(scaleanchor="x", scaleratio=1)
    #fig.update_xaxes(constrain='domain')
    return fig

@app.callback(
    Output("p-rec", "figure"),
    Input("button-model", "n_clicks"),
    [State("route-model", "value")]
)
def update_pr_curve(n_clicks, rota):
    df = data.get_eval(rota)
    fig = df_to_pr_curve(df)
    return fig
