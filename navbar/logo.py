"""
Defines the function to create the DS logo in the top left corner of
the navigation bar.
"""
import dash_bootstrap_components as dbc
from dash import html


PLOTLY_ICON = ('https://images.plot.ly/logo/new-branding/plotly-logomark.png')

def create_sidebar_logo():
    """
    Create the DS logo in the top left corner of the navigation bar.
    """
    return html.A(
        # Use row and col to control vertical alignment of logo / brand
        dbc.Row(
            [
                dbc.Col(html.Img(src=PLOTLY_ICON, height="30px")),
                dbc.Col(dbc.NavbarBrand("ENOViz", className="ms-2")),
            ],
            align="center",
            className="g-0",
        ),
        style={"textDecoration": "none"},
    )
