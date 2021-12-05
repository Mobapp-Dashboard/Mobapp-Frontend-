#!/usr/bin/env ipython

import dash_bootstrap_components as dbc
import dash
import plotly.express as px
import plotly.graph_objects as go
from app import app
from dash.dependencies import Input, Output, State

from . import c_adr_data as data


def trajectory_2_fig(df, dfa, dfr):

    # fig = px.scatter_mapbox()
    #        df, lat="lat", lon="lng", mode="marker+line",
    #        height=600)
    #
    #    fig.add_trace(go.Scattermapbox(

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
    fig.add_trace(
        go.Scattermapbox(
            name="Detected Anomalies",
            lat=dfa["lat"],
            lon=dfa["lng"],
            mode="markers",
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
        height=600,
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        legend_orientation="h",
    )

    return fig



##########
##########
##########

@app.callback(
    Output("list-traj-scores", "children"),
    Input("route-drop-av", "value")
)
def top5_anomaly_scores(route):
    df = data.score_by_route(route)
    scores = df[df["model"] == "transformer"][["trajectory_id", "scores"]]
    scores = scores.sort_values("scores", ascending=True).iloc[:5]
    list_items = [dbc.ListGroupItem("Trajectory (SCORE)")]
    for n, ts in enumerate(scores.values):
        traj = ts[0]
        score = ts[1]
        list_items.append(
            dbc.ListGroupItem(
                f"Trajectory {traj} ({score})",
                id=f"item{n}", n_clicks=0, action=True,
                color="info"
            ))
    return list_items

@app.callback(
    Output("map_adr", "figure"),
    [
        Input("item0", "n_clicks"),
        Input("item1", "n_clicks"),
        Input("item2", "n_clicks"),
        Input("item3", "n_clicks"),
        Input("item4", "n_clicks"),
        Input("route-drop-av", "value")
    ]
)
def generate_map_from_score_list(i1, i2, i3, i4, i5, route):
    ctx = dash.callback_context
    df = data.score_by_route(route)
    scores = df[df["model"] == "transformer"][["trajectory_id", "scores"]]
    scores = scores.sort_values("scores", ascending=True).iloc[:5]
    idx = int(ctx.triggered[0]["prop_id"].split(".")[0][-1])
    traj = int(scores.iloc[idx]["trajectory_id"])


    dfa = data.anom_by_model_route("transformer", route)

    dft = data.traj_by_rota_traj(route, traj)

    if traj >= 50:
        df1 = data.traj_by_rota_traj(route, traj % 50)
    else:
        df1 = dft

    anon_idx = data.extract_anon_idx(dfa, traj)
    #compare = list(map(lambda x, y: x != y, dft["predicted"], dft["input_token"]))
    dft.reset_index(inplace=True)
    compare = dft.index.isin(anon_idx)
    return trajectory_2_fig(dft, dft[compare], df1)






    # print(ctx.triggered[0]["prop_id"])
#    if ctx.triggered[0]["prop_id"].split(".")[0] == "item1":
#    return ctx.triggered[0]["prop_id"].split(".")[0][-1]





