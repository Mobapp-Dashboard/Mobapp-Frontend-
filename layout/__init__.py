#!/usr/bin/env ipython

import time

import dash_core_components as dcc
import dash_html_components as html
from app import app
from dash.dependencies import Input, Output
from pages.anomalies_detection_region import adr
from pages.eda import eda
from pages.eval_model import eval_model
from styles.style import TOP_TITLE_STYLE

START_PAGE = "tab-pred-anom"

layout = html.Div(
    [
        html.H1("Dashboard: Urban Mobility", style=TOP_TITLE_STYLE),
        dcc.Loading(
            id="loading-tabs",
            type="default",
            children=[
                dcc.Tabs(
                    id="front-tabs",
                    value=START_PAGE,
                    children=[
                        dcc.Tab(label="EDA", value="tab-eda"),
                        dcc.Tab(label="Model Evaluation", value="tab-eval-model"),
                        dcc.Tab(
                            label="Anomalies Detection(Points/Region)",
                            value="tab-pred-anom",
                        ),
                    ],
                ),
                html.Div(id="front-tabs-content"),
            ],
        ),
    ]
)


@app.callback(Output("front-tabs-content", "children"), Input("front-tabs", "value"))
def render_content(tab):
    if tab == "tab-eda":
        return eda.content
    elif tab == "tab-eval-model":
        return eval_model.content
    elif tab == "tab-pred-anom":
        return adr.page


@app.callback(Output("loading-tabs", "children"), Input("loading-tabs", "children"))
def input_triggers_spinner(value):
    time.sleep(1)
    return value
