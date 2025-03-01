'''
Created by: Wiem Ben jmaa
Date: 10/02/2025

This main file contains the layout of the dashboard
The file 'backend_logic' contains the logic behind the callbacks function, etc.
'''
import dash
#import more_itertools
from dash import dcc, html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import dash_bootstrap_components as dbc
import backend_logic
import tensorflow_data_validation as tfdv
from tensorflow_data_validation.utils.display_util import get_statistics_html

df = None
# Initialize the Dash app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

def dropdown_template(name, is_multi, options = {'':''}):
    '''
    This function generate dropdown lists, with the options values passed to it.
    
    parameters:
    ------------
    name: str
        The name of the dropdown list, which is used as id as well.

    is_multi: boolean
        A boolean value that indicates if the dropdown list is expected to accept multiple values or a single value.

    options: dict
        A dictionary that must contains the value choices of the dropdown list.

    return:
    --------
    dropdown: html.Div
        A div html container which contains the dropdown list with the options specified in the paramater options

    '''

    dropdown = html.Div([
                html.Label('Select the {:}'.format(name), style = {'color':'white'}),
                dcc.Dropdown(
                    id = name,
                    options = options,
                    #value = 'Select chart type',
                    placeholder = 'Select {:}'.format(name),
                    disabled = True,
                    multi = is_multi
                )
                ])
    
    return dropdown


app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
# This line of code needed in the step of deploying the dashboard web application online for free in Render.  
server = app.server

# Set the title of the dashboard
header = html.Div(children = 'Dashboard for Data visualization', className = 'header')

# row_1 contains 3 parts which highlights the selection of the file
row_1 = html.Div([
                html.Div('Start by selecting a csv or xlsx file', id = 'select-file', 
                         style = {'display':'inline-block', 'height': '50px', 'margin-right':'10px', 'color': 'white'}),
                html.Div([
                    dcc.Upload(
                    id = 'upload-data',
                    children = dbc.Button('📁 Browse CSV or XLSX File', color='primary', className='mt-2', size='lg'),
                    multiple = False,
                    accept = '.csv, .xlsx',
                    )], style={'display': 'inline-block', 'vertical-align': 'middle', 'backgroundColor': 'white'}),
                    html.Div(
                        id='output-data-upload', style={'display': 'inline-block', 'vertical-align': 'middle',
                                                        'margin-left': '10px', 'fontWeight': 'bold'})
                    
])

chart_type = dropdown_template('chart type', False, {'Line Chart': 'Line Chart', 'Scatter Chart': 'Scatter Chart', 
'Area Chart': 'Area Chart', 'Bar Chart': 'Bar Chart'})

x_axis = dropdown_template('x-axis', False)

y_axis = dropdown_template('y-axis', False)

color = dropdown_template('color', False)

tab_1 = html.Div(id = 'data-analysis', style = {'backgroundColor': 'white', 'width': '100%'})

# row_2 contains a first part which include the 1st column with the select type chart drop down and the variable choices part
# The second column which is the larger is the plot
tab_2 = html.Div([
        # main layout
        html.Div([
            #Left column layout
            html.Div([
                chart_type,
                x_axis,
                y_axis,
                color
            ], className = 'leftcolumn'),
            # Right column
            html.Div([
                 html.Div(id = 'container')
            ], className = 'rightcolumn')
        ], style={
        'display': 'flex',  # Flexbox to arrange columns
        'width': '100vw'#,  # Full viewport width
    })
])

eda_type = html.Div([
    html.Label('Select the EDA', style = {'color':'white'}),
    dcc.Dropdown(
        id = 'eda-type',
        options = {'Correlation':'Correlation', 'Parallel coordinate':'Parallel coordinate'},
        #value = 'Select chart type',
        placeholder = 'Select the EDA',
        disabled = False
    )
    ])

features = dropdown_template('features', True)

tab_3 = html.Div([
        # main layout
        html.Div([
            #Left column layout
            html.Div([
                eda_type,
                features
            ], className = 'leftcolumn'),
            # Right column
            html.Div([
                 html.Div(id = 'eda')
            ], className = 'rightcolumn')
        ], style={
        'display': 'flex',  # Flexbox to arrange columns
        'width': '100vw'#,  # Full viewport width
    })
])


layout = html.Div(children=[header, row_1, 
                            dcc.Tabs(id = 'tabs_content', value='tab-1-example-graph',
                            children = [
                                dcc.Tab(label = 'Data analysis', value = 'tab1', children = tab_1),
                                dcc.Tab(label = 'Charts', value = 'tab2', children= tab_2),
                                dcc.Tab(label = 'Exploratory Data Analysis', value = 'tab3', children= tab_3),
                            ])
                            ])

app.layout = layout

# Reading the file through the upload button. To populate the options for the dropdown lists of axis
@app.callback(
    Output('output-data-upload', 'children'),
    Output('chart type', 'disabled'), 
    Output('x-axis', 'options'),
    Output('y-axis', 'options'),
    Output('color', 'options'),
    Output('data-analysis', 'children'),
    Output('features', 'options'),
    Output('features', 'disabled'),
    Input('upload-data', 'contents'),
    State('upload-data', 'filename')
)

def read_data(contents, filename):

    global df
    if contents is None:
        return dbc.Alert('No file uploaded yet!', style = {'color': 'red'}), True, {}, {}, {}, None, {}, True
    else:
        df = backend_logic.read_data(contents, filename)
        if df is None:
            return dbc.Label('There was an error when loading the data!', style = {'color': 'red'}), True, {}, {}, {}, None, {}, True
        else:
            options = [{'label': column, 'value': column} for column in df.columns]
            # color dropdown should only get the features that have unique values <= 6 unique values.
            options_color = [column for column in df.columns if len(df[column].value_counts()) <= 6]

            data_stats = tfdv.generate_statistics_from_dataframe(df)

            ht=tfdv.get_statistics_html(data_stats)

            numeric_features = [feature.path.step[0] for feature in data_stats.datasets[0].features if feature.HasField('num_stats')]

            return dbc.Label('{}'.format(filename), style = {'color': '#90EE90'}), False, options, options, options_color, \
            html.Iframe(srcDoc=ht, style = {'width':"100%", 'minHeight': '2500px', 'overflow': 'auto'}), numeric_features, False

# We are setting the enabling of the dropdown axis based on the chart type, because we will have some chart types
# with a number of dropdowns enabled and others not e.g. Pie plot does not have x and y axis 
# Pie plot will be added in the future
@app.callback(
    Output('x-axis', 'disabled'),
    Output('y-axis', 'disabled'),
    Output('color', 'disabled'),
    Input('chart type', 'value')
)

def dropdown(chart_type):
    
    if chart_type is None:
        return True, True, True
    else:
        return False, False,False

    
@app.callback(
    Output('container', 'children'),
    Input('chart type', 'value'),
    Input('x-axis', 'value'),
    Input('y-axis', 'value'),
    Input('color', 'value'),
    prevent_initial_call = True
)

def generate_graph(chart_type, xaxis, yaxis, color):

    # These are the main fields to be checked if empty
    if chart_type is None or xaxis is None or (yaxis is None and chart_type[0] != 'B'):
        return None
    
    else:
        graph = backend_logic.generate_graph(chart_type, xaxis, yaxis, color, df)

    return graph

@app.callback(
    Output('eda', 'children'),
    Input('features', 'value'),
    Input('eda-type', 'value'),
    prevent_initial_call = True
)
def eda_graph(features, eda_type):
    
    if eda_type == 'Correlation' and features is not None and len(features) >= 1:
        graph = backend_logic.correlation(df, features)
        return graph

    elif eda_type == 'Parallel coordinate' and features is not None and len(features) >= 1:
        graph = backend_logic.parallel_coordinate(df, features)
        return graph

    else:
        return None


# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)

