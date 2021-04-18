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
import json

from dash_layout import layout as layout
from dash.dependencies import Input, Output, State
from fastapi import FastAPI
from starlette.middleware.wsgi import WSGIMiddleware
from fastapi.staticfiles import StaticFiles


app = dash.Dash(__name__, requests_pathname_prefix="/dash/")

app.layout = layout

grapp_server = FastAPI()

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


class Grapp:
    def __init__(self):
       self.meta = None

    def load_meta(self, path):
        with open(path) as f:
            self.meta = json.load(f)
            return self.meta

    def run_server(self, dash_path="/dash", static_path="/static", static_directory="static", port=8080):
        grapp_server.mount(dash_path, WSGIMiddleware(app.server))
        grapp_server.mount(static_path, StaticFiles(directory=static_directory), name="static")
        uvicorn.run(grapp_server, port=port)
