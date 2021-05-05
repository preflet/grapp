import asyncio
import time
import dash
import dash_layouts
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

from dash.dependencies import Input, Output, State
from fastapi import FastAPI
from starlette.middleware.wsgi import WSGIMiddleware
from fastapi.staticfiles import StaticFiles

# app = dash.Dash(__name__, requests_pathname_prefix="/dash/")

grapp_server = FastAPI()


# @app.callback(dash.dependencies.Output('page-content', 'children'),
#               [dash.dependencies.Input('url', 'pathname')])
# def display_page(pathname):
#     if pathname == '/productivity':
#         return dash_layouts.productivity_layout
#     elif pathname == '/demographics':
#         return dash_layouts.demographics_layout
#     elif pathname == '/sample':
#         return dash_layouts.sample_layout
#     else:
#         return dash_layouts.index_layout


@grapp_server.get("/")
async def root():
    return {"message": "Grapp is running!"}


class Grapp:
    def __init__(self, meta_path="meta.json"):
        self.meta = None
        self.port = 8080
        self.host = 'localhost'
        self.app = dash.Dash(__name__, requests_pathname_prefix="/dash/")
        self.app.layout = dash_layouts.layout

        self.layout = {
            'index': dash_layouts.index_layout
        }

        self.load_meta(meta_path)
        self.callbacks(self.app)

    def load_meta(self, path):
        with open(path) as f:
            self.meta = json.load(f)
        # load all initial variables from meta
        self.port = self.meta['port'] if 'port' in self.meta else self.port
        self.host = self.meta['host'] if 'host' in self.meta else self.host

        # construct graph layouts
        graphs = self.meta['graphs'] if 'graphs' in self.meta else []
        for graph in graphs:
            self.layout.update(
                dash_layouts.create_layout(
                    graph
                )
            )

    def callbacks(self, app):
        @app.callback(dash.dependencies.Output('page-content', 'children'),
                      [dash.dependencies.Input('url', 'pathname')])
        def construct_layout(pathname):
            print(pathname)
            if pathname in self.layout:
                return self.layout[pathname]
            else:
                return dash_layouts.index_layout

    def update_figure(self, pie_item):
        return go.Figure(
            data=[
                go.Pie(labels=preprocess.getvalues(pie_item))],
            layout={"title": f"Distribution of {pie_item.title()}"}), go.Figure(
            data=[
                go.Pie(labels=preprocess.getlabels(pie_item), values=preprocess.getvaluesforbalance(pie_item))],
            layout={"title": f"Distribution of Balance over {pie_item.title()}"})

    def start(self, dash_path="/dash", static_path="/static", static_directory="static"):
        grapp_server.mount(dash_path, WSGIMiddleware(self.app.server))
        grapp_server.mount(static_path, StaticFiles(
            directory=static_directory), name="static")
        uvicorn.run(grapp_server, host=self.host, port=self.port)
