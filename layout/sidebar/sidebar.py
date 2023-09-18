#!/usr/bin/env ipython
import pandas as pd
import requests

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from environment.settings import BACKEND
from styles.style import SIDEBAR_STYLE, TEXT_STYLE

print(f"http://{BACKEND}/api/v1/trajectory_metadata/lines")


r = requests.get(
    f"http://{BACKEND}/api/v1/trajectory_metadata/meta_trajectory"
).json()


df = pd.DataFrame(r)

linhas = df["line_id"].unique()
linhas.sort()

linha_opt = [{"label": f"Linha {linha}", "value": linha} for linha in linhas]

controls = dbc.FormGroup(
    [
        html.P("Seleção de Trajetória", style={"textAlign": "center"}),
        dbc.Card(
            [dcc.Dropdown(id="radio_linha_1", options=linha_opt, value=linhas[0])]
        ),
        dbc.Card([dcc.Dropdown(id="radio_journey_1", options=[], value="")]),
        dbc.Card([dcc.Dropdown(id="radio_traj_1", options=[], value=None)]),
        dbc.Button(
            id="submit_button",
            n_clicks=0,
            children="Submit",
            color="primary",
            block=True,
        ),
        html.Br(),
        html.P("Histograma", style={"textAlign": "center"}),
        dbc.Card(
            [
                dcc.Dropdown(
                    id="radio_hist_type",
                    options=[
                        {"label": "Velocidade", "value": "speed"},
                        {"label": "Aceleração", "value": "acceleration"},
                    ],
                    value="speed",
                )
            ]
        ),
        dbc.Button(
            id="hist_button", n_clicks=0, children="Submit", color="primary", block=True
        ),
    ]
)


sidebar = html.Div(
    [html.H2("Comparação de Modelos", style=TEXT_STYLE), html.Hr(), controls],
    style=SIDEBAR_STYLE,
)
