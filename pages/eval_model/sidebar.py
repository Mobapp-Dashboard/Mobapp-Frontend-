#!/usr/bin/env ipython

#!/usr/bin/env ipython
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from styles.style import SIDEBAR_STYLE, TEXT_STYLE
import requests
import pandas as pd

from environment.settings import BACKEND

#from . import sidebar_callbacks


rotas = list(range(64))
rotas_opt = [{'label': f"Route: {rota}", "value": rota} for rota in rotas]

trajs = list(range(100))
trajs_opt = [{'label': f"Trajectory: {traj}", "value": traj} for traj in trajs]

controls = dbc.Nav(
    [
        html.P('Select route and trajectory', style={
            'textAlign': 'center'
        }),
        dbc.Card([dcc.Dropdown(
            id='route-model',
            options=rotas_opt,
            value=rotas[0]

        )]),
        dbc.Card([dcc.Dropdown(
            id='traj-model',
            options=trajs_opt,
            value=trajs[50]
        )]),
        html.Br(),
        dbc.Button(
            id='button-model',
            n_clicks=0,
            children='Modelo',
            color='primary',
            block=True
        )
    ],
    vertical=True
)

sidebar = html.Div(
    [
        html.H2('Trajectories Selection', style=TEXT_STYLE),
        html.Hr(),
        controls
    ],
    #style=SIDEBAR_STYLE,
)
