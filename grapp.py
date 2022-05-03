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
import charts


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
                # header = dash_layouts.create_header(
                #     graph['name'],
                #     graph['description'] if 'description' in graph else ''
                # )
                
                # lastupdated = dash_layouts.create_lastupdated(
                #     title="Última actualização em 1 de junio de 2021"
                # )
                design = []

                # run all queries
                # pipeline = {}
                # for q in graph['queries']:
                #     if q['input']['type'] != 'raw':
                #         print("INDEX : "+str(graph['queries'].index(q)))
                #         pipeline[graph['queries'].index(q)] = q['input']
                # result = db_types[db_type](
                #     credentials, [p for p in list(pipeline.values()) if p]
                # )
                # print(result)

                # generate graph
                for query in graph['queries']:
                    r = None
                    # check if colors exist in local chat
                    _colors = query['colors'] if 'colors' in query else colors
                    if query['input']['type'] == 'raw':
                        r = query['input']['value']
                    # start graph generation
                    if query['output']['type'] == 'indicator':
                        # r = preprocess.indicator(result[graph['queries'].index(query)])
                        design.append(
                            dash_layouts.create_indicator(
                                title=query['output']['title'],
                                size=query['size'],
                                id = query['output']['id']
                            )
                        )
                    elif query['output']['type'] == 'piechart':
                        # r = preprocess.piechart(result[graph['queries'].index(query)], query)
                        design.append(
                            dash_layouts.create_piechart(
                                title=query['output']['title'],
                                size=query['size'],
                                id = query['output']['id']
                            )
                        )
                    elif query['output']['type'] == 'donut':
                        # r = preprocess.piechart(result[graph['queries'].index(query)], query)
                        design.append(
                            dash_layouts.create_piechart(
                                title=query['output']['title'],
                                size=query['size'],
                                id = query['output']['id']
                            )
                        )
                    elif query['output']['type'] == 'barchart':
                        # r = preprocess.barchart(result[graph['queries'].index(query)],query)
                        design.append(
                            dash_layouts.create_barchart(
                                title=query['output']['title'],
                                size=query['size'],
                                id = query['output']['id']
                            )
                        )
                    elif query['output']['type'] == 'treechart':
                        # r = preprocess.treechart(result[graph['queries'].index(query)],query)
                        design.append(
                            dash_layouts.create_treechart(
                                title=query['output']['title'],
                                size=query['size'],
                                id = query['output']['id']
                            )
                        )
                    elif query['output']['type'] == 'horizontal-barchart':
                        # r = preprocess.horizontal_barchart(result[graph['queries'].index(query)],query)
                        design.append(
                            dash_layouts.create_horizontal_barchart(
                                title=query['output']['title'],
                                size=query['size'],
                                id = query['output']['id']
                            )
                        )
                    elif query['output']['type'] == 'bubblechart':
                        # r = preprocess.bubblechart(result[graph['queries'].index(query)],query)
                        design.append(
                            dash_layouts.create_bubblechart(
                                title=query['output']['title'],
                                id = query['output']['id'],
                                size=query['size']
                            )
                        )
                    elif query['output']['type'] == 'bubblechart':
                        # r = preprocess.bubblechart(result[graph['queries'].index(query)],query)
                        design.append(
                            dash_layouts.create_bubblechart(
                                title=query['output']['title'],
                                id = query['output']['id'],
                                size=query['size']
                            )
                        )
                    elif query['output']['type'] == 'map-scatter-plot':
                        print('dfdfd')
                        # r = preprocess.map(result[graph['queries'].index(query)],query)
                        design.append(
                            dash_layouts.create_map(
                                title=query['output']['title'],
                                id = query['output']['id'],
                                size=query['size']
                            )
                        )
                    elif query['output']['type'] == 'linechart':
                        # r = preprocess.linechart(result[graph['queries'].index(query)],query)
                        design.append(
                            dash_layouts.create_linechart(
                                title=query['output']['title'],
                                id = query['output']['id'],
                                size=query['size']
                            )
                        )
                    elif query['output']['type'] == 'areachart':
                        # r = preprocess.areachart(result[graph['queries'].index(query)],query)
                        # print("RRRRRRRR"+str(r))
                        design.append(
                            dash_layouts.create_areachart(
                                title=query['output']['title'],
                                size=query['size'],
                                id = query['output']['id']
                            )
                        )
                    elif query['output']['type'] == 'scatterchart':
                        # r = preprocess.scatterchart(result[graph['queries'].index(query)],query)
                        design.append(
                            dash_layouts.create_scatterchart(
                                title=query['output']['title'],
                                size=query['size'],
                                id = query['output']['id']
                            )
                         )
                    elif query['output']['type'] == 'single-line-chart':
                        # r = preprocess.single_line_chart(result[graph['queries'].index(query)],query)
                        design.append(
                            dash_layouts.create_single_line_chart(
                                size=query['size'],
                                title=query['output']['title'],
                                id = query['output']['id']
                            )
                        )
                
<<<<<<< HEAD
                # design.insert(4,dash_layouts.create_lastupdated(
                #     title="Última actualização em 1 de Junho de 2021"
                # ))
=======
                design.insert(4,dash_layouts.create_lastupdated(
                    title="Última actualização em 2 de Maio de 2022"
                ))
>>>>>>> fc11b6b980b818497efdcfe69176c6527fa9da3b
                self.layout[graph['route']] = html.Div(
                    html.Div([
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

        # @self.cache()
        # def cached_time():
        #     return f'Current time is{datetime.now().strftime("%H:%M:%S")}'

        # @app.callback(
        #     Output('cache_text', 'children'),
        #     Input('interval-component', 'n_intervals'))
        # def render(value):
        #     return cached_time()

        # @app.callback(
        #     Output('logo','style'),
        #     [Input('muni-dropdown','value')]
        # )
        # def func(val):
        #     return {'display': 'none'}
        
        @app.callback(
            Output('indi_1', 'children'),
            Output('indi_2', 'children'),
            Output('indi_3', 'children'),
            Output('indi_4', 'children'),
            Output('indi_5', 'children'),
            Output('single-line-chart','figure'),
            Output('donut-chart','figure'),
            Output('treechart_tipo_de_edifício','figure'),
            Output('horizontal_barchart_sazonalidade_por_municipio','figure'),
            Output('scatterchart_sazonalidade_por_pavilhão','figure'),
            Output('bubblechart_sazonalidade_por_edificio','figure'),
            Output('linechart_padrão_por_hora_por_tipo_de_edifício','figure'),
            Output('areachart_comparação_semanal','figure'),
            Output('piechart_padrão_do_fim_de_semana','figure'),
            Output('geojson','data'),
            [Input('date-range', 'start_date'),Input('date-range', 'end_date')],
            [Input('muni-dropdown','value')],
            [Input('tepo-dropdown','value')])
        def filters(start_date,end_date,muni,tepo):

            filter = charts.create_filter(start_date,end_date,muni,tepo)

            indi_1 = str(charts.indicator_total(filter))
            indi_2 = str(charts.indicator_numero_de_edificios(filter))
            indi_3 = str(charts.indicator_tipo_de_edifícios(filter))
            indi_4 = str(charts.indicator_município(filter))
            indi_5 = str(charts.indicator_fatura(filter))
            single_line_chart = charts.single_line_chart(filter)
            donut_chart = charts.donut_chart(filter)
            treechart_tipo_de_edifício = charts.treechart_tipo_de_edifício(filter)
            horizontal_barchart_sazonalidade_por_municipio = charts.horizontal_barchart_sazonalidade_por_municipio(filter)
            scatterchart_sazonalidade_por_pavilhão = charts.scatterchart_sazonalidade_por_pavilhão(filter)
            bubblechart_sazonalidade_por_edificio = charts.bubblechart_sazonalidade_por_edificio(filter)
            linechart_padrão_por_hora_por_tipo_de_edifício = charts.linechart_padrão_por_hora_por_tipo_de_edifício(filter)
            areachart_comparação_semanal = charts.areachart_comparação_semanal(filter)
            piechart_padrão_do_fim_de_semana = charts.piechart_padrão_do_fim_de_semana(filter)
            geomap = charts.geomap(filter)

            return indi_1,indi_2,indi_3,indi_4,indi_5,\
            single_line_chart,donut_chart,treechart_tipo_de_edifício,\
                horizontal_barchart_sazonalidade_por_municipio,scatterchart_sazonalidade_por_pavilhão,\
                bubblechart_sazonalidade_por_edificio,linechart_padrão_por_hora_por_tipo_de_edifício,\
                areachart_comparação_semanal,piechart_padrão_do_fim_de_semana,\
                geomap
            
        
    def start(self, dash_path="/", static_path="/static", static_directory="static"):
        grapp_server.mount(dash_path, WSGIMiddleware(self.app.server))
        grapp_server.mount(static_path, StaticFiles(
            directory=static_directory), name="static")
        browser(f'http://{"localhost" if self.host == "0.0.0.0" else self.host}:{self.port}')
        uvicorn.run(grapp_server, host=self.host, port=self.port)
