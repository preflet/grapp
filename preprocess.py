from db.load import load_from_file
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
import numpy as np

from plotly.subplots import make_subplots
from millify import millify

def indicator(val):
    if 'count' in val:
        c = len(val['count']) if type(val['count']) == list else val['count']
        return millify(c, precision=2)
    return '-'

def piechart(val, _input):
    labels = []
    values = []
    for v in val:
        labels.append(v[_input['output']['labels']])
        values.append(v[_input['output']['values']])
    return {
        'labels': labels,
        'values': values
    }

def barchart(val, _input):
    labels = []
    values = []
    for v in val:
        print(v)
        labels.append(v[_input['output']['labels']])
        values.append(v[_input['output']['values']])
    return {
        'labels': labels,
        'values': values
    }

def treechart(val, _input):
    labels = []
    values = []
    parents = []
    for v in val:
        labels.append(v[_input['output']['labels']])
        values.append(v[_input['output']['values']])
    parents = ["" for i in values ]
    return {
        'labels': labels,
        'values': values,
        'parents':parents
    }

def horizontal_barchart(val, _input):
    x_axis = []
    y_axis = []
    color = []
    for v in val:
        x_axis.append(v[_input['output']['x_axis_label']])
        y_axis.append(v[_input['output']['y_axis_label']])
        color.append(v[_input['output']['color']])
    
    return {
        'x_axis': x_axis,
        'y_axis': y_axis,
        'color': color
    }

def map(val, _input):
    print(val)
    print(_input)
    return {

    }