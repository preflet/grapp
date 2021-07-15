import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import plotly.express as px

from datetime import datetime
global_graph_config = {"displayModeBar":False,"displaylogo":False,"modeBarButtonsToRemove":["*"],"scrollZoom":False,"showAxisRangeEntryBoxes":False,"showAxisDragHandles":False  }

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
        dcc.Location(id='url', refresh=False),
        html.Nav([
            html.Div([
                html.A([
                    html.Img(src='https://www.preflet.com/assets/img/imgs/logo.png'),
                ], className='navbar-item', href="https://preflet.com", target="_blank"),
                html.A([
                    html.Span(hidden='true'),
                    html.Span(hidden='true'),
                    html.Span(hidden='true')
                ], className='navbar-burger')
            ], className='navbar-brand'),
            html.Div([
                html.Div([
                    navigation
                ], className='navbar-start')
            ], className='navbar-menu', id='grapp-nav')
        ], 
        className='navbar',
        role="navigation",
        ),
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

def create_indicator(title='-', value='-', info='', size=4):
    return html.Div(
        html.Div([
            html.P(title, className='card-header-title has-text-white', style={'white-space': 'nowrap'}),
            html.Div(
                html.H1(value, className='title has-text-white', style={'white-space': 'nowrap'})
            , className='card-content')
        ], className='card', style={'background-color': 'rgb(15, 70, 145)'})    
    , className='column is-' + str(size))

def create_piechart(labels=[], values=[], title='', size=6, colors=[]):
    figure = px.pie({'value': values,'label':labels}, 
        values='value',
        names='label',
    )
    figure.update_traces(
        hoverinfo='label+percent',
        textinfo='value',
        textfont_size=20,
        # paper_bgcolor='rgb(244, 244, 244)',
        marker=dict(colors=colors, line=dict(color='#000000', width=2))
    )
    return html.Div(
        html.Div([
            html.Div(
                html.Div([
                    html.H4(title, className='subtitle is-4 has-text-centered is-bold'),
                    dcc.Graph(
                        id='pie-chart-' + str(title).replace(' ', '-'),
                        figure=figure,
                        config=global_graph_config
                    ),
                ], className='content',),
            className='card-content'),
        ], className='card', style={'background-color': 'rgb(244, 244, 244)'})  
    , className='column is-' + str(size))

def create_barchart(labels=[], values=[], title='', size=6,x_axis_label='',y_axis_label=''):
    figure = px.bar({y_axis_label: values,x_axis_label:labels}, 
       x=x_axis_label, y=y_axis_label
    )
    # figure.update_traces(
    #     hoverinfo='label+percent',
    #     # textinfo='value',
    #     textfont_size=20,
    #     # paper_bgcolor='rgb(244, 244, 244)',
    #     # marker=dict(colors=colors, line=dict(color='#000000', width=2))
    # )
    return html.Div(
        html.Div([
            html.Div(
                html.Div([
                    html.H4(title, className='subtitle is-4 has-text-centered is-bold'),
                    dcc.Graph(
                        id='bar-chart-' + str(title).replace(' ', '-'),
                        figure=figure,
                        config=global_graph_config
                    ),
                ], className='content',),
            className='card-content'),
        ], className='card', style={'background-color': 'rgb(244, 244, 244)'})  
    , className='column is-' + str(size))