import dash_core_components as dcc
import dash_html_components as html
import preprocess

from datetime import datetime

sample_layout = html.Div(
    [
        html.Div([
            html.H1('Hello Dash'),
            html.Div([
                html.P('Dash converts Python classes into HTML'),
                html.P(
                    "This conversion happens behind the scenes by Dash's JavaScript front-end")
            ])
        ]),
        # search dropdown
        html.Div(
            [
                dcc.Dropdown(
                    id="hotels-dropdown",
                    className="dropclass",
                    options=preprocess.option_search_dd,
                    value="(key-value)",
                    style={"width": "550px", "display": "inline-block"},
                ),
                html.Img(
                    src="/static/searchlogo3.png",
                    className="searchlogo",
                    style={
                        "display": "inline-block",
                        "height": "31px",
                        "width": "34px",
                        "margin-left": "10px",
                    },
                ),
            ]
        ),
        html.Div(className="gap"),
        html.Div(className="gap"),
        html.Div(className="gap"),
        # tabs
        html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div(
                                    children="Total No. of Restaurants Registered:  ",
                                    className="box1",
                                    style={
                                        "backgroundColor": "#60c0e0",
                                        "padding-top": "5px",
                                        "border-radius": "15px 15px 0px 0px",
                                        "color": "black",
                                        "height": "35px",
                                        "margin-left": "10px",
                                        "width": "100%",
                                        "text-align": "center",
                                    },
                                ),
                                html.Div(
                                    children=f"{preprocess.RESTAURANT_REGISTERED}",
                                    className="box1op",
                                    style={
                                        "backgroundColor": "#60c0e0",
                                        "border-radius": "0px 0px 15px 15px",
                                        "color": "black",
                                        "height": "55px",
                                        "margin-left": "10px",
                                        "text-align": "center",
                                        "width": "100%",
                                    },
                                ),
                            ],
                            style={
                                "display": "inline-block",
                                "width": "22%",
                                "margin-left": "65px",
                            },
                        ),
                        html.Div(
                            [
                                html.Div(
                                    children="Total No. of Restaurants for Online Delivery :",
                                    className="box2",
                                    style={
                                        "backgroundColor": "#60c0e0",
                                        "color": "black",
                                        "padding-top": "5px",
                                        "border-radius": "15px 15px 0px 0px",
                                        "height": "35px",
                                        "margin-left": "10px",
                                        "text-align": "center",
                                        "width": "100%",
                                    },
                                ),
                                html.Div(
                                    children=f"{preprocess.RESTAURANT_ONLINE}",
                                    className="box2op",
                                    style={
                                        "backgroundColor": "#60c0e0",
                                        "color": "black",
                                        "border-radius": "0px 0px 15px 15px",
                                        "height": "55px",
                                        "margin-left": "10px",
                                        "text-align": "center",
                                        "width": "100%",
                                    },
                                ),
                            ],
                            style={
                                "display": "inline-block",
                                "width": "22%",
                                "margin-left": "10px",
                            },
                        ),
                        html.Div(
                            [
                                html.Div(
                                    children="Types Of Cuisines Served :",
                                    className="box3",
                                    style={
                                        "backgroundColor": "#60c0e0",
                                        "color": "black",
                                        "padding-top": "5px",
                                        "border-radius": "15px 15px 0px 0px",
                                        "height": "35px",
                                        "margin-left": "10px",
                                        "width": "100%",
                                        "text-align": "center",
                                    },
                                ),
                                html.Div(
                                    children=f"{preprocess.CUISINES}",
                                    className="box3op",
                                    style={
                                        "backgroundColor": "#60c0e0",
                                        "color": "black",
                                        "border-radius": "0px 0px 15px 15px",
                                        "height": "55px",
                                        "margin-left": "10px",
                                        "text-align": "center",
                                        "width": "100%",
                                    },
                                ),
                            ],
                            style={
                                "display": "inline-block",
                                "width": "22%",
                                "margin-left": "10px",
                            },
                        ),
                        html.Div(
                            [
                                html.Div(
                                    children="Number Of Locations Served :  ",
                                    className="box4",
                                    style={
                                        "backgroundColor": "#60c0e0",
                                        "color": "black",
                                        "padding-top": "5px",
                                        "border-radius": "15px 15px 0px 0px",
                                        "height": "35px",
                                        "margin-left": "10px",
                                        "width": "100%",
                                        "text-align": "center",
                                    },
                                ),
                                html.Div(
                                    children=f"{preprocess.LOCATIONS}",
                                    className="box4op",
                                    style={
                                        "backgroundColor": "#60c0e0",
                                        "color": "black",
                                        "height": "55px",
                                        "border-radius": "0px 0px 15px 15px",
                                        "margin-left": "10px",
                                        "text-align": "center",
                                        "width": "100%",
                                    },
                                ),
                            ],
                            style={
                                "display": "inline-block",
                                "margin-left": "10px",
                                "width": "22%",
                            },
                        ),
                    ]
                )
            ]
        ),
        html.Div(className="gap"),
        html.Div(className="gap"),
        html.Div(
            dcc.Graph(figure=preprocess.fig_line),
            style={
                "width": "90%",
                "border": "2px solid #6d9399",
                "border-radius": "10px",
                "margin-left": "20px",
            },
        ),
        html.Div(className="gap"),
        html.Div(className="gap"),
        html.Div(
            [
                dcc.Graph(
                    figure=preprocess.fig_pie,
                    style={
                        "width": "45%",
                        "border": "2px solid #6d9399",
                        "border-radius": "10px",
                        "margin-left": "20px",
                        "display": "inline-block",
                    },
                ),
                dcc.Graph(
                    figure=preprocess.fig_imshow,
                    style={
                        "width": "45%",
                        "border": "2px solid #6d9399",
                        "border-radius": "10px",
                        "margin-left": "30px",
                        "display": "inline-block",
                    },
                ),
            ]
        ),
        html.Div(className="gap"),
        html.Div(className="gap"),

        html.Div(
            [
                html.Div(
                    [
                        dcc.Graph(
                            id='boxplot',
                            style={"width": "50%", "float": "left"},
                            figure=preprocess.fig_boxplot1
                        ),
                        dcc.Graph(
                            id='boxplot2',
                            style={"width": "50%", "float": "right"},
                            figure=preprocess.fig_boxplot2
                        )
                    ], style={"width": "100%"}
                )
            ]
        ),
        html.Div(
            [
                dcc.Dropdown(
                    id="pie-dropdown",
                    className="dropclass",
                    options=preprocess.options_pieplot,
                    value="job",
                    clearable=False,
                    style={
                        "width": "40%",
                        "text-align": "center",
                        "margin": "auto"
                    },
                )], style={"width": "100%"}),
        html.Div(
            [
                dcc.Graph(
                    id='piePlot1',
                    style={"width": "50%", "float": "left",
                           "display": "inline", "text-align": "center"},
                ),
                dcc.Graph(
                    id='piePlot2',
                    style={"width": "50%", "float": "right",
                           "display": "inline", "text-align": "center"}
                )
            ], style={"width": "100%", "display": "inline-block"}
        ),

        html.Div(
            [
                dcc.Graph(
                    id='scatterPlot',
                    figure=preprocess.fig_scatterplot1
                ),
                dcc.Graph(
                    id='barPlot',
                    figure=preprocess.fig_barplot2
                )
            ],
            id='div-bar'
        )

    ]
)

def get_all_graph_routes_layout(graph_data):
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
        dcc.Location(id='url', refresh=True),
        html.Div(
            id='page-content',
            children=html.Nav()
        ),
        html.Nav([
            html.Div([
                html.A([
                    html.Img(src='https://www.preflet.com/assets/img/imgs/logo.png'),
                ], className='navbar-item', href="https://preflet.com")
            ], className='navbar-brand'),
            html.Div([
                html.Div([
                    navigation
                ], className='navbar-end')
            ], className='navbar-menu')
        ], 
        className='navbar',
        role="navigation",
        ),
    ])
    return layout

def create_header(title, description=''):
    return html.Div([
        # html.Row(
        #     [
        #         html.H1(title)
        #     ], justify="center", align="center", className="h-50"
        # ),
        html.Div([
            html.P(description),
        ])
    ]),

def create_layout(graph):
    graph_ = {}
    header = create_header(graph['name'], graph['description'] if 'description' in graph else '')
    layout = html.Div(header)
    graph_[graph['route']] = layout
    return graph_
