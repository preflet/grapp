import load
import plotly.graph_objs as go

load.ddf.drop(columns=['contact', 'day', 'month'])

options_boxplot = [
    {'label': 'Age', 'value': 'age'},
    {'label': 'Balance', 'value': 'balance'}
]

options_pieplot = [
    {'label': i.title(), 'value': i} for i in ['marital', 'loan', 'housing', 'education', 'job']
]

fig_boxplot1 = {
    'data': [
        go.Box(
            y=load.ddf.age,
            name='age'
        )
    ],
    'layout': go.Layout(
        title='Age Boxplot'
    )
}

fig_boxplot2 = {
    'data': [
        go.Box(
            y=load.ddf.balance,
            name='balance'
        )
    ],
    'layout': go.Layout(
        title='Balance Boxplot'
    )
}

fig_scatterplot1 = go.Figure(data=go.Scatter(x=load.ddf.age, y=load.ddf.balance, mode='markers'),
                             layout={'title': 'Distribution of Balance with Age'})

fig_barplot1 = go.Figure([go.Bar(x=load.ddf.age, y=load.ddf.balance)])

# Funtions
#Returns categories of values of the column

def getlabels(pie_item):
    labels = [i for i in load.ddf.loc[:, pie_item].unique().compute()]
    return labels


def getvalues(pie_item):
    values = [i for i in load.ddf.loc[:, pie_item].compute()]
    return values

#Returns sum of Balance after Grouping By pie_item
def getvaluesforbalance(pie_item):
    df2 = load.ddf.loc[:, ['balance', pie_item]]
    df2 = df2.groupby(pie_item).sum().compute()
    df2 = df2.reset_index(drop=True)
    values = [i for i in df2['balance']]
    return values
