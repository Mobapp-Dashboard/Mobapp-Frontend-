# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
import dash
#from layout import layout
import dash_bootstrap_components as dbc
from flask_caching import Cache
import uuid


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.config.suppress_callback_exceptions = True

cache = Cache(app.server, config={
    'CACHE_TYPE': 'filesystem',
    'CACHE_DIR': 'cache-directory',
    'CACHE_THRESHOLD': 2
})

session_id = str(uuid.uuid4())
