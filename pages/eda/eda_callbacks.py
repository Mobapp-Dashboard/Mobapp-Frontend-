#!/usr/bin/env ipython

from datetime import date
import json
import dash_bootstrap_components as dbc
import dash
import plotly.express as px
import plotly.graph_objects as go
from app import app
from dash.dependencies import Input, Output, State
from styles.style import POINT_FOCUS

from . import eda_data as data

style_first = POINT_FOCUS
style_first["color"] = "rgb(115,131,202)"
style_last = POINT_FOCUS.copy()
style_last["color"] = "rgb(115,131,202)"


def map_layout(fig):
    return fig.update_layout(
        mapbox_style="open-street-map",
        mapbox_zoom=12,
        legend_orientation="h",
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
    )


def trajectories_to_fig(df, n=5, cor="speed"):
    fig = px.scatter_mapbox(
        df,
        lat="lat",
        lon="lng",
        height=600,
        hover_data=["instant", "trajectory_id", "cum_dist"],
        color=cor,
        opacity=1,
        color_continuous_scale="Turbo",
    )
    map_layout(fig)

    return fig


def add_range_scatters(df, n, fig):
    for i in [n, -n]:
        style = style_first if (n > 0) else style_last
        fig.add_trace(
            go.Scattermapbox(
                lat=df["lat"].iloc[5:],
                lon=df["lng"].iloc[-5:],
                mode="markers",
                marker=go.scattermapbox.Marker(**style),
            )
        )


def histogram_fig(df, cols):
    fig = go.Figure()
    for c in cols:
        fig.add_trace(go.Histogram(x=df[c]))
    # Overlay both histograms
    fig.update_layout(
        xaxis_title='Cumulative Distance (meters)',
        yaxis_title='Cumulative Time (minutes)',
        barmode="overlay")
    fig.update_traces(opacity=0.75)
    return fig


@app.callback(
    [
        Output("mapL", "figure"),
        Output("cum-dist-time", "figure"),
        Output("radio-shift", "value"),
        Output("summary-table", "children"),
    ],
    [
        Input("submit-button", "n_clicks"),
        Input("reset-button", "n_clicks"),
        Input("DataFrames", "data"),
        Input("radio-shift", "value"),
        Input("radio-color", "value"),
        Input("mapL", "clickData"),
        Input("cum-dist-time", "clickData"),
    ],
)
def update_graph_4x(n_clicks, r_clicks, json_df, turno, cor, click_map, click_scatter):
    ctx = dash.callback_context

    # print(ctx.triggered[0]["prop_id"])
    if ctx.triggered[0]["prop_id"].split(".")[0] == "reset-button":
        click_map = None
        click_scatter = None
        turno = 0

    df = data.get_from_store(json_df)

    if click_map is not None:
        traj = click_map["points"][0]["customdata"][1]
        df = df[df["trajectory_id"] == traj]

    if click_scatter is not None:
        traj = click_scatter["points"][0]["customdata"][0]
        df = df[df["trajectory_id"] == traj]

    if turno != 0:
        turno_col = "turn"
        df = df[df[turno_col] == turno_dict[turno]]

    map_fig = trajectories_to_fig(df, cor=cor)
    scatter_fig = scatter_dist_time(df, cor=cor)

    # df = data.get_from_store(json_df)
    df = df[["speed", "acceleration", "delta_dist", "delta_time"]]
    dfs = df.describe()
    dfs.iloc[1:] = dfs.iloc[1:].applymap("{:,.2f}".format)
    dfs = dfs.reset_index()
    dfs.columns = [
        "",
        "Velocity(km/h)",
        "Acceleration(m/s^2)",
        "Distance between points(m)",
        "Time between points(s)",
    ]

    table = dbc.Table.from_dataframe(dfs, striped=True, bordered=True, hover=True)

    return map_fig, scatter_fig, turno, table


def scatter_dist_time(df, cor="speed"):
    fig = px.scatter(
        df,
        x="cum_dist",
        y="cum_time",
        hover_data=["trajectory_id"],
        color=cor,
        color_continuous_scale="Turbo",
    )
    fig.update_layout(
        xaxis_title='Cumulative Distance (meters)',
<<<<<<< HEAD
        yaxis_title='Cumulative Time (minutes)'
    )

=======
        yaxis_title='Cumulative Time (minutes)',
    )
>>>>>>> 662209622ad4225e8eb1ce491d173d5eb1a61ea2
    return fig


turno_dict = {1: "MANHÃ", 2: "TARDE", 3: "NOITE", 4: "MADRUGADA"}

# @app.callback(
#
#     Input("DataFrames", "data")
# )
# def tabela_sumario(json_df):
#
#    df = data.get_from_store(json_df)
#    df = df[["speed", "acceleration", "delta_dist", "delta_time"]]
#    dfs = df.describe()
#    dfs.iloc[1:] = dfs.iloc[1:].applymap("{:,.2f}".format)
#    dfs = dfs.reset_index()
#    dfs.columns = [
#        "Medida", "Velocidade (km/h)", "Aceleração(m/s^2)",
#        "Distância entre pontos (m)", "Tempo entre pontos (s)"
#    ]
#
#    dfs
#
#    table = dbc.Table.from_dataframe(dfs, striped=True, bordered=True, hover=True)
#    return table
#
