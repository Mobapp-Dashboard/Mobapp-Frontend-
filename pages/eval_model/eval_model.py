#!/usr/bin/env ipython

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from styles.style import CONTENT_STYLE, TEXT_STYLE

from . import eval_model_callbacks
from .sidebar import sidebar

#############################
# Dropbox Itens Definitions #
#############################

rotas = list(range(64))
rotas_opt = [{'label': f"Route: {rota}", "value": rota} for rota in rotas]

trajs = list(range(100))
trajs_opt = [{'label': f"Trajectory: {traj}", "value": traj} for traj in trajs]

models = ["riobusdata", "gmvsae", "iboat", "transformer"]
models_opt = [{'label': f"Model: {model}", "value": model} for model in models]


drop_models = dcc.Dropdown(
    id='models',
    options=models_opt,
    value=models[3]
)
#
#drop_threshold = dcc.Dropdown(
#    id="thr-model",
#    options=[],
#    value="1"
#)
#
slider_threshold = html.Div([
    html.P("Threshold"),
    dcc.Slider(
    id="thr-model",
#    min=0,
#    max=1,
    step=0.00001,
    value=0,
    tooltip={"placement": "bottom", "always_visible": True},
    )])

drop_routes = dcc.Dropdown(
    id='route-model',
    options=rotas_opt,
    value=rotas[35]
)

drop_trajs = dcc.Dropdown(
    id='traj-model',
    options=trajs_opt,
    value=trajs[65]
)


#################
# Maps and plot #
#################

map_traj = dcc.Graph(id="map-traj")

map_region = dcc.Graph(id="map-ad")
map_adr =    dcc.Graph(id="map-route")
p_rec_plot = dcc.Graph(id="p-rec")


###########
# Results #
###########

prediction = dbc.Card(
    dbc.CardBody(id="pred-title"))

# Todo BOX with predictions: IS ANOMALY?

#################
# Section Cols #
#################

route_section = html.Div(
    [
        html.Br(),
        html.H3("Results on routes"),
        drop_routes,
        dbc.Row([
            dbc.Col([
                html.Br(),
                html.H4("PR-Curve"),
                p_rec_plot
            ], md=6),
            dbc.Col([
                html.Br(),
                html.H4("Set of trajectories under evaluation"),
                html.Br(),
                map_adr
            ], md=6),
        ])
    ], style=CONTENT_STYLE)

traj_section = html.Div(
    [
        html.Br(),
        html.H3("Results on trajectories"),
        drop_trajs,
        drop_models,
        #drop_threshold,
        slider_threshold,
        html.Br(),
        dbc.Row([
            dbc.Col([map_traj], md=6),
            dbc.Col([prediction], md=6)
        ])
    ], style=CONTENT_STYLE
)

###############
# Page Layout #
###############

page = html.Div(
    html.H2('Model Evaluation', style=TEXT_STYLE),
    html.Hr(),
    dbc.Container(
        dbc.Row(
            [
                dbc.Col(route_section, md=12),
                html.Hr(),
                dbc.Col(traj_section, md=12),
            ]
        ),
        fluid=True,
    )
)
