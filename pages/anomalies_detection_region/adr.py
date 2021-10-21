#!/usr/bin/env ipython

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from styles.style import CONTENT_STYLE

from . import adr_callbacks
from .sidebar import sidebar

map_adr = dbc.Row(
    [
        dbc.Col(
            dcc.Graph(id='map_ad'), md=12,
        ),
        #        dbc.Col(
        #            dcc.Graph(id='map_ad_gt'), md=6,
        #        ),

    ]
)

content = html.Div([
    sidebar,
    html.Div([
        html.H3('Análise de Modelos'),
        map_adr
    ], style=CONTENT_STYLE)
])
