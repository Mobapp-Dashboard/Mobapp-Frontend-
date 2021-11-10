#!/usr/bin/env ipython

import dash_core_components as dcc
import dash_html_components as html
from app import app
from dash.dependencies import Input, Output
from pages.anomalies_detection_region import adr
from pages.eda import eda
from pages.eval_model import eval_model
import time

layout = html.Div([
    html.H1('Dashboard: Urban Mobility'),
        dcc.Loading(
            id="loading-tabs",
            type="default",
            children=[
                dcc.Tabs(id="front-tabs", value='tab-pred-anon', children=[
                    dcc.Tab(label='EDA', value='tab-eda'),
                    dcc.Tab(label='Model Evaluation', value='tab-eval-model'),
                    dcc.Tab(label='Anomalies Detection(Points/Region)', value='tab-pred-anon'),
                ]),
                html.Div(id='front-tabs-content')
            ]
        ),


])


@app.callback(Output('front-tabs-content', 'children'),
              Input('front-tabs', 'value'))
def render_content(tab):
    if tab == 'tab-eda':
        return eda.content
    elif tab == 'tab-eval-model':
        return eval_model.content
    elif tab == "tab-pred-anon":
        return adr.page


@app.callback(Output("loading-tabs", "children"), Input("loading-tabs", "children"))
def input_triggers_spinner(value):
    time.sleep(1)
    return value
