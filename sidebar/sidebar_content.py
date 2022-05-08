"""
Functions used to create sidebar components
"""

import datetime

from dash import dcc
from dash import html
import dash_bootstrap_components as dbc

from .styles import SIDEBAR_SUBTITLE
from .styles import SIDEBAR_TITLE



list_range_server = ['Null','0','1','[2 - 5]','[6 - 10]', '11+']
list_range_odt = ['0','[1 - 50]','[51 - 250]','[251 - 500]','[501 - 1000]','[1001 - 2000]','2001+']
list_range_build = ['1','[2 - 5]','[6 - 15]','[16 - 50]','[51 - 100]','101+']
list_ts_subcats = ['None', 'Lab', 'Level', 'Pipeline_status', 'Assessment',
    'Server_impact','SSR_Eligible', 'Range_of_Server_impact', 'Range_of_ODTs', 'Range_of_Build_impact']


def create_title() :
    """
    Creates the block corresponding to the title of the sidebar.
    """
    return html.Div([
        dbc.Row([
            dbc.Col(html.H2('Parameters', style=SIDEBAR_TITLE )),
            dbc.Col(create_reset_button())
            ])
        ])


def create_reset_button():
    """
    Creates the block corresponding to the reset button.
    """
    return html.Div([
        dbc.Button(children="Reset",id ='reset',  color="danger", className="me-1", n_clicks=0),
        ])



def create_color_blind_switch():
    """
    Creates the block corresponding to the color blind switch.
    """
    return html.Div(
        [dbc.Checklist(
            options=[
                {"label": 'Color-blind Mode', "value": True},
            ],
            value=False,
            id="color_blind",
            switch=True,
            ),
        ]
    )






def create_ts_subcat_accordion():
    """
    Creates the block corresponding to subcategories to display in the evolution of the pipelines graph.
    """
    return dbc.Accordion(
        [
            dbc.AccordionItem(
                dbc.RadioItems(
                    id = 'ts_subcat',
                    #value = 'None',
                    options=[{'label': x.replace('_', ' '), 'value': x} for x in list_ts_subcats],
                    value='None',
                    labelStyle={'display': 'inline-block'}
                    ),
                title="Subcategories for evolution graph",
                item_id="item-20",
            )
        ],
        start_collapsed=False)

def create_ts_period_accordion():
    """
    Creates the block corresponding to the time step in the evolution of the pipelines graph.
    """
    return dbc.Accordion(
        [
            dbc.AccordionItem(
                dbc.RadioItems(
                    id = 'ts_period',
                    #value = 'None',
                    options=[
                        {'label': 'Day', 'value': 'D'},
                        {'label': 'Month', 'value': 'M'},
                        {'label': 'Year', 'value': 'Y'}
                    ],
                    value='M',
                    labelStyle={'display': 'inline-block'}
                ),
                title="Period of evolution graph",
                item_id="item-21",
            )
        ],
        start_collapsed=True)


def create_chart_accordion():
    """
    Creates the block corresponding to the type of graphs (Pie or Bar).
    """
    return dbc.Accordion(
        [
            dbc.AccordionItem(
                dbc.RadioItems(
                    options=[
                        {'label': 'Pie', 'value': 'Pie'},
                        {'label': 'Bar', 'value': 'Bar'},
                    ],
                    value='Pie',
                    id= 'chart_radio',
                    inline= True
                ),
                title="Type of charts",
                item_id="item-22",
            )
        ],
        start_collapsed=True)


def create_osds_accordion():
    """
    Creates the block corresponding to the osds to show in
    the graphs for the range of ODTs and range of build impacts.
    """
    return dbc.Accordion(
        [
            dbc.AccordionItem(
                dbc.RadioItems(
                    options=[
                        {'label': 'Windows', 'value': 'Win'},
                        {'label': 'Linux', 'value': 'Linux'},
                    ],
                    value='Win',
                    id= 'osds_radio',
                    inline=True
                    ),
                title="OS",
                item_id="item-23",
            )
        ],
        start_collapsed=True)


def create_lab_accordion(df):
    """
    Creates the block corresponding to the lab.
    """
    return dbc.Accordion(
        [
            dbc.AccordionItem(
                dbc.Checklist(
                    id = 'lab',
                    #value = [],
                    options=[{'label': x, 'value': x} for x in df.Lab.unique()],
                    labelStyle={'display': 'inline-block'}
                    ),
                title="Lab",
                item_id="item-1",
            )
        ],
        start_collapsed=True)



def create_level_accordion(df):
    """
    Creates the block corresponding to the level.
    """
    return dbc.Accordion(
        [
            dbc.AccordionItem(
                dbc.Checklist(
                    id = 'level',
                    #value = 'None',
                    options=[{'label': x, 'value': x} for x in sorted(df.Level.unique())],
                    labelStyle={'display': 'inline-block'}
                    ),
                title="Level",
                item_id="item-2",
            )
        ],
        start_collapsed=True)

def create_pipeline_status_accordion(df):
    """
    Creates the block corresponding to the status of the pipelines.
    """
    return dbc.Accordion(
        [
            dbc.AccordionItem(
                dbc.Checklist(
                    id = 'pipeline_status',
                    #value = 'None',
                    options=[{'label': x, 'value': x} for x in df.Pipeline_status.unique()],
                    labelStyle={'display': 'inline-block'}
                    ),
                title="Pipeline Status",
                item_id="item-3",
            )
        ],
        start_collapsed=True)


def create_assessment_accordion(df):
    """
    Creates the block corresponding to the assessment.
    """
    return dbc.Accordion(
        [
            dbc.AccordionItem(
                dbc.Checklist(
                    id = 'assessment',
                    #value = 'None',
                    options=[{'label': x, 'value': x} for x in df.Assessment.unique()],
                    inline=False
                    ),
                title="Assessment",
                item_id="item-4",
            )
        ],
        start_collapsed=True)

def create_server_impact_accordion(df):
    """
    Creates the block corresponding to server impact.
    """
    return dbc.Accordion(
        [
            dbc.AccordionItem(
                dbc.Checklist(
                    id = 'server_impact',
                    #value = 'None',
                    options=[{'label': str(x), 'value': x} for x in df.Server_impact.unique()],
                    inline=False
                    ),
                title="Server Impact",
                item_id="item-7",
            )
        ],
        start_collapsed=True)



def create_range_odt_accordion():
    """
    Creates the block corresponding to the range of ODTs.
    """
    return dbc.Accordion(
        [
            dbc.AccordionItem(
                dbc.Checklist(
                    id = 'range_odt',
                    #value = 'None',
                    options=[{'label': x, 'value': x} for x in list_range_odt],
                    inline=False
                    ),
                title="Range of ODTs",
                item_id="item-5",
            )
        ],
        start_collapsed=True)


def create_range_server_accordion():
    """
    Creates the block corresponding to the range of server impact.
    """
    return dbc.Accordion(
        [
            dbc.AccordionItem(
                dbc.Checklist(
                    id = 'range_server',
                    #value = 'None',
                    options=[{'label': x, 'value': x} for x in list_range_server],
                    inline=False
                    ),
                title="Range of Server Impacts",
                item_id="item-10",
            )
        ],
        start_collapsed=True)


def create_range_build_accordion():
    """
    Creates the block corresponding to the range of build impacts.
    """
    return dbc.Accordion(
        [
            dbc.AccordionItem(
                dbc.Checklist(
                    id = 'range_build',
                    #value = 'None',
                    options=[{'label': x, 'value': x} for x in list_range_build],
                    inline=False
                    ),
                title="Range of Build Impacts",
                item_id="item-11",
            )
        ],
        start_collapsed=True)



def create_date_range(df):
    """
    Creates the block corresponding to the date range.
    """
    return html.Div(
        [
            html.P("Date Range ", style=SIDEBAR_SUBTITLE),
            dcc.DatePickerRange(
                id='date',
                max_date_allowed =datetime.datetime.now().date(),
                start_date= df.Date.min().date(),
                end_date= df.Date.max().date(),
                display_format='MMM Do, YY',
                start_date_placeholder_text='MMM Do, YY',
                initial_visible_month= df.Date.max().date(),
                persistence_type = 'memory')
        ])

def create_ssr_eligible_accordion(df):
    """
    Creates the block corresponding to the lab.
    """
    return dbc.Accordion(
        [
            dbc.AccordionItem(
                dbc.Checklist(
                    id = 'ssr',
                    #value = [],
                    options=[{'label': x, 'value': x} for x in sorted(list(set(df.SSR_Eligible.unique())-set(['Null'])))],
                    labelStyle={'display': 'inline-block'}
                    ),
                title="SSR Eligibility",
                item_id="item-12",
            )
        ],
        start_collapsed=True)
