"""
Dash app Layout and callbacks
"""
import datetime
import os

import pandas as pd
import dash
import flask
from dash import Input, Output, State, html
import dash_bootstrap_components as dbc

from functions.functions import update_df,display_interactive_chart
from navbar.navbar import create_navbar
from sidebar.sidebar import create_sidebar
from dashboard.graphs import create_graphs




database= update_df(csv_path=os.path.join('Data','data.csv'))



# Dash app
flask_app = flask.Flask(__name__)
app = dash.Dash(__name__, server= flask_app,  external_stylesheets=[dbc.themes.LITERA])

# For dev server:
#app = dash.Dash(__name__,  external_stylesheets=[dbc.themes.LITERA])

app.layout = html.Div([
    create_navbar(),
    dbc.Row([
        dbc.Col(create_sidebar(database), width='auto'),
        dbc.Col(create_graphs(),width=True)]
    )])


@app.callback(
    [
    Output('lab', 'options'),
    Output('level', 'options'),
    Output('assessment', 'options'),
    Output('pipeline_status', 'options'),
    Output('date', 'max_date_allowed'),
    Output('date', 'initial_visible_month'),
    ],
    [Input('ts_period', 'value'),
    Input('ts_subcat', 'value'),
    Input('chart_radio', 'value'),
    Input('osds_radio', 'value'),
    Input('date', 'start_date'),
    Input('date', 'end_date'),
    Input('lab', 'value'),
    Input('level', 'value'),
    Input('pipeline_status', 'value'),
    Input('assessment', 'value'),
    Input('server_impact', 'value'),
    Input('range_server', 'value'),
    Input('range_odt', 'value'),
    Input('range_build', 'value'),
    Input('reset', 'n_clicks'),
    Input('ssr', 'value'),
    ])
# pylint: disable=unused-argument
# pylint: disable=invalid-name
def update_df_and_sidebar(ts_period, ts_subcat, chart_type, osds,start_date, end_date,
    Lab, Level, Pipeline_status, Assessment, Server_impact, range_server, range_odt, range_build,
    n_clicks, ssr):
    """
    Update the global database df and the sidebar (in case there are new values in the dataframe,
    like a new lab)
    """
    global database # pylint: disable=global-statement
    database = update_df(csv_path=os.path.join('Data','data.csv'))
    return [
        [{'label': x, 'value': x} for x in database.Lab.unique()],
        [{'label': x, 'value': x} for x in sorted(database.Level.unique())], # pylint: disable=E1101
        [{'label': x, 'value': x} for x in database.Assessment.unique()], # pylint: disable=E1101
        [{'label': x, 'value': x} for x in database.Pipeline_status.unique()], # pylint: disable=E1101
        datetime.datetime.now().date(),
        datetime.datetime.now().date(),
    ]





@app.callback(
    [Output('ts_subcat', 'value'),
    Output('ts_period', 'value'),
    Output('chart_radio', 'value'),
    Output('osds_radio', 'value'),
    Output('date', 'start_date'),
    Output('date', 'end_date'),
    Output('lab', 'value'),
    Output('level', 'value'),
    Output('pipeline_status', 'value'),
    Output('assessment', 'value'),
    Output('server_impact', 'value'),
    Output('range_server', 'value'),
    Output('range_odt', 'value'),
    Output('range_build', 'value'),
    Output('ssr', 'value'),
    Output('reset', 'n_clicks'),
    ],
    Input('reset', 'n_clicks')
)
# pylint: disable=unused-argument
def reset_inputs(n_clicks) :
    """
    Resets the values of inputs
    """
    list_ = ['None','M','Pie', 'Win', database.Date.min().date(), database.Date.max().date(),
        [], [], [], [], [], [], [], [], [], 0]

    return list_




@app.callback(
    Output('modal', 'is_open'),
    [Input('open', 'n_clicks'), Input('close', 'n_clicks')],
    [State('modal', 'is_open')],
)
def toggle_modal(open_, close, is_open):
    """
    Open and close the modal of 'About ENOViz' button
    """
    if open_ or close:
        return not is_open
    return is_open


@app.callback(
    [Output('pie-chart1', 'figure'),
    Output('pie-chart2', 'figure'),
    Output('pie-chart3', 'figure'),
    Output('pie-chart4', 'figure'),
    Output('pie-chart5', 'figure'),
    Output('pie-chart6', 'figure'),
    Output('pie-chart7', 'figure'),
    Output('pie-chart8', 'figure'),
    Output('pie-chart9', 'figure'),
    Output('ts_graph', 'figure'),
    Output('total', 'children'),
    ],
    [Input('color_blind', 'value'),
    Input('ts_period', 'value'),
    Input('ts_subcat', 'value'),
    Input('chart_radio', 'value'),
    Input('osds_radio', 'value'),
    Input('date', 'start_date'),
    Input('date', 'end_date'),
    Input('lab', 'value'),
    Input('level', 'value'),
    Input('pipeline_status', 'value'),
    Input('assessment', 'value'),
    Input('server_impact', 'value'),
    Input('range_server', 'value'),
    Input('range_odt', 'value'),
    Input('range_build', 'value'),
    Input('ssr', 'value'),
    ]
)
# pylint: disable=unused-argument
# pylint: disable=invalid-name
def generate_chart(color_blind, ts_period, ts_subcat, chart_type, osds,start_date, end_date,
    Lab, Level, Pipeline_status, Assessment, Server_impact, range_server, range_odt, range_build,
    SSR_Eligible):
    """
    Creates filter dictionary depending on inputs and returns the figures in a list.
    """

    # Create a filter as a dictionary with input values
    filter_dict = {}
    for key in ['osds', 'Lab', 'Level', 'Pipeline_status',
        'Assessment', 'Server_impact', 'SSR_Eligible'] :

        filter_dict[key] = eval(key) #pylint: disable= eval-used
    start_date = list(map(int,start_date.split('-')))
    end_date = list(map(int,end_date.split('-')))
    filter_dict['Date'] = [datetime.datetime(start_date[0],start_date[1],start_date[2],0,0,0),
                    datetime.datetime(end_date[0],end_date[1],end_date[2],23,59,59)]
    filter_dict['Range_of_Server_impact'] = range_server
    filter_dict['Range_of_ODTs'] = range_odt
    filter_dict['Range_of_Build_impact'] = range_build

    # Return all graphs + Total Pipelines number
    return display_interactive_chart(database, filter_dict = filter_dict,
        chart_type=chart_type, ts_period = ts_period, ts_subcat= ts_subcat, color_blind=color_blind)





# Run server
if __name__ == '__main__':
    # If dev server, comment the following line:
    flask_app.run(host = '0.0.0.0:8050', debug=True)

    # For dev server:
    #app.run_server(debug=True)
