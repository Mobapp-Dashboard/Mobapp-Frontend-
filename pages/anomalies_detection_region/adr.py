#!/usr/bin/env ipython

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from styles.style import CONTENT_STYLE

from . import adr_callbacks
from .sidebar import sidebar

map_region = dbc.Col(dcc.Graph(id="map_ad"), md=7)
map_adr = dbc.Col(dcc.Graph(id="map_rota"), md=7)
p_rec_plot = dbc.Col(dcc.Graph(id="p_rec"), md=2)


pre_content = html.Div(
    [
        html.H3("Análise de Modelos"),
        dbc.Row([
            map_adr,
            p_rec_plot
        ])
    ])

content = html.Div(
    dbc.Container(dbc.Row([
        dbc.Col(sidebar, md=2),
        dbc.Col(pre_content, md=10)
    ]), fluid=True))
