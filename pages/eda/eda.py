#!/usr/bin/env ipython

from datetime import date

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from styles.style import CONTENT_STYLE, SIDEBAR_STYLE, TEXT_STYLE

from . import eda_callbacks, sidebar_callbacks

# from .sidebar import sidebar

###############
### SIDEBAR ###
###############

controls = dbc.FormGroup(
    [
        html.P("Use those fields for filter the trajectories loaded."),
        html.Hr(),
        dcc.DatePickerRange(
            id="date-range",
            min_date_allowed=date(2013, 1, 1),
            max_date_allowed=date(2013, 1, 7),
            initial_visible_month=date(2013, 1, 1),
            start_date=date(2013, 1, 1),
            end_date=date(2013, 1, 1),
        ),
        html.Hr(),
        dcc.RadioItems(
            id="radio-shift",
            options=[
                {"label": "All", "value": 0},
                {"label": "Morning", "value": 1},
                {"label": "Afternoon", "value": 2},
                {"label": "Evening", "value": 3},
                {"label": "Dawn", "value": 4},
            ],
            value=0,
        ),
        html.Hr(),
        dbc.Card([dcc.Dropdown(id="dropdown-journey", options=[], value="10001")]),
        html.Hr(),
        dbc.Button(
            id="submit-button",
            n_clicks=0,
            children="Submit",
            color="primary",
            block=True,
        ),
    ]
)


control_painel = dbc.FormGroup(
    [
        html.H2("Control Panel", style={"textAlign": "center"}),
        html.Hr(),
        html.P("Clicked Point Data"),
        html.Div(
            id="click-log",
            style={"border": "thin lightgrey solid", "overflowX": "scroll"},
        ),
        html.Hr(),
        dbc.Button(
            id="reset-button", n_clicks=0, children="Reset", color="primary", block=True
        ),
    ]
)

control_color = html.Div(
    [
        html.P("Select the highlighted attribute in scatter plots"),
        dcc.RadioItems(
            id="radio-color",
            options=[
                {"label": "Velocity", "value": "speed"},
                {"label": "Acceleration", "value": "acceleration"},
                {"label": "Distance (cumulative)", "value": "cum_dist"},
                {"label": "Time (cumulative)", "value": "cum_time"},
            ],
            value="speed",
            #        labelStyle={'display': 'inline-block'}
        ),
    ]
)


sidebar = html.Div(
    [
        #html.H2("Exploratory Data Analysis", style=TEXT_STYLE),
        html.Hr(),
        controls,
        html.Hr(),
        control_color,
        html.Hr(),
        html.Hr(),
        control_painel,
    ]
)

###############
### CONTENT ###
###############

map_eda = dbc.Row(
    [
        dbc.Col(html.Div([html.H2("Map"), html.Br(),]), md=12),
        dbc.Col(html.Div([dcc.Graph(id="mapL"), html.Br(), html.Hr(),]), md=12,),
    ]
)

stats_plots = dbc.Row(
    [
        dbc.Col(
            html.Div(
                [
                    html.H2("Distance* x Time (cumulative)"),
                    dcc.Graph(id="cum-dist-time"),
                ]
            ),
            md=6,
        ),
        dbc.Col([html.H2("Summary"), html.Div(id="summary-table"),], md=6),
        dbc.Col(
            [
                html.P(
                    "*Distances are calculated by euclidean distance, witch means that the road network are not used to this calculus and we have a substimation of the distances, velocity and acceleration."
                ),
            ],
            md=6,
        ),
    ]
)


pre_content = html.Div(
    [map_eda, stats_plots, dcc.Store(id="DataFrames")], style=CONTENT_STYLE
)

content = html.Div([
    html.H2('Exploratory Data Analysis', style=TEXT_STYLE),
    html.Hr(),
    dbc.Container(
        dbc.Row(
            [
                dbc.Col(sidebar, md=2),
                dbc.Col(pre_content, md=9),
                #                dbc.Col(pre_content, md=5),
                #                dbc.Col(sidebar, md=1),
            ]
        ),
        fluid=True,
    )]
)
