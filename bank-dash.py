import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input, Output

import preprocess

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
                figure=preprocess.fig_barplot1
            )
        ],
        id='div-bar'
    )
]
)


@app.callback(Output('piePlot1', 'figure'),
              [Input('pie-dropdown', 'value')])
def update_figure(pie_item):
    return go.Figure(
        data=[
            go.Pie(labels=preprocess.getvalues(pie_item))], layout={"title": f"Distribution of {pie_item.title()}"})


@app.callback(Output('piePlot2', 'figure'),
              [Input('pie-dropdown', 'value')])
def update_figure(pie_item):
    return go.Figure(
        data=[
            go.Pie(labels=preprocess.getlabels(pie_item), values=preprocess.getvaluesforbalance(pie_item))],
        layout={"title": f"Distribution of Balance over {pie_item.title()}"})


if __name__ == "__main__":
    app.run_server()
