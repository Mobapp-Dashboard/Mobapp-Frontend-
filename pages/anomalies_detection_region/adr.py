#!/usr/bin/env ipython
#!/usr/bin/env ipython

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from styles.style import CONTENT_STYLE

from . import adr_callbacks
#, sidebar_callbacks
from .sidebar import sidebar

map_adr = dbc.Col(dcc.Graph(id="map_adr"), md=7)

content = html.Div([
    map_adr,
#    stats_plots,
#    dcc.Store(id="DataFrames")
], style=CONTENT_STYLE)


page = html.Div(
    dbc.Container(dbc.Row([
        dbc.Col(sidebar, md=2),
        dbc.Col(content, md=10)
    ]), fluid=True))
