#!/usr/bin/env ipython

import dash_core_components as dcc
import dash_html_components as html
from app import app
from dash.dependencies import Input, Output
from pages.anomalies_detection_region import adr
from pages.eda import eda

layout = html.Div([
    html.H1('Dashboard: Mobilidade Urbana'),
    dcc.Tabs(id="front-tabs", value='tab-eda', children=[
        dcc.Tab(label='EDA', value='tab-eda'),
        dcc.Tab(label='Análise de Modelos', value='tab-one-model'),
    ]),
    html.Div(id='front-tabs-content')
])


@app.callback(Output('front-tabs-content', 'children'),
              Input('front-tabs', 'value'))
def render_content(tab):
    if tab == 'tab-eda':
        return eda.content
    elif tab == 'tab-one-model':
        return adr.content
