#!/usr/bin/env ipython

import json
from app import app

from dash.dependencies import Input, Output
from utils.extract_data import get_journey_by_date, get_traj_by_journey_date


def line_2_jouney_options(start_date, end_date):
    df = get_journey_by_date(start_date, end_date)
    journeys = df["journey_id"].unique()
    journeys.sort()
    return ([{'label': f"Route {j}", "value": j} for j in journeys], journeys[0])


@app.callback(
    [Output('dropdown-journey', 'options'),
     Output('dropdown-journey', 'value')],
    [Input('date-range', 'start_date'),
     Input('date-range', 'end_date')])
def att_journey_1(start_date, end_date):
    print(start_date)
    opt = line_2_jouney_options(start_date, end_date)
    return opt


#def traj_by_journey_date(journey, start_date, end_date):
#    df = get_traj_by_journey_date(journey, start_date, end_date)
#    trajs = df["trajectory_id"].unique()
#    trajs.sort()
#    return ([{'label': f"Trajectory {t}", "value": t} for t in trajs], trajs[0])
#
#
#@app.callback(
#    [Output('radio-traj-1', 'options'),
#     Output('radio-traj-1', 'value')],
#    [Input('dropdown-journey', 'value'),
#     Input('date-range', 'start-date'),
#     Input('date-range', 'end-date')])
#def att_traj_1(journey, start_date, end_date):
#    return traj_by_journey_date(journey, start_date, end_date)
#

@app.callback(Output("click-log", "children"),
              [Input('mapL', 'clickData'),
               Input("cum-dist-time", "clickData")])
def click_logging(click_map, click_scatter):
    return [json.dumps(click_map, indent=2), json.dumps(click_scatter, indent=2)]
