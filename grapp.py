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

import hermes.backend.dict

from db import mongodb

app = dash.Dash(__name__, requests_pathname_prefix="/dash/")

app.layout = dash_layouts.layout

grapp_server = FastAPI()
cache = hermes.Hermes(hermes.backend.dict.Backend, ttl=mongodb.TTL)


@cache
def get_result_and_cache():
    loop = asyncio.get_event_loop()
    query_results = loop.run_until_complete(mongodb.fetch_results())
    return query_results


@app.callback(
    [Output('piePlot1', 'figure'), Output('piePlot2', 'figure')],
    [Input('pie-dropdown', 'value')])
def update_figure(pie_item):
    return go.Figure(
        data=[
            go.Pie(labels=preprocess.getvalues(pie_item))],
        layout={"title": f"Distribution of {pie_item.title()}"}), go.Figure(
        data=[
            go.Pie(labels=preprocess.getlabels(pie_item), values=preprocess.getvaluesforbalance(pie_item))],
        layout={"title": f"Distribution of Balance over {pie_item.title()}"})


@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/productivity':
        return dash_layouts.productivity_layout
    elif pathname == '/demographics':
        return dash_layouts.demographics_layout
    elif pathname == '/sample':
        return dash_layouts.sample_layout
    else:
        return dash_layouts.index_layout


@grapp_server.get("/")
async def root():
    return {"message": "Grapp is running!"}


class Grapp:
    def __init__(self):
        self.meta = None

    def load_meta(self, path):
        with open(path) as f:
            self.meta = json.load(f)
            return self.meta

    @staticmethod
    def run_server(dash_path="/dash", static_path="/static", static_directory="static", port=8080):
        grapp_server.mount(dash_path, WSGIMiddleware(app.server))
        grapp_server.mount(static_path, StaticFiles(directory=static_directory), name="static")
        uvicorn.run(grapp_server, port=port)

    @staticmethod
    def init_cache():
        query_results = get_result_and_cache()
        print(query_results)
