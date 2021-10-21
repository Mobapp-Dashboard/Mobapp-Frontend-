#!/usr/bin/env ipython

from datetime import date

import dash_table
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
        margin={"r": 0, "t": 0, "l": 0, "b": 0}
    )


def trajectories_to_fig(df, n=5):
    fig = px.scatter_mapbox(
        df,
        lat="lat", lon="lng",
        height=600,
        hover_data=['instant', "trajectory_id", "cum_dist"],
        color="speed", opacity=0.5, color_continuous_scale="Edge"
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
                mode='markers',
                marker=go.scattermapbox.Marker(**style)
            ))


def histogram_fig(df, cols):
    fig = go.Figure()
    for c in cols:
        fig.add_trace(go.Histogram(x=df[c]))
    # Overlay both histograms
    fig.update_layout(barmode='overlay')
    fig.update_traces(opacity=0.75)
    return fig

@app.callback(
    [Output('mapL', 'figure'),
     Output('cum_dist_time', 'figure')],
    Input("DataFrames", "data")
)
def update_graph_4x(json_df):
    df = data.get_from_store(json_df)
    map_fig = trajectories_to_fig(df)
    scatter_fig = scatter_dist_time(df)
    return map_fig, scatter_fig


def scatter_dist_time(df):
    fig = px.scatter(
        df, x="cum_dist", y="cum_time",
        hover_data=["trajectory_id"],
        color="speed", color_continuous_scale="Edge"
    )
    return fig
