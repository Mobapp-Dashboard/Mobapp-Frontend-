#!/usr/bin/env ipython

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from styles.style import CONTENT_STYLE

from . import eda_callbacks, sidebar_callbacks
from .sidebar import sidebar

map_eda = dbc.Row(
    [
        dbc.Col(html.Div([
            html.H2("Mapa"),
            html.Br(),
        ]), md=12),
        dbc.Col(
            html.Div([
                dcc.Graph(id='mapL'),
                html.Br(),
                html.Hr(),
            ]),
            md=12,
        )
    ])

stats_plots = dbc.Row(
    [
        dbc.Col(
            html.Div([
                html.H2("Distância x Tempo (acumulados)"),
                dcc.Graph(id='cum_dist_time')
            ]),
            md=6,
        ),
        dbc.Col([
            html.H2("Sumário"),
            html.Div(id="tabela-sumario"),
        ],
                md=6),

    ])


content = html.Div([
    sidebar,
    html.Div([
        map_eda,
        stats_plots
    ], style=CONTENT_STYLE),
    dcc.Store(id="DataFrames")
])

#
#        dbc.Col(
#            [
#                dbc.Button(
#                    "Sumário",
#                    id="sumario-button",
#                    className="mb-3",
#                    color="primary",
#                    n_clicks=0,
#                ),
#                dbc.Collapse(
#                    dbc.Card(
#                        dbc.CardBody(
#                            [
#                                html.P("Aqui haverá uma tabela de sumário"),
#                            ])),
#                    id="collapse",
#                    is_open=False,),
#            ], md=6)
#
