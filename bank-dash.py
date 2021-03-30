import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import plotly.express as px
import dask.dataframe as dd

ddf = dd.read_csv('assets/bank.csv')
ddf.drop(columns=['contact', 'day', 'month'])
df = ddf.compute()

options_boxplot = [
    {'label': 'Age', 'value': 'age'},
    {'label': 'Balance', 'value': 'balance'}
]

options_pieplot = [
    {'label': i.title(), 'value': i} for i in ['marital', 'loan', 'housing', 'education', 'job']
]

app = dash.Dash(__name__)

app.layout = html.Div(children=
[
    html.Div(
        [
            html.Div(
                [
                    dcc.Graph(
                        id='boxplot',
                        style={"width": "50%", "float": "left"},
                        figure={
                            'data': [
                                go.Box(
                                    y=ddf.age.compute(),
                                    name='age'
                                )
                            ],
                            'layout': go.Layout(
                                title='Age Boxplot'
                            )
                        }
                    ),
                    dcc.Graph(
                        id='boxplot2',
                        style={"width": "50%", "float": "right"},
                        figure={
                            'data': [
                                go.Box(
                                    y=ddf.balance.compute(),
                                    name='balance'
                                )
                            ],
                            'layout': go.Layout(
                                title='Balance Boxplot'
                            )
                        }
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
                options=options_pieplot,
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
                figure=go.Figure(
                    data=[go.Pie(labels=[i for i in ddf.job.unique().compute()], values=ddf.job.compute())]),
                # px.pie(df, names='job', title="Distribution of Jobs"),
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
                figure=px.scatter(data_frame=df, x='age', y='balance',
                                  title='Distribution of Balance with Age')
            ),
            dcc.Graph(
                id='barPlot',
                figure=px.bar(data_frame=df, x='age', y='balance', color='education')
            )
        ],
        id='div-bar'
    )
]
)


def getlabels(pie_item):
    labels = [i for i in ddf.loc[:, pie_item].unique().compute()]
    return labels


def getvalues(pie_item):
    values = [i for i in ddf.loc[:, pie_item].compute()]
    return values


def getvaluesforbalance(pie_item):
    df2 = ddf.loc[:, ['balance', pie_item]]
    df2 = df2.groupby(pie_item).sum().compute()
    values = df2.reset_index(drop=True)
    return values


@app.callback(Output('piePlot1', 'figure'),
              [Input('pie-dropdown', 'value')])
def update_figure(pie_item):
    return go.Figure(
        data=[
            go.Pie(labels=getvalues(pie_item))], layout={"title": f"Distribution of {pie_item.title()}"})


@app.callback(Output('piePlot2', 'figure'),
              [Input('pie-dropdown', 'value')])
def update_figure(pie_item):
    return px.pie(df, names=pie_item, values='balance', title=f"Distribution of Balance over {pie_item.title()}")


if __name__ == "__main__":
    app.run_server()
