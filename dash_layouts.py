import dash_core_components as dcc
import dash_html_components as html
import preprocess

layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

index_layout = html.Div(
    [html.Div([
        dcc.Link('Productivity', href='/productivity'),
        html.Br(),
        dcc.Link('Demographics', href='/demographics'),
        html.Br(),
        dcc.Link('Sample', href='/sample'),
    ])])

sample_layout = html.Div(
    [
        html.Div([
            html.H1('Hello Dash'),
            html.Div([
                html.P('Dash converts Python classes into HTML'),
                html.P("This conversion happens behind the scenes by Dash's JavaScript front-end")
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
                    style={"width": "50%", "float": "left", "display": "inline", "text-align": "center"},
                ),
                dcc.Graph(
                    id='piePlot2',
                    style={"width": "50%", "float": "right", "display": "inline", "text-align": "center"}
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

demographics_layout = html.Div([
    html.Div([
        html.Div(children='Time and Attendance', style={"font-size": "40px",
                                                        "color": "#0275d8", "margin-bottom": "10px"}),
        html.Div('The key facts about Ristro Rail employees in October', style={"font-size": "20px"})
    ]),
    html.Br(),
    html.Div([
        html.Div([
            html.H1('15.9%', className="flex-h1"),
            html.Div('Irregularities*', className="flex-div")
        ]),
        html.Div([
            html.H1('13.5%', className="flex-h1"),
            html.Div('Late Arrival*', className="flex-div")
        ]),
        html.Div([
            html.H1('12.7%', className="flex-h1"),
            html.Div('Leave Early*', className="flex-div")
        ]),
        html.Div([
            html.H1('21.3%', className="flex-h1"),
            html.Div('Work on Weekends', className="flex-div")
        ])
    ], className="flexbox-container", style={"width": "100%"}),
    html.Br(),
    html.Br(),
    html.Div(
        [
            dcc.Graph(
                id='areaPlot',
                figure=preprocess.fig_area,
            ),
        ],
        id='div-area',
        style={"align-content": "center"}
    ),
    html.Div([
        html.Div("*Irregularity: when employee do not punch out", style={"margin-bottom": "10px"}),
        html.Div('*Late Arrival/Leave Early: by 20 minutes difference from the nearest hour')
    ], style={"font-size": "20px"}),

], style={"font-family": "serif", "padding": "20px"})


productivity_layout = html.Div([
    html.Div([
        html.Div('Workhours Overview', style={"font-size": "40px",
                                                        "color": "#0275d8", "margin-bottom": "10px"}),
        html.Div('The key facts about Ristro Rail employees in October', style={"font-size": "20px"})
    ]),
    html.Br(),
    html.Div([
        html.Div([
            html.H1('52', className="flex-h1"),
            html.Div('Employees/day', className="flex-div")
        ]),
        html.Div([
            html.H1('8:16', className="flex-h1"),
            html.Div('Avg Hours/day', className="flex-div")
        ]),
        html.Div([
            html.H1('00:47', className="flex-h1"),
            html.Div('Avg Breaktime', className="flex-div")
        ]),
        html.Div([
            html.H1('93.4%', className="flex-h1"),
            html.Div('Productivity*', className="flex-div")
        ])
    ], className="flexbox-container", style={"width": "100%"}),
    html.Br(),
    html.Br(),
    html.Div(
        [
            dcc.Graph(
                id='areaPlot',
                figure=preprocess.fig_barplot3,
            ),
        ],
        id='div-area',
        style={"align-content": "center"}
    ),
    html.Div([
        html.Div("*Productivity: % total hours without break by 8 hours"),
    ], style={"font-size": "20px"}),

], style={"font-family": "serif", "padding": "20px"})
