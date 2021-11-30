#!/usr/bin/env ipython
#!/usr/bin/env ipython

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from styles.style import CONTENT_STYLE

from . import c_adr_callbacks
#, sidebar_callbacks
from .sidebar import sidebar

models = ["transformer", "iboat"]
models_opt = [{'label': f"Model: {m}", "value": m} for m in models]

maps_cadr = dbc.Row(children=[
    dbc.Col(children=[
        dcc.Dropdown(
            id='drop_model_name_l',
            options=models_opt,
            value=models[0]),
        dcc.Graph(id="map_cadr_l"),
        ], md=4),
    dbc.Col(dcc.Graph(id="pr-curve"), md=4),
    dbc.Col(children=[
        dcc.Dropdown(
            id='drop_model_name_r',
            options=models_opt,
            value=models[1]),
        dcc.Graph(id="map_cadr_r"),
        ], md=4),

])




content = html.Div([
    html.Br(),
    maps_cadr,
#    stats_plots,
#    dcc.Store(id="DataFrames")
], style=CONTENT_STYLE)


page = html.Div(
    dbc.Container(dbc.Row([
        dbc.Col(sidebar, md=2),
        dbc.Col(content, md=10)
    ]), fluid=True))
