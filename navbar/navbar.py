"""
Creates the navigation bar
"""

import dash_bootstrap_components as dbc

from .logo import create_sidebar_logo
from .about_button import create_about_button


def create_navbar():
    """
    Returns the block corresponding to the navigation bar.
    """
    return dbc.Navbar(
        dbc.Container(
            [
                create_sidebar_logo(),
                dbc.NavbarToggler(id='navbar-toggler', n_clicks=0),
                create_about_button(),
            ]
        ),
        color='dark',
        dark=True,
        fixed='top'
    )
