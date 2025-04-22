import base64
import io
import pandas as pd
from dash import dcc
import plotly.express as px
import plotly.graph_objects as go

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

    # If xaxis and color are the same column and no yaxis is selected then there wouldn't be a plot generated
    if yaxis is None and xaxis == color:
        return None
    elif yaxis is None:
        # For the Bar chart specifically we allow the yaxis to be not selected by the user and in this case we treat it
        # as the count of the xaxis
        yaxis = 'count'

        group = [xaxis, color] if color is not None else xaxis

        df = df.groupby(group).size().reset_index(name='count')

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
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')), engine = 'pyarrow')
        else:
            df = pd.read_excel(io.BytesIO(decoded))
            # In the case of excel file formats, we need to check for any mixed type columns set their types to str.
            # This is because the later tensforflow data validation process will not handle a column with mixed 
            # type from the excel file format reading.
            for col in df.columns:
                if pd.api.types.infer_dtype(df[col]) in ['mixed', 'mixed-integer']:
                    df[col] = df[col].astype(str)

    except Exception as e:
        print(e)
        return None
    return df
    
def generate_graph(chart_type, xaxis, yaxis, color, df):

    graph = None
    if chart_type[0] == 'L':
        figure = line_plot(xaxis, yaxis, color, df)

    elif chart_type[0] == 'S':
        figure = scatter_plot(xaxis, yaxis, color, df)

    elif chart_type[0] == 'A':
        figure = area_plot(xaxis, yaxis, color, df)

    elif chart_type[0] == 'B':
        figure = bar_plot(xaxis, yaxis, color, df)
        
    if figure is not None:
        figure = layout_update(figure)
        graph = dcc.Graph(figure = figure)

    return graph

def correlation(data):

    df_corr = data.corr().round(2)
    figure = px.imshow(df_corr, text_auto=True)
    figure = layout_update(figure)

    graph = dcc.Graph(figure = figure)
    
    return graph

def parallel_coordinate(data, numeric_features):

    dim = []
    for col in data.columns:
        if col in numeric_features:
            dim.append(dict(label = col, values = data[col]))
        else:
            data[col+'_encoded'] = data[col].astype('category').cat.codes
            labels = data[col].astype('category').cat.categories
            dim.append(dict(label = col, tickvals = list(range(len(labels))),ticktext = list(labels) , values = data[col+'_encoded']))

    figure = go.Figure(data=
                       go.Parcoords(
                           dimensions = dim
))

    figure = layout_update(figure)

    graph = dcc.Graph(figure = figure)

    return graph

def layout_update(figure):

    figure.update_layout(paper_bgcolor = '#333333', title_font = dict(color = 'white'),
                            legend_font = dict(color = 'white'), font=dict(color="white", size=12))
    #figure.update_xaxes(
    #    tickfont=dict(color="white"),  # X-axis ticks
    #    title_font = dict(color = 'white')
    #    )
    #figure.update_yaxes(
    #    tickfont=dict(color="white"),  # Y-axis ticks
    #    title_font = dict(color = 'white')
    #)

    return figure