#!/usr/bin/env ipython
import plotly.express as px

import plotly.graph_objects as go

style_point_focus = {
    "size": 18,
    "opacity": 1
}
style_first = style_point_focus
style_first["color"] = "#7383CA"
style_last = style_point_focus
style_last["color"] = "#231B25"

def trajectory_2_fig(df, n=5):
    fig = px.scatter_mapbox(
        df,
        lat="lat", lon="lng",
        height=600,
        hover_data=['instant', "trajectory_id"]
    )
    fig = add_range_scatters(df, n, fig)
    fig.update_layout(
            mapbox_style="open-street-map",
            mapbox_zoom=12,
            margin={"r":0,"t":0,"l":0,"b":0})
    return fig


def add_range_scatters(df, n, fig):
    for i in [n, -n]:
        style = style_first if (n > 0) else style_last
        fig.add_trace(
            go.Scattermapbox(
                lat=df["lat"],
                lon=df["lng"],
                mode='markers',
                marker=go.scattermapbox.Marker(**style)
        ))
