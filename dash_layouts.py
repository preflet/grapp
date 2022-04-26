import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import plotly.express as px

from dash_leaflet import Map, TileLayer, GeoJSON,WMSTileLayer
from datetime import datetime
from dash_leaflet.express import dicts_to_geojson
from dash_extensions.javascript import assign
from datetime import date

_colors = ["#02124F","#CA3A38","#D77C04","#1A764E"]

global_graph_config = {"displayModeBar":False,"displaylogo":False,"modeBarButtonsToRemove":["*"],"scrollZoom":False,"showAxisRangeEntryBoxes":False,"showAxisDragHandles":False,"style":{"background-color": "coral"}  }
plot_colors = {
    'background-color': 'rgb(244, 244, 244)'
}

def wrap_layout(graph_data):
    routes = []
    for graph in graph_data:
        routes.append(html.A(graph['name'], className='navbar-item', href=graph['route']))
    navigation = None
    if len(routes) > 1:
        # when multiple graphs show a dropdown
        navigation = html.Div([
            html.A('Switch', className='navbar-link'),
            html.Div(routes, className='navbar-dropdown')
        ], className='navbar-item has-dropdown is-hoverable')
    else:
        navigation = ''
        layout = html.Div([
        html.Font(style={"face": "nunito-sans, sans-serif"}),
        dcc.Location(id='url', refresh=False),
        # html.A([
        #             html.Img(src='./assets/ena_logo_2.png'),
        #         ],id="logo", className='navbar-item', target="_blank",style={"position": "absolute",'padding-right': "30px",'padding-bottom':"20px"}),
        html.H1("Barómetro de consumo de energia",className='title is-2 has-text-centered'),
        html.Div([
            html.Div(
                html.Div([
                    html.P("Data", className='has-text-black', style={'text-align':'center'}) ,
                        html.Div([
                            dcc.DatePickerRange(
                                id='date-range',
                                min_date_allowed=date(1995, 8, 5),
                                max_date_allowed=date(2050, 9, 19),
                                initial_visible_month=date(2020, 12, 1),
                                style={"height": "auto","padding": "1.1em"},
                                start_date_placeholder_text = "Data de Início",
                                end_date_placeholder_text = "Data de Fim"
                            )
                        ],className='',style={"display": "flex","justify-content": "center"}),
                    ],className='card'),
            className='column is-6'),

            # html.Div(
            #     html.Div([
            #         html.P("Municípios", className='has-text-black', style={'text-align':'center'}) ,
            #             html.Div([
            #                 dcc.Dropdown(
            #                     id = "muni-dropdown",
            #                     options=[
            #                         {'label': 'Palmela', 'value': 'Palmela'},
            #                         {'label': 'Sesimbra', 'value': 'Sesimbra'},
            #                         {'label': 'Setúbal', 'value': 'Setúbal'}
            #                     ],
            #                     placeholder="Selecione",
            #                     value=[],
            #                     multi=True
            #                 )
            #             ],className='card-content'),
            #     ],className='card'),
            # className='column is-4' ),

            html.Div(
                html.Div([
                    html.P("Tipo de edifícios", className='has-text-black', style={'text-align':'center'}) ,
                        html.Div([
                            dcc.Dropdown(
                                id = 'tepo-dropdown',
                                options=[
                                    {'label': 'Centro Desportivo', 'value': 'Centro Desportivo'},
                                    {'label': 'Centro de Juventude', 'value': 'Centro de Juventude'},
                                    {'label': 'Centro Cultural', 'value': 'Centro Cultural'},
                                    {'label': 'Decorativas', 'value': 'Decorativas'},
                                    {'label': 'Edifício Municipal', 'value': 'Edifício Municipal'},                                    
                                    {'label': 'Escola Básica', 'value': 'Escola Básica'},
                                    {'label': 'Instituição', 'value': 'Instituição'},
                                    {'label': 'Jardim de Infância', 'value': 'Jardim de Infância'},                                    
                                    {'label': 'Mercado', 'value': 'Mercado'},
                                    {'label': 'Museu', 'value': 'Museu'},
                                    {'label': 'Outros', 'value': 'Outros'},
                                    {'label': 'Parque', 'value': 'Parque'},
                                ],
                                placeholder="Selecione",
                                value=[],
                                multi=True
                            )
                    ],className='card-content'),
                ],className='card'),
            className='column is-6' ),
        ], className='columns' ,style={ "margin-top": "3rem"}),
            html.Div(id='page-content')
        ])
    return layout

def create_header(title, description=''):
    return html.Div(html.Div(
        [
            html.H1(title, className='title is-2 has-text-centered'),
            html.P(description, className='sub-title is-4 has-text-centered'),
        ]
    ))

def create_lastupdated(title='-'):
    return html.Div(
        [
            html.P(title, className='sub-title has-text-right'),
        ],className='column is-12'    )

def create_indicator(title='-', size=4,id=''):
    return html.Div(
        html.Div([
            html.Div(
                dcc.Loading(
                    id="loading-1",
                    type="default",
                    children=html.H1(id=id, className='title has-text-white', style={'white-space': 'nowrap','font-weight': 'bold','text-align': 'center'})
                )
            , className='card-content'),
            html.P(title, className='has-text-white', style={'text-align':'center'}) 
        ], className='card', style={'background-color': 'rgb(15, 70, 145)'})
    , className='column is-' + str(size))

def create_piechart(id='',title='',size=''):
    return html.Div(
        html.Div([
            html.Div(
                html.Div([
                    html.H4(title, className='subtitle is-4 has-text-centered is-bold'),
                    dcc.Loading(
                        id="loading-1",
                        type="default",
                        children=dcc.Graph(
                            id=id,
                            config=global_graph_config
                    )
                ) 
                ], className='content',),
            className='card-content'),
        ], className='card', style={'background-color': 'rgb(244, 244, 244)'})  
    , className='column is-' + str(size))

def create_barchart(id='',title='',size=''):
    return html.Div(
        html.Div([
            html.Div(
                html.Div([
                    html.H4(title, className='subtitle is-4 has-text-centered is-bold'),
                    dcc.Loading(
                        id="loading-1",
                        type="default",
                        children=dcc.Graph(
                            id=id,
                            config=global_graph_config
                        )
                    )
                ], className='content',),
            className='card-content'),
        ], className='card', style={'background-color': 'rgb(244, 244, 244)'})  
    , className='column is-' + str(size))

def create_clustered_barchart(id='',title='',size=''):
    return html.Div(
        html.Div([
            html.Div(
                html.Div([
                    html.H4(title, className='subtitle is-4 has-text-centered is-bold'),
                    dcc.Loading(
                        id="loading-1",
                        type="default",
                        children=dcc.Graph(
                            id=id,
                            config=global_graph_config
                        )
                    )
                ], className='content',),
            className='card-content'),
        ], className='card', style={'background-color': 'rgb(244, 244, 244)'})  
    , className='column is-' + str(size))


def create_treechart(id='',title='',size=''):
    return html.Div(
    html.Div([
        html.Div(
            html.Div([
                html.H4(title, className='subtitle is-4 has-text-centered is-bold'),
                dcc.Loading(
                        id="loading-1",
                        type="default",
                        children=dcc.Graph(
                            id=id,
                            config=global_graph_config
                    ))
                ], className='content',),
            className='card-content'),
        ], className='card', style={'background-color': 'rgb(244, 244, 244)'})  
    , className='column is-' + str(size))

def create_horizontal_barchart(id='',title='',size=''):
    return html.Div(
    html.Div([
        html.Div(
            html.Div([
                html.H4(title, className='subtitle is-4 has-text-centered is-bold'),
                dcc.Loading(
                        id="loading-1",
                        type="default",
                        children=dcc.Graph(
                            id=id,
                            config=global_graph_config
                    ))
                ], className='content',),
            className='card-content'),
        ], className='card', style={'background-color': 'rgb(244, 244, 244)'})  
    , className='column is-' + str(size))

def create_bubblechart(id='',title='',size=''):
    return html.Div(
    html.Div([
        html.Div(
            html.Div([
                html.H4(title, className='subtitle is-4 has-text-centered is-bold'),
                    dcc.Loading(
                        id="loading-1",
                        type="default",
                        children=dcc.Graph(
                            id=id,
                            config=global_graph_config
                    ))
                ], className='content',),
            className='card-content'),
        ], className='card', style={'background-color': 'rgb(244, 244, 244)'})  
    , className='column is-' + str(size))

def create_map(id='',title='',size=''):
    point_to_layer = assign("""function(feature, latlng, context){
        return L.circleMarker(latlng);  // sender a simple circle marker.
    }""")  
    
    map = Map(
        children=[
            TileLayer(),
            GeoJSON(
                id='geojson', zoomToBounds=True, options=dict(pointToLayer=point_to_layer)
            )
        ], style={'width': '100%', 'height': '50vh', 'margin': 'auto', 'display': 'block'}, id='map'
    )
 
    return html.Div(
        html.Div([
            html.Div(
                html.Div([
                    html.H4(title, className='subtitle is-4 has-text-centered is-bold'),
                    dcc.Loading(
                        id="loading-1",
                        type="default",
                        children=map
                    )
                    ], className='content',),
                className='card-content'),
            ], className='card', style={'background-color': 'rgb(244, 244, 244)'})  
        , className='column is-' + str(size)
    )

def create_linechart(title='',size='',id=''):
    return html.Div(
    html.Div([
        html.Div(
            html.Div([
                html.H4(title, className='subtitle is-4 has-text-centered is-bold'),
                dcc.Loading(
                        id="loading-1",
                        type="default",
                        children=dcc.Graph(
                            id=id,
                            config=global_graph_config
                    ))
                ], className='content',),
            className='card-content'),
        ], className='card', style={'background-color': 'rgb(244, 244, 244)'})  
    , className='column is-' + str(size))

def create_areachart(title='',size='',id=''):
    return html.Div(
    html.Div([
        html.Div(
            html.Div([
                html.H4(title, className='subtitle is-4 has-text-centered is-bold'),
                    dcc.Loading(
                        id="loading-1",
                        type="default",
                        children=dcc.Graph(
                            id=id,
                            config=global_graph_config
                    ))
                ], className='content',),
            className='card-content'),
        ], className='card', style={'background-color': 'rgb(244, 244, 244)'})  
    , className='column is-' + str(size))

def create_scatterchart(title='',size='',id=''):
    return html.Div(
    html.Div([
        html.Div(
            html.Div([
                html.H4(title, className='subtitle is-4 has-text-centered is-bold'),
                dcc.Loading(
                        id="loading-1",
                        type="default",
                        children=dcc.Graph(
                            id=id,
                            config=global_graph_config
                    ))
                ], className='content',),
            className='card-content'),
        ], className='card', style={'background-color': 'rgb(244, 244, 244)'})  
    , className='column is-' + str(size))

def create_single_line_chart(x_axis=[],y_axis=[],title='',size='',x_axis_label='',y_axis_label='',color_discrete_map={},id=''):
    figure = px.line({x_axis_label:x_axis,y_axis_label:y_axis }, x=x_axis_label, y=y_axis_label, title=title)
    figure.update_layout(
        plot_bgcolor=plot_colors['background-color'],
        paper_bgcolor=plot_colors['background-color']
    )
    return html.Div(
    html.Div([
        html.Div(
            html.Div([
                html.H4(title, className='subtitle is-4 has-text-centered is-bold'),
                dcc.Loading(
                        id="loading-1",
                        type="default",
                        children=dcc.Graph(
                        id=id,
                        figure=figure,
                        config=global_graph_config
                    ))
                ], className='content'),
            className='card-content'),
        ], className='card', style={'background-color': 'rgb(244, 244, 244)'})  
    , className='column is-' + str(size))