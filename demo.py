import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
import random

app.layout = html.Div([
    dcc.Input(
        id='num-multi',
        type='number',
        value=5
    ),
    html.Table([
        # html.Tr([html.Td(['x', html.Sup(2)]), html.Td(id='square')]),
        # html.Tr([html.Td(['x', html.Sup(3)]), html.Td(id='cube')]),
        # html.Tr([html.Td([2, html.Sup('x')]), html.Td(id='twos')]),
        # html.Tr([html.Td([3, html.Sup('x')]), html.Td(id='threes')]),
        # html.Tr([html.Td(['x', html.Sup('x')]), html.Td(id='x^x')]),
    ]),
    html.Div(
        html.Div([
            html.Div(
                html.Div([
                    html.H4("title", className='subtitle is-4 has-text-centered is-bold'),
                    dcc.Graph(
                        id='pie-chart'
                    ),
                ], className='content',),
            className='card-content'),
        ], className='card', style={'background-color': 'rgb(244, 244, 244)'})  
    , className='column is-' + '6')
])


@app.callback(
    # Output('square', 'children'),
    # Output('cube', 'children'),
    # Output('twos', 'children'),
    # Output('threes', 'children'),
    Output('pie-chart', 'figure'),
    Input('date-range', 'value'))
def callback_a(x):
    year = [random.randrange(1, 50, 1) for i in range(7)]
    lifeExp = [random.randrange(1, 50, 1) for i in range(7)]

    figure = px.line({
                    "year":year,
                    "lifeExp":lifeExp
                    }, x="year", y="lifeExp", title='Life expectancy in Canada')

    return figure


if __name__ == '__main__':
    app.run_server(debug=True)