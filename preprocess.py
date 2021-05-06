from db.load import load_from_file
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
import numpy as np

from plotly.subplots import make_subplots

RESTAURANT_REGISTERED = 91
RESTAURANT_ONLINE = 80
CUISINES = 50
LOCATIONS = 45


# Functions
# Returns categories of values of the column

def getlabels(pie_item):
    labels = [i for i in bank_ddf.loc[:, pie_item].unique()]
    return labels


def getvalues(pie_item):
    values = [i for i in bank_ddf.loc[:, pie_item]]
    return values


# Returns sum of Balance after Grouping By pie_item
def getvaluesforbalance(pie_item):
    df2 = bank_ddf.loc[:, ['balance', pie_item]]
    df2 = df2.groupby(pie_item).sum().compute()
    df2 = df2.reset_index(drop=True)
    values = [i for i in df2['balance']]
    return values


bank_ddf = load_from_file('static/bank.csv')
bank_ddf = bank_ddf.drop(columns=['contact', 'day', 'month'])
sample_ddf = pd.read_csv('static/sample.xls')

# For Bank File
options_boxplot = [
    {'label': 'Age', 'value': 'age'},
    {'label': 'Balance', 'value': 'balance'}
]
options_pieplot = [
    {'label': i.title(), 'value': i} for i in ['marital', 'loan', 'housing', 'education', 'job']
]
search_dropdown = dict(label="icecream", value="ice")
option_search_dd = [search_dropdown]

city_names = list(sample_ddf["location"].value_counts()[:10].index)
city_values = list(sample_ddf["location"].value_counts()[:10].values)

city_names2 = sample_ddf["location"][:10]
city_values2 = sample_ddf["location"][:10]

pie_label1 = ["Oxygen", "Hydrogen", "Carbon_Dioxide", "Nitrogen", "Sodium"]
pie_values = [4500, 2500, 1053, 500, 700]

data_imshow = [[1, 25, 30, 50, 1], [20, 1, 60, 80, 30], [30, 60, 1, 5, 20]]

fig_boxplot1 = {
    'data': [
        go.Box(
            y=bank_ddf.age,
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
            y=bank_ddf.balance,
            name='balance'
        )
    ],
    'layout': go.Layout(
        title='Balance Boxplot'
    )
}

fig_scatterplot1 = go.Figure(data=go.Scatter(x=bank_ddf.age, y=bank_ddf.balance, mode='markers'),
                             layout={'title': 'Distribution of Balance with Age'})

fig_barplot2 = go.Figure([go.Bar(x=bank_ddf.age, y=bank_ddf.balance)])

# For Sample File
fig_line = go.Figure(data=go.Scatter(x=city_names,
                                     y=city_values),
                     )

fig_line.add_bar(x=city_names, y=city_values, name="Count")

fig_pie = go.Figure(
    data=[go.Pie(labels=pie_label1, values=pie_values, hole=0.3)])

fig_imshow = px.imshow(
    data_imshow,
    labels=dict(x="Day of Week", y="Time of Day", color="Productivity"),
    x=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
    y=["Morning", "Afternoon", "Evening"],
)
fig_imshow.update_xaxes(side="top")

# For Demographics
fig_area = go.Figure()
fig_area.add_trace(
    go.Scatter(x=[1, 2, 3, 4], y=[0, 2, 3, 5], fill='tozeroy', stackgroup='one', opacity=1, fillcolor="#001540"))
fig_area.add_trace(
    go.Scatter(x=[1, 2, 3, 4], y=[3, 5, 1, 7], fill='tonexty', stackgroup='one', opacity=1, fillcolor="#CB9D06"))

# For Productivity
X = [i for i in range(1, 32)]
barY = np.random.randint(0, 60, 31)
lineY = np.random.randint(0, 10, 31)
fig_barplot3 = make_subplots(specs=[[{"secondary_y": True}]])
fig_barplot3.add_trace(go.Bar(x=X, y=barY, width=0.5, name="Employees", marker=dict(color='darkblue',
                                                                                    )), secondary_y=False)
fig_barplot3.add_trace(go.Scatter(x=X, y=lineY, name="Hours", mode='lines', line=dict(color='orange', width=3)),
                       secondary_y=True)
