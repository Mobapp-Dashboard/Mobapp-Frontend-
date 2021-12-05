#!/usr/bin/env ipython
#!/usr/bin/env ipython

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from styles.style import CONTENT_STYLE, TEXT_STYLE
from . import c_adr_callbacks
#, sidebar_callbacks
#from .sidebar import sidebar

###########
# Sidebar #
###########

rotas = list(range(64))
rotas_opt = [{'label': f"Route: {rota}", "value": rota} for rota in rotas]

controls = dbc.Nav(
    [
        html.P('', style={
            'textAlign': 'center'
        }),

        html.Br(),
        dbc.Card([dcc.Dropdown(
            id='route-drop-av',
            options=rotas_opt,
            value=rotas[0]

        )]),
        html.Hr(),
        html.P("Click on trajectory's box to see the anomalies:"),
        dbc.ListGroup(id="list-traj-scores"),
        html.P(id="traj-score-box")
    ],
    vertical=True
)

sidebar = html.Div(
    [
             controls
    ],
    #style=SIDEBAR_STYLE,
)

models = ["transformer", "iboat"]
models_opt = [{'label': f"Model: {m}", "value": m} for m in models]

maps_cadr = dbc.Row(dcc.Graph(id="map_adr"))




content = html.Div([
    html.Br(),
    maps_cadr,
#    stats_plots,
#    dcc.Store(id="DataFrames")
], style=CONTENT_STYLE)


page = html.Div([
    html.H2('Trajectory Anomalies Visualization', style=TEXT_STYLE),
    html.Hr(),
    dbc.Container(dbc.Row([
        dbc.Col(sidebar, md=6),
        dbc.Col(content, md=6)
    ]), fluid=True)])
