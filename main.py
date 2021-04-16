import dash
import dash_core_components as dcc
import dash_html_components as html
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import squarify
import uvicorn as uvicorn
import preprocess

from dash_layout import layout as layout
from dash.dependencies import Input, Output, State
from fastapi import FastAPI
from starlette.middleware.wsgi import WSGIMiddleware
from fastapi.staticfiles import StaticFiles


app = dash.Dash(__name__, requests_pathname_prefix="/dash/")

app.layout = layout


@app.callback([Output('piePlot1', 'figure'), Output('piePlot2', 'figure')],
              [Input('pie-dropdown', 'value')])
def update_figure(pie_item):
    return go.Figure(
        data=[
            go.Pie(labels=preprocess.getvalues(pie_item))],
        layout={"title": f"Distribution of {pie_item.title()}"}), go.Figure(
        data=[
            go.Pie(labels=preprocess.getlabels(pie_item), values=preprocess.getvaluesforbalance(pie_item))],
        layout={"title": f"Distribution of Balance over {pie_item.title()}"})


if __name__ == "__main__":
    app_fastapi = FastAPI()
    app_fastapi.mount("/dash", WSGIMiddleware(app.server))
    app_fastapi.mount("/static", StaticFiles(directory="static"), name="static")
    uvicorn.run(app_fastapi, port=8080)
