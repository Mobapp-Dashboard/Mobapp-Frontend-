#!/usr/bin/env ipython

import pandas as pd
import requests

import plotly.express as px
import plotly.graph_objects as go
from app import app
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import dash_html_components as html
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
        animation_frame="trajectory_id")

    fig.update_layout(
        mapbox_style="open-street-map",
        mapbox_zoom=11,
        mapbox_center_lat=53.3460,
        #df["lat"].iloc[100],
        mapbox_center_lon=-6.3474,
        height=800,
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
              Input("route-model", "value"))
def update_map_rota(rota):
    df = data.trajs_by_rota(rota)

    fig = rota_2_fig(df)
    return fig


@app.callback(
    Output("map-ad", "figure"),
    [Input("route-model", "value"),
     Input("traj-model", "value")],
)
def update_graph_model(rota, traj):
    df = data.traj_by_rota_traj(rota, traj)

    if traj >= 50:
        df1 = data.traj_by_rota_traj(rota, traj % 50)
    else:
        df1 = df

    compare = list(map(lambda x, y: x != y, df["predicted"], df["input_token"]))

    return trajectory_2_fig(df, df[compare], df1)


def df_to_pr_curve(dfs):
    fig = go.Figure()

    models = ["riobusdata", "gmvsae", "iboat", "transformer"]

    for m in models:
        df = dfs[dfs["model"] == m]
        precision = df["precision"].values
        recall = df["recall"].values
        #auc = df["auc"].unique()[0]
        auc = 666

        fig.add_trace(go.Scatter(
            x=recall, y=precision,
            name= f"{m}",
            mode="lines+markers",
            text = ['Threshold {}'.format(i) for i in df["threshold"]],
        ))
    fig.add_shape(
        type='line', line=dict(dash='dash'),
        x0=0, x1=1, y0=1, y1=0
    )
    fig.update_layout(
        xaxis_title='Recall',
        yaxis_title='Precision',
        yaxis=dict(scaleanchor="x", scaleratio=1),
        xaxis=dict(constrain='domain'),
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        legend_orientation="h"
        #width=700, height=500
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
    Input("route-model", "value")
)
def update_pr_curve(rota):
    df = data.get_eval(rota)
    fig = df_to_pr_curve(df)
    return fig


def trajectory_2_fig(df, dfr):

    fig = go.Figure(
        go.Scattermapbox(
            name="Real Trajectory",
            lat=df["lat"],
            lon=df["lng"],
            mode="markers+lines",
            marker=go.scattermapbox.Marker(size=8, color="rgb(0, 100, 142)", opacity=1),
        )
    )
    fig.add_trace(
        go.Scattermapbox(
            name="Initial Point",
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
            name="Expected Trajectory",
            lat=dfr["lat"],
            lon=dfr["lng"],
            mode="markers+lines",
            visible="legendonly",
            marker=go.scattermapbox.Marker(
                size=8, color="rgb(175, 100, 42)", opacity=0.5
            ),
        )
    )
    points = int(len(df)/2)
    fig.update_layout(
        mapbox_style="open-street-map",
        mapbox_zoom=12,
        mapbox_center_lat=53.3670,
        #df["lat"].iloc[100],
        mapbox_center_lon=-6.2957,
        # mapbox_zoom=9.8,
        # mapbox_center_lat=df["lat"].iloc[points],
        # mapbox_center_lon=df["lng"].iloc[points],
        height=800,
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        legend_orientation="h",
    )

    return fig


@app.callback(
    Output("map-traj", "figure"),
    [Input("models", "value"),
     Input("route-model", "value"),
     Input("traj-model", "value")],
)
def update_graph_modeles(model, rota, traj):
    dft = data.traj_by_rota_traj(rota, traj)

    if traj >= 50:
        df1 = data.traj_by_rota_traj(rota, traj % 50)
    else:
        df1 = dft

    dft.reset_index(inplace=True)

    fig = trajectory_2_fig(dft, df1)
    return fig

@app.callback(
#    [Output("thr-model", "marksoptions"),
#     Output("thr-model", "value")],
    [Output("thr-model", "marks"),
     Output("thr-model", "min"),
     Output("thr-model", "max"),
     Output("thr-model", "value")],
    [Input("route-model", "value"),
     Input("models", "value")]
)
def thresholds_for_model(route, model):
    df = data.get_eval(route)
    df = df[(df["threshold"].notna()) & (df["model"]==model)]

    thresholds = df["threshold"].unique()
    thresholds.sort()

    #thrs_opt = [{'label': f"Threshold: {thr}", "value": thr} for thr in thresholds]
    thrs_opt = {t: "" for t in thresholds}

    max_t = max(thresholds)
    value_t = min_t = min(thresholds)

    return (thrs_opt, min_t, max_t, value_t)

@app.callback(
    Output("pred-title", "children"),
    [Input("models", "value"),
     Input("thr-model", "value"),
     Input("route-model", "value"),
     Input("traj-model", "value")],
)
def prediction_title_generator(model, threshold, route, traj):


    row1 = html.Tr([html.Td("Route"), html.Td(route)])
    row2 = html.Tr([html.Td("Trajectory"), html.Td(traj)])

    if (model=="iboat"):
        anomaly_direction = "Above"
    else:
        anomaly_direction = "Below"

    row3 = html.Tr([html.Td("Model"), html.Td(model)])
    row4 = html.Tr([html.Td("Anomaly Direction"), html.Td(f"{anomaly_direction} threshold")])
    row5 = html.Tr([html.Td("Threshold"), html.Td(threshold)])

    df1 = data.get_eval(route)
    df1 = df1[(df1["route"]==route) & (df1["model"] == model)]
    _thr = df1[df1["threshold"]>=threshold]["threshold"].min()
    precision, recall = df1[df1["threshold"]==_thr][["precision", "recall"]].values[0]

    row6= html.Tr([html.Td("Precision / Recall (on route)"), html.Td(f"{precision} / {recall}")])

    df = data.score_by_route(route)
    score = df[(df["model"] == model) & (df["trajectory_id"] == traj)]["scores"].values
    #score = 0.8

    row7 = html.Tr([html.Td("Score"), html.Td(score)])

    result = result_by_method(model, score, threshold )

    row8 = html.Tr([html.Td("Result"), html.Td(f"Anomaly {result}")])

    table_body = [html.Tbody([row1, row2, row3, row4, row5, row6, row7, row8])]

    table = dbc.Table(table_body, bordered=True)


    return table

def result_by_method(model, score, thr):
    if (model == "iboat"):
        if score < thr:
            return "NOT DETECTED"
        else:
            return  "DETECTED"
    else:
        if thr < score :
            return "NOT DETECTED"
        else:
            return  "DETECTED"
