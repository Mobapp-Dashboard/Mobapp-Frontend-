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
        dbc.Col(
            html.Div("Selecione ou exclua trajetórias clicando na legenda."),
            md=10
        ),
        dbc.Col(
            dcc.Graph(id='mapL'),
            md=12,
        )
    ])

stats_plots = dbc.Row([
    dbc.Col(
        dcc.Graph(id='cum_dist_time'),
        md=7,
    ),
    dbc.Col(
        dash_table.DataTable(id='describe_table'),
        md=12,
    ),

])

content = html.Div([
    sidebar,
    html.Div([
        html.H3('Análise Exploratória de Dados'),
        map_eda,
        stats_plots
    ], style=CONTENT_STYLE),
    html.Div([
            dcc.Markdown("""
                **Click Data**

                Click on points in the graph.
            """),
            html.Pre(id='click-data')
    ]),
    dcc.Store(id="DataFrames")
])
