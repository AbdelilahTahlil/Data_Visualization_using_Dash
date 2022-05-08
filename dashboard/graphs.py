"""
Graphs layout
"""
from dash import html
from dash import dcc
from .dashboard_styles import DASHBOARD_CONTENT, DASHBOARD_TEXT



ts_graph = [dcc.Graph(id="ts_graph",
        style={'display': 'inline-block','vertical-align': 'top','width': '99%'})]


# Create groups of 3 graphs at most
graph_group_1 = [
    dcc.Graph(
        id="pie-chart1",
        style={'display': 'inline-block','vertical-align': 'top','width': '33%'}),
    dcc.Graph(
        id="pie-chart2",
        style={'display': 'inline-block','vertical-align': 'top','width': '33%'}),
    dcc.Graph(
        id="pie-chart3",
        style={'display': 'inline-block','vertical-align': 'top','width': '33%'})
]

graph_group_2 = [
    dcc.Graph(
        id="pie-chart4",
        style={'display': 'inline-block','vertical-align': 'top','width': '33%'}),
    dcc.Graph(
        id="pie-chart5",
        style={'display': 'inline-block','vertical-align': 'top','width': '33%'}),
    dcc.Graph(
        id="pie-chart6",
        style={'display': 'inline-block','vertical-align': 'top','width': '33%'})
]

graph_group_3 = [
    dcc.Graph(
        id="pie-chart7",
        style={'display': 'inline-block','vertical-align': 'top','width': '33%'}),
    dcc.Graph(
        id="pie-chart8",
        style={'display': 'inline-block','vertical-align': 'top','width': '33%'}),
    dcc.Graph(
        id="pie-chart9",
        style={'display': 'inline-block','vertical-align': 'top','width': '33%'}),
]



# Dashboard layout
def create_graphs() :
    """
    Generates the block corresponding to graph display
    """
    return html.Div(
        [
            html.H2('Statistics on Jenkins Pipelines', style=DASHBOARD_TEXT),
            dcc.Markdown(id='total', style={'textAlign':'center', 'fontSize':20, 'font':'italic'}),
            html.Br(),
            html.Div(ts_graph),
            html.Div(graph_group_1),
            html.Div(graph_group_2),
            html.Div(graph_group_3),
        ],
        style=DASHBOARD_CONTENT
    )
