#!/usr/bin/env ipython

#!/usr/bin/env ipython

#!/usr/bin/env ipython
from dash.dependencies import Input, Output, State

from app import app
from utils import request_functions as rf



def line_2_jouney_options(df, line):
    journeys = df[df["line_id"] == line].journey_id.unique()
    journeys.sort()
    return ([{'label': f"Journey {j}", "value": j} for j in journeys], journeys[0])

def line_jouney_2_traj_options(df, line, journey):
    trajs = df[(df["line_id"] == line) & (df["journey_id"] == journey)].trajectory_id.unique()

    trajs.sort()
    return ([{'label': f"Trajetória {t}", "value": t} for t in trajs], trajs[0])



@app.callback(
    [Output('radio_traj_1', 'options'),
     Output('radio_traj_1', 'value')],
    [Input('radio_linha_1', 'value'),
     Input('radio_journey_1', 'value')
     ])
def att_traj_1(line, journey):
    return line_jouney_2_traj_options(df, line, journey)

@app.callback(
    [Output('radio_traj_2', 'options'),
     Output('radio_traj_2', 'value')],
    [Input('radio_linha_2', 'value'),
     Input('radio_journey_2', 'value')
     ])
def att_traj_1(line, journey):
    return line_jouney_2_traj_options(df, line, journey)

@app.callback(
    Output("offcanvas", "is_open"),
    Input("open-offcanvas", "n_clicks"),
    [State("offcanvas", "is_open")],
)
def toggle_offcanvas(n1, is_open):
    if n1:
        return not is_open
    return is_open
