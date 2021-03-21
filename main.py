import dash
import dash_core_components as dcc
import dash_html_components as html
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import squarify
import uvicorn as uvicorn
from dash.dependencies import Input, Output, State
from fastapi import FastAPI
from starlette.middleware.wsgi import WSGIMiddleware

df = pd.read_csv("assets/sample.xls")

x = dict(label="icecream", value="ice")
option = [x]

t1 = 91
t2 = 80
t3 = 50
t4 = 45


names = list(df["location"].value_counts()[:10].index)
values = list(df["location"].value_counts()[:10].values)


names2 = df["location"][:10]
values2 = df["location"][:10]


import plotly.express as px

fig = go.Figure()

fig = px.line(
    x=names,
    y=values,
    color=px.Constant("This year"),
    labels=dict(x="Names", y="Values", color="Names vs values"),
)
fig.add_bar(x=names, y=values, name="Count")

label1 = ["Oxygen", "Hydrogen", "Carbon_Dioxide", "Nitrogen", "Sodium"]
value1 = [4500, 2500, 1053, 500, 700]

fig_do = go.Figure(data=[go.Pie(labels=label1, values=value1, hole=0.3)])

labels = ["A1", "A2", "A3", "A4", "A5", "B1", "B2"]
parents = ["", "A1", "A2", "A3", "A4", "", "B1"]
fig3 = go.Figure(
    go.Treemap(labels=labels, parents=parents, values=[10, 20, 14, 24, 32, 41, 22])
)


data = [[1, 25, 30, 50, 1], [20, 1, 60, 80, 30], [30, 60, 1, 5, 20]]
fig4 = px.imshow(
    data,
    labels=dict(x="Day of Week", y="Time of Day", color="Productivity"),
    x=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
    y=["Morning", "Afternoon", "Evening"],
)
fig4.update_xaxes(side="top")


app = dash.Dash(__name__)  # requests_pathname_prefix='/dash/'


app.layout = html.Div(
    [
        # search dropdown
        html.Div(
            [
                dcc.Dropdown(
                    id="hotels-dropdown",
                    className="dropclass",
                    options=option,
                    value="(key-value)",
                    style={"width": "550px", "display": "inline-block"},
                ),
                html.Img(
                    src="/assets/searchlogo3.png",
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
                                    children="Total No. of Restaurents Registered:  ",
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
                                    children=f"{t1}",
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
                                    children="Total No. of Restaurents for Online Delivery :",
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
                                    children=f"{t2}",
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
                                    children=f"{t3}",
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
                                    children=f"{t4}",
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
            dcc.Graph(figure=fig),
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
                    figure=fig_do,
                    style={
                        "width": "45%",
                        "border": "2px solid #6d9399",
                        "border-radius": "10px",
                        "margin-left": "20px",
                        "display": "inline-block",
                    },
                ),
                dcc.Graph(
                    figure=fig4,
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
    ]
)


if __name__ == "__main__":
    app.run_server()
