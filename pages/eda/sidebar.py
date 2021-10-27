#!/usr/bin/env ipython
from datetime import date

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from styles.style import SIDEBAR_STYLE, TEXT_STYLE

controls = dbc.FormGroup(
    [
        html.P('Selecione a granularidade da visualização', style={
            'textAlign': 'center'
        }),
        dcc.DatePickerRange(
            id='date-range',
            min_date_allowed=date(2013, 1, 1),
            max_date_allowed=date(2013, 1, 7),
            initial_visible_month=date(2013, 1, 1),
            start_date=date(2013, 1, 1),
            end_date=date(2013, 1, 1)
        ),
        html.Br(),
        html.Br(),
        dcc.RadioItems(
            id="radio_grao",
            options=[
                {'label': 'Por rota', 'value': 1},
                {'label': 'Por trajetória', 'value': 0},
            ],
            value=1,
            labelStyle={'display': 'inline-block'}
        ),
        html.Br(),
        dcc.RadioItems(
            id="radio_turno",
            options=[
                {'label': 'Todos', 'value': 0},
                {'label': 'Manhã', 'value': 1},
                {'label': 'Tarde', 'value': 2},
                {'label': 'Noite', 'value': 3},
                {'label': 'Madrugada', 'value': 4},
            ],
            value=0,
            labelStyle={'display': 'inline-block'}
        ),
        html.Br(),
        dbc.Card([dcc.Dropdown(
            id='radio_journey_1',
            options=[],
            value="00010001"
        )]),
        html.Br(),
        dbc.Card([dcc.Dropdown(
            id='radio_traj_1',
            options=[],
            value=None
        )]),
        html.Br(),
        dbc.Button(
            id='submit_button',
            n_clicks=0,
            children='Submit',
            color='primary',
            block=True
        )
    ]
)


control_painel = dbc.FormGroup([
    html.H2("Painel de Controle", style={"textAlign": "center"}),
    html.Hr(),
    html.P("Dados do ponto clicado"),
    html.Div(id="click-log", style={
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }),
    html.Hr(),
    dbc.Button(
            id='reset_button',
            n_clicks=0,
            children='Reset',
            color='primary',
            block=True
        ),
])

control_color = html.Div([
    html.P("Selecionar o atributo destacado nos pontos"),
    dcc.RadioItems(
        id="radio_cor",
        options=[
            {'label': 'Velocidade', 'value': "speed"},
            {'label': 'Aceleração', 'value': "acceleration"},
            {'label': 'Distância (acumulada)', 'value': "cum_dist"},
            {'label': 'Tempo (acumulado)', 'value': "cum_time"}
        ],
        value="speed",
        labelStyle={'display': 'inline-block'}
    )])

sidebar = html.Div(
    [
        html.H2('Análise Exploratória de Dados', style=TEXT_STYLE),
        html.Hr(),
        controls,
        html.Hr(),
        control_color,
        html.Hr(),
        html.Hr(),
        control_painel,
    ],
    #style=SIDEBAR_STYLE,
)
