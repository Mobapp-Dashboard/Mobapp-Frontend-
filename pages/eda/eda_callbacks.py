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
    Output('mapL', 'figure'),
    Input('submit_button', 'n_clicks'),
    [State('radio_journey_1', 'value'),
     State('radio_traj_1', 'value'),
     State("radio_grao", "value"),
     State('date-range', 'start_date'),
     State('date-range', 'end_date')]
)
def update_graph_4x(n_clicks, journey, traj, grao, start_date, end_date):
    if grao:
        # df = data.traj_by_journey(journey)
        df = data.traj_by_journey_date(journey, start_date, end_date)

#    if grao:
#        df = data.traj_by_journey(journey)
    else:
        df = data.traj_by_traj(traj)

    fig = trajectories_to_fig(df)
    # fig = hex_map(df)
    return fig


def scatter_dist_time(df):
    fig = px.scatter(
        df, x="cum_dist", y="cum_time",
        hover_data=["trajectory_id"],
        color="speed", color_continuous_scale="Edge"
    )
    return fig


@app.callback(
    [Output('cum_dist_time', 'figure'),
     Output("describe_table", "columns"),
     Output("describe_table", "data")],
    Input('submit_button', 'n_clicks'),
    [State('radio_journey_1', 'value'),
     State('radio_traj_1', 'value'),
     State("radio_grao", "value"),
     State('date-range', 'start_date'),
     State('date-range', 'end_date')]
)
def update_graph_4y(n_clicks, journey, traj, grao, start_date, end_date):
    start_date_object = date.fromisoformat(start_date)
    print(start_date_object)
    if grao:
        # df = data.traj_by_journey(journey)
        df = data.traj_by_journey_date(journey, start_date, end_date)
    else:
        df = data.traj_by_traj(traj)
    fig = scatter_dist_time(df)
    dfd = df[["speed", "acceleration", "hour"]].describe()
    columns = [{"name": i, "id": i} for i in dfd.columns]
    datat = dfd.to_dict('records')
    return (fig, columns, datat)


def create_table(df):
    return dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict('records'),
    )
