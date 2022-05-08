"""
Defines the the block html.Div of the sidebar
"""

from dash import html

from .sidebar_content import (create_lab_accordion, create_level_accordion,
    create_assessment_accordion,create_date_range, create_ts_subcat_accordion,
    create_osds_accordion, create_pipeline_status_accordion,
    create_range_build_accordion, create_range_odt_accordion,
    create_range_server_accordion, create_server_impact_accordion,
    create_title, create_chart_accordion, create_ts_period_accordion,
    create_ssr_eligible_accordion, create_color_blind_switch)
from .styles import SIDEBAR_CONTENT


def create_sidebar(df):
    """
    Return: html.Div, which is the block representing the sidebar in the app layout.

    Some elements of the sidebar (like Lab, Level,..) automatically detect the number of unique
    values in the database.
    Thus the need to put df in the arguments.

    df: DataFrame of pipelines.
    """
    return html.Div(
        [
            create_title(),
            html.Br(),
            create_color_blind_switch(),
            html.Br(),
            create_date_range(df),
            html.Br(),
            create_ts_subcat_accordion(),
            html.Br(),
            create_ts_period_accordion(),
            html.Br(),
            create_chart_accordion(),
            html.Br(),
            create_lab_accordion(df),
            html.Br(),
            create_level_accordion(df),
            html.Br(),
            create_pipeline_status_accordion(df),
            html.Br(),
            create_server_impact_accordion(df),
            html.Br(),
            create_assessment_accordion(df),
            html.Br(),
            create_ssr_eligible_accordion(df),
            html.Br(),
            create_osds_accordion(),
            html.Br(),
            create_range_server_accordion(),
            html.Br(),
            create_range_odt_accordion(),
            html.Br(),
            create_range_build_accordion(),
        ],
        style=SIDEBAR_CONTENT,
    )
