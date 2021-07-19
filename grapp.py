import asyncio
import time
import dash
import hermes

import dash_layouts
import dash_core_components as dcc
import dash_html_components as html
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import squarify
import uvicorn as uvicorn
import preprocess
import json

from dash.dependencies import Input, Output, State
from fastapi import FastAPI
from starlette.middleware.wsgi import WSGIMiddleware
from fastapi.staticfiles import StaticFiles
from db.load import load_from as db_types
from jsonschema import validate
# from flask_caching import Cache
from datetime import datetime
from schema import schema
from webbrowser import open as browser
from os import path, getcwd

grapp_server = FastAPI()

styles = [
    'https://cdnjs.cloudflare.com/ajax/libs/bulma/0.9.3/css/bulma.min.css',
    'https://cdnjs.cloudflare.com/ajax/libs/chroma-js/2.1.0/chroma.min.js'
]

scripts = [
   'https://cdnjs.cloudflare.com/ajax/libs/chroma-js/2.1.0/chroma.min.js' 
]

@grapp_server.get("/health")
async def root():
    return {"message": "Grapp is running!"}


class Grapp:

    def __init__(self, meta_path='meta.json'):
        self.meta = None
        self.port = 8080
        self.host = 'localhost'
        self.app = dash.Dash(__name__, requests_pathname_prefix='/', external_stylesheets=styles, external_scripts=scripts)
        self.cache = hermes.Hermes(hermes.backend.dict.Backend, ttl=60)
        self.cache_timeout = 10
        self.app.config.suppress_callback_exceptions = True
        self.layout = {}
        self.load_meta(path.join(getcwd(), meta_path))
        self.schema = schema
        self.callbacks(self.app)

    def load_meta(self, path):
        with open(path,encoding="utf8") as f:

            self.meta = json.load(f)

        validate(instance=self.meta, schema=schema)

        # load all initial variables from meta
        self.port = self.meta['port'] if 'port' in self.meta else self.port
        self.host = self.meta['host'] if 'host' in self.meta else self.host
        # construct graph layouts
        graphs = self.meta['graphs'] if 'graphs' in self.meta else []
        # create basic route
        self.app.layout = dash_layouts.wrap_layout(graphs)
        
        # change app title
        self.app.title = self.meta['name'] if 'name' in self.meta else 'Grapp'

        for graph in graphs:
            # load colors
            colors = graph['colors'] if 'colors' in graph else []
            # Connect to Graphs DB Here
            db_type = graph["db"]["type"]
            if db_type in db_types.keys():
                # create db connection
                credentials = graph['db']['credentials']

                # create app header
                header = dash_layouts.create_header(
                    graph['name'],
                    graph['description'] if 'description' in graph else ''
                )
                
                lastupdated = dash_layouts.create_lastupdated(
                    title="Última actualização em 1 de junio de 2021"
                )
                design = []

                # run all queries
                pipeline = {}
                for q in graph['queries']:
                    if q['input']['type'] != 'raw':
                        print("INDEX : "+str(graph['queries'].index(q)))
                        pipeline[graph['queries'].index(q)] = q['input']
                result = db_types[db_type](
                    credentials, [p for p in list(pipeline.values()) if p]
                )
                print(result)

                # generate graph
                for query in graph['queries']:
                    r = None
                    # check if colors exist in local chat
                    _colors = query['colors'] if 'colors' in query else colors
                    if query['input']['type'] == 'raw':
                        r = query['input']['value']
                    # start graph generation
                    if query['output']['type'] == 'indicator':
                        r = preprocess.indicator(result[graph['queries'].index(query)])
                        design.append(
                            dash_layouts.create_indicator(
                                value=r,
                                title=query['output']['title'],
                                size=query['size']
                            )
                        )
                    elif query['output']['type'] == 'piechart':
                        r = preprocess.piechart(result[graph['queries'].index(query)], query)
                        design.append(
                            dash_layouts.create_piechart(
                                labels=r['labels'],
                                values=r['values'], 
                                title=query['output']['title'],
                                size=query['size'],
                                color_discrete_map=query['output']['color_discrete_map'],

                            )
                        )
                    elif query['output']['type'] == 'donut':
                        r = preprocess.piechart(result[graph['queries'].index(query)], query)
                        design.append(
                            dash_layouts.create_piechart(
                                labels=r['labels'],
                                values=r['values'], 
                                title=query['output']['title'],
                                size=query['size'],
                                colors=_colors,
                                hole=0.5,
                                color_discrete_map=query['output']['color_discrete_map']
                            )
                        )
                    elif query['output']['type'] == 'barchart':
                        r = preprocess.barchart(result[graph['queries'].index(query)],query)
                        design.append(
                            dash_layouts.create_barchart(
                                labels=r['labels'],
                                values=r['values'],
                                title=query['output']['title'],
                                x_axis_label=query['output']['x_axis_label'],
                                y_axis_label=query['output']['y_axis_label'],
                                size=query['size'],
                                color_discrete_map=query['output']['color_discrete_map']
                            )
                        )
                    elif query['output']['type'] == 'treechart':
                        r = preprocess.treechart(result[graph['queries'].index(query)],query)
                        design.append(
                            dash_layouts.create_treechart(
                                labels=r['labels'],
                                values=r['values'],
                                parents=r['parents'],
                                title=query['output']['title'],
                                size=query['size'],
                                color_discrete_map=query['output']['color_discrete_map']
                            )
                        )
                    elif query['output']['type'] == 'horizontal-barchart':
                        r = preprocess.horizontal_barchart(result[graph['queries'].index(query)],query)
                        design.append(
                            dash_layouts.create_horizontal_barchart(
                                x_axis=r['x_axis'],
                                y_axis=r['y_axis'],
                                color=r['color'],
                                title=query['output']['title'],
                                size=query['size'],
                                x_axis_label = query['output']['x_axis_label'],
                                y_axis_label = query['output']['y_axis_label'],
                                color_label = query['output']['color'],
                                color_discrete_map=query['output']['color_discrete_map']
                            )
                        )
                    elif query['output']['type'] == 'bubblechart':
                        r = preprocess.bubblechart(result[graph['queries'].index(query)],query)
                        design.append(
                            dash_layouts.create_bubblechart(
                                x_axis=r['x_axis'],
                                y_axis=r['y_axis'],
                                bubbles = r['bubbles'],
                                title=query['output']['title'],
                                size=query['size'],
                                x_axis_label = query['output']['x_axis_label'],
                                y_axis_label = query['output']['y_axis_label'],
                                bubble_label = query['output']['bubbles'],
                                color_discrete_map=query['output']['color_discrete_map']
                            )
                        )
                    elif query['output']['type'] == 'bubblechart':
                        r = preprocess.bubblechart(result[graph['queries'].index(query)],query)
                        design.append(
                            dash_layouts.create_bubblechart(
                                x_axis=r['x_axis'],
                                y_axis=r['y_axis'],
                                bubbles = r['bubbles'],
                                title=query['output']['title'],
                                size=query['size'],
                                x_axis_label = query['output']['x_axis_label'],
                                y_axis_label = query['output']['y_axis_label'],
                                bubble_label = query['output']['bubbles']
                            )
                        )
                    elif query['output']['type'] == 'map-scatter-plot':
                        print('dfdfd')
                        r = preprocess.map(result[graph['queries'].index(query)],query)
                        design.append(
                            dash_layouts.create_map(
                                title=query['output']['title'],
                                size=query['size'],
                                data=r
                            )
                        )
                    elif query['output']['type'] == 'linechart':
                        r = preprocess.linechart(result[graph['queries'].index(query)],query)
                        design.append(
                            dash_layouts.create_linechart(
                                x_axis=r['x_axis'],
                                y_axis=r['y_axis'],
                                colors = r['colors'],
                                title=query['output']['title'],
                                size=query['size'],
                                x_axis_label = query['output']['x_axis_label'],
                                y_axis_label = query['output']['y_axis_label'],
                                color_label = query['output']['color_label'],
                                color_discrete_map = query['output']['color_discrete_map']
                            )
                        )
                    elif query['output']['type'] == 'areachart':
                        r = preprocess.areachart(result[graph['queries'].index(query)],query)
                        design.append(
                            dash_layouts.create_areachart(
                                x_axis=r['x_axis'],
                                y_axis=r['y_axis'],
                                colors = r['colors'],
                                title=query['output']['title'],
                                size=query['size'],
                                x_axis_label = query['output']['x_axis_label'],
                                y_axis_label = query['output']['y_axis_label'],
                                color_label = query['output']['color_label'],
                                line_group = query['output']['line_group'],
                                color_discrete_map = query['output']['color_discrete_map']
                            )
                        )
                    elif query['output']['type'] == 'scatterchart':
                        r = preprocess.scatterchart(result[graph['queries'].index(query)],query)
                        design.append(
                            dash_layouts.create_scatterchart(
                                x_axis=r['x_axis'],
                                y_axis=r['y_axis'],
                                title=query['output']['title'],
                                size=query['size'],
                                x_axis_label = query['output']['x_axis_label'],
                                y_axis_label = query['output']['y_axis_label'],
                                fill = query['output']['fill'],
                                fillcolor = query['output']['fillcolor'],
                                line_color = query['output']['line_color']
                            )
                         )
                    elif query['output']['type'] == 'single-line-chart':
                        r = preprocess.single_line_chart(result[graph['queries'].index(query)],query)
                        design.append(
                            dash_layouts.create_single_line_chart(
                                x_axis=r['x_axis'],
                                y_axis=r['y_axis'],
                                x_axis_label = query['output']['x_axis_label'],
                                y_axis_label = query['output']['y_axis_label'],
                                size=query['size'],
                                title=query['output']['title']
                            )
                        )
                self.layout[graph['route']] = html.Div(
                    html.Div([
                        header,
                        lastupdated,
                        html.Div(design, className="columns is-multiline"),
                    ], className="container")
                )
            else:
                print('Data source is currently not supported.')

    def callbacks(self, app):
        @app.callback(dash.dependencies.Output('page-content', 'children'),
                      [dash.dependencies.Input('url', 'pathname')])
        def construct_layout(pathname):
            if pathname in self.layout:
                return self.layout[pathname]
            else:
                # render first graph always
                return self.layout[list(self.layout.keys())[0]]

        @self.cache()
        def cached_time():
            return f'Current time is{datetime.now().strftime("%H:%M:%S")}'

        @app.callback(
            Output('cache_text', 'children'),
            Input('interval-component', 'n_intervals'))
        def render(value):
            return cached_time()

    def start(self, dash_path="/", static_path="/static", static_directory="static"):
        grapp_server.mount(dash_path, WSGIMiddleware(self.app.server))
        grapp_server.mount(static_path, StaticFiles(
            directory=static_directory), name="static")
        browser(f'http://{"localhost" if self.host == "0.0.0.0" else self.host}:{self.port}')
        uvicorn.run(grapp_server, host=self.host, port=self.port)
