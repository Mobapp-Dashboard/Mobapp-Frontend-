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

models = ["transformer", "iboat"]
models_opt = [{'label': f"Model: {m}", "value": m} for m in models]

trajs = list(range(100))
trajs_opt = [{'label': f"Trajetória: {traj}", "value": traj} for traj in trajs]

controls = dbc.Nav(
    [
        html.P('', style={
            'textAlign': 'center'
        }),
        dbc.Card([dcc.Dropdown(
            id='drop_model_name',
            options=models_opt,
            value=models[0]
        )]),
        html.Br(),
        dbc.Card([dcc.Dropdown(
            id='drop_rota',
            options=rotas_opt,
            value=rotas[0]

        )]),
        dbc.Card([dcc.Dropdown(
            id='drop_traj',
            options=trajs_opt,
            value=trajs[50]

        )]),
        html.Br(),
        dbc.Button(
            id='button_adr',
            n_clicks=0,
            children='Submit',
            color='primary',
            block=True
        )
    ],
    vertical=True
)

sidebar = html.Div(
    [
        html.H2('Model and Route Selection', style=TEXT_STYLE),
        html.Hr(),
        controls
    ],
    #style=SIDEBAR_STYLE,
)
