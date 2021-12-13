#!/usr/bin/env ipython

#!/usr/bin/env ipython
from dash.dependencies import Input, Output, State

from app import app
from utils import request_functions as rf

from .sidebar import df

def line_2_jouney_options(df, line):
    journeys = df[df["line_id"] == line].journey_id.unique()
    journeys.sort()
    return ([{'label': f"Rota {j}", "value": j} for j in journeys], journeys[0])

def line_jouney_2_traj_options(df, line, journey):
    trajs = df[(df["line_id"] == line) & (df["journey_id"] == journey)].trajectory_id.unique()
    print(trajs)
    trajs.sort()
    return ([{'label': f"Trajetória {t}", "value": t} for t in trajs], trajs[0])

@app.callback(
    [Output('radio_journey_1', 'options'),
     Output('radio_journey_1', 'value')],
    Input('radio_linha_1', 'value'))
def att_journey_1(line):
    return line_2_jouney_options(df, line)


@app.callback(
    [Output('radio_traj_1', 'options'),
     Output('radio_traj_1', 'value')],
    [Input('radio_linha_1', 'value'),
     Input('radio_journey_1', 'value')
     ])
def att_traj_1(line, journey):
    return line_jouney_2_traj_options(df, line, journey)
