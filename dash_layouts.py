import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import plotly.express as px

from dash_leaflet import Map, TileLayer, GeoJSON
from datetime import datetime
from dash_leaflet.express import dicts_to_geojson
from dash_extensions.javascript import assign

global_graph_config = {"displayModeBar":False,"displaylogo":False,"modeBarButtonsToRemove":["*"],"scrollZoom":False,"showAxisRangeEntryBoxes":False,"showAxisDragHandles":False,"style":{"background-color": "coral"}  }
plot_colors = {
    'background-color': 'rgb(244, 244, 244)'
}
_colors = ["#02124F","#CA3A38","#D77C04","#1A764E"]

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
         html.A([
                    html.Img(src='./assets/ena_logo_2.png',style={"width":"90px","height":"70px"}),
                ], className='navbar-item', href="https://preflet.com", target="_blank",style={"display": "block","width":"100px","height":"80px"}),
        html.Nav([
            html.Div([
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

def create_lastupdated(title='-'):
    return html.Div(html.Div(
        [
            html.P(title, className='sub-title is-4 has-text-right'),
        ]
    ))

def create_indicator(title='-', value='-', info='', size=4):
    return html.Div(
        html.Div([
            html.Div(
                html.H1(value, className='title has-text-white', style={'white-space': 'nowrap','font-weight': 'bold','text-align': 'center','transform': 'scaleY(1.8)','transform': 'scaleX(1.5)'})
            , className='card-content'),
            html.P(title, className='has-text-white', style={'text-align':'center'}) 
        ], className='card', style={'background-color': 'rgb(15, 70, 145)'})
    , className='column is-' + str(size))

def create_piechart(labels=[], values=[], title='', size=6, colors=[],color_discrete_map={}, hole=0.0):
    figure = px.pie({'value': values,'label':labels}, 
        values='value',
        names='label',
        hole=hole,
        color_discrete_map=color_discrete_map,
        color='label',
    )
    figure.update_layout(
        plot_bgcolor=plot_colors['background-color'],
        paper_bgcolor=plot_colors['background-color']
    )
    figure.update_traces(
        hoverinfo='label+percent',
        textinfo='label+percent',
        textfont_size=20,
        # paper_bgcolor='rgb(244, 244, 244)',
        # marker=dict(colors=colors)
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

def create_barchart(labels=[], values=[], title='', size=6, x_axis_label='', y_axis_label='', colors=[],color_discrete_map={}):
    figure = px.bar({y_axis_label: values,x_axis_label:labels}, 
       x=x_axis_label, y=y_axis_label,
       color_discrete_map=color_discrete_map,
       color=x_axis_label
    )
    figure.update_layout(
        plot_bgcolor=plot_colors['background-color'],
        paper_bgcolor=plot_colors['background-color']
    )
    # figure.update_traces(
    #     marker=dict(color=colors)
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

def create_treechart(labels=[],values=[],parents=[],title='',size=6,color_discrete_map={}):
    figure = go.Figure(go.Treemap(
        labels = labels,
        values = values,
        parents = parents,
        root_color="rgb(244, 244, 244)",
        marker=dict(
            colors=['#0066CC', '#D35C59',  '#FCB454', '#61DBA7','#02124F','#CA3A38','#D77C04','#1A764E','#D4EEFF'])
    ))
    figure.update_layout(
        plot_bgcolor=plot_colors['background-color'],
        paper_bgcolor=plot_colors['background-color']
    )
    # figure.update_traces(
    #     marker=dict(colors=colors, line=dict(color='#000000', width=2))
    # )
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

def create_horizontal_barchart(x_axis=[],y_axis=[],color=[],title='',size='',x_axis_label='',y_axis_label='',color_label='',color_discrete_map={}):
    figure = px.bar(  { y_axis_label: y_axis,
                        x_axis_label: x_axis,
                        color_label: color }, 
                        x=x_axis_label, 
                        y=y_axis_label,
                        color=color_label,
                        barmode="stack",
                        color_discrete_map=color_discrete_map
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

def create_bubblechart(x_axis=[],y_axis=[],bubbles=[],title='',size='',x_axis_label='',y_axis_label='',bubble_label='',color_discrete_map={}):
    figure = px.scatter(  { y_axis_label: y_axis,
                        x_axis_label: x_axis,
                        bubble_label: bubbles }, 
                        x=x_axis_label, 
                        y=y_axis_label,
                        size=x_axis_label,
                        color=bubble_label,
                        hover_name=bubble_label,
                        log_x=True, 
                        size_max=60,
                        color_discrete_map=color_discrete_map
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

def create_linechart(x_axis=[],y_axis=[],colors=[],title='',size='',x_axis_label='',y_axis_label='',color_label='',color_discrete_map={}):
    figure = px.line(  { y_axis_label: y_axis,
                        x_axis_label: x_axis,
                        color_label: colors }, 
                        x=x_axis_label, 
                        y=y_axis_label,
                        color=color_label,
                        color_discrete_map=color_discrete_map
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
                        id='line-chart-' + str(title).replace(' ', '-'),
                        figure=figure,
                        config=global_graph_config
                    ),
                ], className='content',),
            className='card-content'),
        ], className='card', style={'background-color': 'rgb(244, 244, 244)'})  
    , className='column is-' + str(size))

def create_areachart(x_axis=[],y_axis=[],colors=[],title='',size='',x_axis_label='',y_axis_label='',line_group='',color_label='',color_discrete_map={}):
    figure = px.area(  { y_axis_label: y_axis,
                        x_axis_label: x_axis,
                        color_label: colors }, 
                        x=x_axis_label, 
                        y=y_axis_label,
                        color_discrete_map=color_discrete_map,
                        color=line_group,
                        line_group=line_group
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
                        id='line-chart-' + str(title).replace(' ', '-'),
                        figure=figure,
                        config=global_graph_config
                    ),
                ], className='content',),
            className='card-content'),
        ], className='card', style={'background-color': 'rgb(244, 244, 244)'})  
    , className='column is-' + str(size))

def create_scatterchart(x_axis=[],y_axis=[],title='',size='',x_axis_label='',y_axis_label='',color_discrete_map={}):
    figure = go.Figure(go.Figure(go.Scatter(x=x_axis, y=y_axis, fill='tozeroy',
                    mode='none'
                    )))
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
                        id='scatter-chart-' + str(title).replace(' ', '-'),
                        figure=figure,
                        config=global_graph_config
                    ),
                ], className='content',),
            className='card-content'),
        ], className='card', style={'background-color': 'rgb(244, 244, 244)'})  
    , className='column is-' + str(size))

def create_horizontal_line_chart(x_axis=[],y_axis=[],title='',size='',x_axis_label='',y_axis_label='',color_discrete_map={}):
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
                    dcc.Graph(
                        id='horizontal-line-chart-' + str(title).replace(' ', '-'),
                        figure=figure,
                        config=global_graph_config
                    ),
                ], className='content',),
            className='card-content'),
        ], className='card', style={'background-color': 'rgb(244, 244, 244)'})  
    , className='column is-' + str(size))