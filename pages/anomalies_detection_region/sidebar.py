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


rotas = list(range(5))
rotas_opt = [{'label': f"Rota: {rota}", "value": rota} for rota in rotas]

trajs = list(range(100))
trajs_opt = [{'label': f"Trajetória: {traj}", "value": traj} for traj in trajs]

controls = dbc.Nav(
    [
        html.P('Selecione rota e trajetória', style={
            'textAlign': 'center'
        }),
        dbc.Card([dcc.Dropdown(
            id='rota_model',
            options=rotas_opt,
            value=rotas[0]

        )]),
        dbc.Card([dcc.Dropdown(
            id='traj_model',
            options=trajs_opt,
            value=trajs[50]
        )]),
        html.Br(),
        dbc.Button(
            id='model_button',
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
        html.H2('Selção de Trajetórias', style=TEXT_STYLE),
        html.Hr(),
        controls
    ],
    #style=SIDEBAR_STYLE,
)
