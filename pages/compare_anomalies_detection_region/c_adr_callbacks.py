#!/usr/bin/env ipython

import dash_bootstrap_components as dbc
import dash
import plotly.express as px
import plotly.graph_objects as go
from app import app
from dash.dependencies import Input, Output, State

from . import c_adr_data as data


def trajectory_2_fig(df, dfa, dfr):

    # fig = px.scatter_mapbox()
    #        df, lat="lat", lon="lng", mode="marker+line",
    #        height=600)
    #
    #    fig.add_trace(go.Scattermapbox(

    fig = go.Figure(
        go.Scattermapbox(
            name="Trajetória Realizada",
            lat=df["lat"],
            lon=df["lng"],
            mode="markers+lines",
            marker=go.scattermapbox.Marker(size=8, color="rgb(0, 100, 142)", opacity=1),
        )
    )
    fig.add_trace(
        go.Scattermapbox(
            name="Ponto Inicial",
            lat=[df["lat"].iloc[0]],
            lon=[df["lng"].iloc[0]],
            mode="markers",
            marker=go.scattermapbox.Marker(
                size=18, color="rgb(0, 100, 142)", opacity=1,
            ),
        )
    )
    fig.add_trace(
        go.Scattermapbox(
            name="Trajeto Esperado",
            lat=dfr["lat"],
            lon=dfr["lng"],
            mode="markers+lines",
            visible="legendonly",
            marker=go.scattermapbox.Marker(
                size=8, color="rgb(175, 100, 42)", opacity=0.5
            ),
        )
    )
    fig.add_trace(
        go.Scattermapbox(
            name="Anomalias",
            lat=dfa["lat"],
            lon=dfa["lng"],
            mode="markers+lines",
            marker=go.scattermapbox.Marker(
                size=11, color="rgb(175, 0, 42)", opacity=0.5
            ),
        )
    )

    fig.update_layout(
        mapbox_style="open-street-map",
        mapbox_zoom=11,
        mapbox_center_lat=df["lat"].iloc[100],
        mapbox_center_lon=df["lng"].iloc[100],
        height=700,
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        legend_orientation="h",
    )

    return fig

def df_to_pr_curve(dfs):
    fig = go.Figure()

    fig.add_shape(
        type='line', line=dict(dash='dash'),
        x0=0, x1=1, y0=1, y1=0
    )
    models = ["riobusdata", "gmvsae", "iboat", "transformer"]

    for m in models:
        df = dfs[dfs["model"] == m]
        precision = df["precision"].values
        recall = df["recall"].values
        #auc = df["auc"].unique()[0]
        auc = 666

        fig.add_trace(go.Scatter(
            x=recall, y=precision,
            name= f"{m}",
            #(AUC={auc:.4f})
            mode="lines+markers",
            text = ['Threshold {}'.format(i) for i in df["threshold"]],
        ))
    fig.update_layout(
        xaxis_title='Recall',
        yaxis_title='Precision',
        yaxis=dict(scaleanchor="x", scaleratio=1),
        xaxis=dict(constrain='domain'),
        #width=600, height=700,
        legend_orientation="h",
    )
        #fig = px.area(
        #    x=recall, y=precision,
        #    title=f'Precision-Recall Curve (AUC={auc:.4f})',
        #    labels=dict(x='Recall', y='Precision'),
        #    width=700, height=500
                   #)


    #fig.update_yaxes(scaleanchor="x", scaleratio=1)
    #fig.update_xaxes(constrain='domain')
    return fig



@app.callback(
    Output("map_cadr_l", "figure"),
    [Input("button_cadr", "n_clicks"),
     Input("drop_model_name_l", "value")],
    [State("drop_rota", "value"),
     State("drop_traj", "value")],
)
def update_graph_model_l(n_clicks, model, rota, traj):
    return update_graph_model(n_clicks, model, rota, traj)

@app.callback(
    Output("map_cadr_r", "figure"),
    [Input("button_cadr", "n_clicks"),
     Input("drop_model_name_r", "value")],
    [State("drop_rota", "value"),
     State("drop_traj", "value"),
     ],
)
def update_graph_model_r(n_clicks, model, rota, traj):
    return update_graph_model(n_clicks, model, rota, traj)


def update_graph_model(n_clicks, model, rota, traj):
    dfa = data.anom_by_model_route(model, rota)

    dft = data.traj_by_rota_traj(rota, traj)

    if traj >= 50:
        df1 = data.traj_by_rota_traj(rota, traj % 50)
    else:
        df1 = dft

    anon_idx = data.extract_anon_idx(dfa, traj)
    #compare = list(map(lambda x, y: x != y, dft["predicted"], dft["input_token"]))
    dft.reset_index(inplace=True)
    compare = dft.index.isin(anon_idx)
    return trajectory_2_fig(dft, dft[compare], df1)

@app.callback(
    Output("pr-curve", "figure"),
    Input("button_cadr", "n_clicks"),
    [State("drop_rota", "value"),
     State("drop_traj", "value"),
     ]
)
def update_pr_curve(n_clicks, rota, traj):
    df = data.get_eval(rota)
    fig = df_to_pr_curve(df)
    return fig
