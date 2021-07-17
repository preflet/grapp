import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import plotly.express as px

from dash_leaflet import Map, TileLayer, GeoJSON
from datetime import datetime
from dash_leaflet.express import dicts_to_geojson
from dash_extensions.javascript import assign
from datetime import date

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
        html.Div(id='page-content'),
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

def create_piechart(labels=[], values=[], title='', size=6, colors=[], hole=0.0):
    figure = px.pie({'value': values,'label':labels}, 
        values='value',
        names='label',
        hole=hole
    )
    figure.update_layout(
        plot_bgcolor=plot_colors['background-color'],
        paper_bgcolor=plot_colors['background-color']
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

def create_barchart(labels=[], values=[], title='', size=6, x_axis_label='', y_axis_label='', colors=[]):
    figure = px.bar({y_axis_label: values,x_axis_label:labels}, 
       x=x_axis_label, y=y_axis_label,
    )
    figure.update_layout(
        plot_bgcolor=plot_colors['background-color'],
        paper_bgcolor=plot_colors['background-color']
    )
    figure.update_traces(
        marker=dict(color=colors, line=dict(color='#000000', width=2))
    )
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

def create_treechart(labels=[],values=[],parents=[],title='',size=6, colors=[]):
    figure = go.Figure(go.Treemap(
        labels = labels,
        values = values,
        parents = parents,
        root_color="lightblue"
    ))
    figure.update_layout(
        plot_bgcolor=plot_colors['background-color'],
        paper_bgcolor=plot_colors['background-color']
    )
    figure.update_traces(
        marker=dict(colors=colors, line=dict(color='#000000', width=2))
    )
    return html.Div(
    html.Div([
        html.Div(
            html.Div([
                html.H4(title, className='subtitle is-4 has-text-centered is-bold'),
                    dcc.Graph(
                        id='tree-chart-' + str(title).replace(' ', '-'),
                        figure=figure,
                        config=global_graph_config
                    ),
                ], className='content',),
            className='card-content'),
        ], className='card', style={'background-color': 'rgb(244, 244, 244)'})  
    , className='column is-' + str(size))

def create_horizontal_barchart(x_axis=[],y_axis=[],color=[],title='',size='',x_axis_label='',y_axis_label='',color_label=''):
    figure = px.bar(  { y_axis_label: y_axis,
                        x_axis_label: x_axis,
                        color_label: color }, 
                        x=x_axis_label, 
                        y=y_axis_label,
                        color=color_label,
                        barmode="stack"
                    )
    figure.update_layout(
        plot_bgcolor=plot_colors['background-color'],
        paper_bgcolor=plot_colors['background-color']
    )
    return html.Div(
    html.Div([
        html.Div(
            html.Div([
                html.H4(title, className='subtitle is-4 has-text-centered is-bold'),
                    dcc.Graph(
                        id='horizontal-bar-chart-' + str(title).replace(' ', '-'),
                        figure=figure,
                        config=global_graph_config
                    ),
                ], className='content',),
            className='card-content'),
        ], className='card', style={'background-color': 'rgb(244, 244, 244)'})  
    , className='column is-' + str(size))

def create_bubblechart(x_axis=[],y_axis=[],bubbles=[],title='',size='',x_axis_label='',y_axis_label='',bubble_label=''):
    figure = px.scatter(  { y_axis_label: y_axis,
                        x_axis_label: x_axis,
                        bubble_label: bubbles }, 
                        x=x_axis_label, 
                        y=y_axis_label,
                        size=x_axis_label,
                        color=bubble_label,
                        hover_name=bubble_label,
                        log_x=True, 
                        size_max=60
                    )
    figure.update_layout(
        plot_bgcolor=plot_colors['background-color'],
        paper_bgcolor=plot_colors['background-color']
    )
    return html.Div(
    html.Div([
        html.Div(
            html.Div([
                html.H4(title, className='subtitle is-4 has-text-centered is-bold'),
                    dcc.Graph(
                        id='bubble-chart-' + str(title).replace(' ', '-'),
                        figure=figure,
                        config=global_graph_config
                    ),
                ], className='content',),
            className='card-content'),
        ], className='card', style={'background-color': 'rgb(244, 244, 244)'})  
    , className='column is-' + str(size))

def create_map(title='', data=[], size=6):
    geojson = dicts_to_geojson([{**d, **dict(tooltip=d['name'])} for d in data])
    dd_options = [dict(value=c['name'], label=c['name']) for c in data]
    dd_defaults = [o['value'] for o in dd_options]
    dd_defaults = list(set(dd_defaults))
    point_to_layer = assign("""function(feature, latlng, context){
        return L.circleMarker(latlng);  // sender a simple circle marker.
    }""")
    map = Map(
        children=[
            TileLayer(),
            GeoJSON(
                data=geojson, hideout=dd_defaults, id='geojson', zoomToBounds=True, options=dict(pointToLayer=point_to_layer)
            )
        ], style={'width': '100%', 'height': '50vh', 'margin': 'auto', 'display': 'block'}, id='map'
    )

                
    return html.Div(
        html.Div([
            html.Div(
                html.Div([
                    html.H4(title, className='subtitle is-4 has-text-centered is-bold'),
                    map,
                    ], className='content',),
                className='card-content'),
            ], className='card', style={'background-color': 'rgb(244, 244, 244)'})  
        , className='column is-' + str(size)
    )

def create_filters(filters):
    layout = []
    base_query = []
    for filter in filters:
        if filter['filter_type'] == 'DatePickerRange':
            layout.append(
                html.Div(
                    dcc.DatePickerRange(
                        id='date-picker',
                    )
                , className='column is-' + str(filter['size']))
            )
        elif filter['filter_type'] == 'DatePickerSingle':
            layout.append(
                html.Div(
                    dcc.DatePickerSingle(
                        id='date-picker',
                    )
                , className='column is-' + str(filter['size']))
            )
        # add query to base
        base_query.append({
            'type': filter['filter_type'],
            'query': filter['query']
        })
        
    # fake output
    layout.append(html.Div(id='output-date-picker'))
    return html.Div(layout, className='columns'), base_query