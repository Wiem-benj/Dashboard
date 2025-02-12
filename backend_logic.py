import base64
import io
import pandas as pd
from dash import dcc
import plotly.express as px

def line_plot(xaxis, yaxis, color, df):

    figure = px.line(df,
        x = xaxis,
        y = yaxis,
        color = color,
        title = 'Line chart')
    
    return figure

def scatter_plot(xaxis, yaxis, color, df):
    figure = px.scatter(df,
                        x = xaxis,
                        y = yaxis,
                        color = color,
                        title = 'Scatter plot')
    return figure


def area_plot(xaxis, yaxis, color, df):

    figure = px.area(df,
                     x = xaxis,
                     y = yaxis,
                     color = color,
                     title = 'Area plot')

    return figure


def bar_plot(xaxis, yaxis, color, df):

    figure = px.bar(df,
                    x = xaxis,
                    y = yaxis,
                    color = color,
                    title = 'Bar Plot')

    return figure


def read_data(contents, filename):
    
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    
    try:
        if '.csv' in filename.lower():
            # Read CSV file
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        else:
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return None
    
    return df
    
def generate_graph(chart_type, xaxis, yaxis, color, df):

    graph = None
    if chart_type[0] == 'L':
        graph = dcc.Graph(
            figure = line_plot(xaxis, yaxis, color, df)
        )
    elif chart_type[0] == 'S':
        graph = dcc.Graph(
            figure = scatter_plot(xaxis, yaxis, color, df)
        )
    elif chart_type[0] == 'A':
        graph = dcc.Graph(
            figure = area_plot(xaxis, yaxis, color, df)
        )

    elif chart_type[0] == 'B':
        graph = dcc.Graph(
            figure = bar_plot(xaxis, yaxis, color, df)
        )

    return graph

