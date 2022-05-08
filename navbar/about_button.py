"""
"About ENOViz" button
"""

import dash_bootstrap_components as dbc



ABOUT_TEXT_1 = '''ENOViz aims to provide a graphic visualization of
 statistics concerning some Jenkins pipelines dataset. The dataset used here is randomly generated.'''
ABOUT_TEXT_2 = '''Ten graphs are presented. The first one demonstrates the variation
 of the number of Pipelines per a certain period
 of time defined in the Parameters sidebar (default = Month).
 Each of the next 9 graphs illustrates the propotions of groups of pipelines in the form of Pie charts (default)
 or Bar charts (Option in the Parameters). These groups are formed
 according to respectively the lab, the level, the status, the assessment,
 the server impact of the pipelines and the number of ODTs to replay and build impacts for both Windows
 and Linux.'''
ABOUT_TEXT_3 = 'All the graphs are updated depending on the filters presented in the Parameters'
ABOUT_TEXT_4 = '''In case you would like to save a graph as a .png image,
 you can simply click on the camera logo on the top right of each graph.'''



def create_about_button():
    """
    Creates the block corresponding to About ENOViz button
    """
    return dbc.Collapse(
        dbc.Row(
            [
            dbc.Col(
                [
                    dbc.Button("About ENOViz", id="open", n_clicks=0),
                    dbc.Modal(
                    [
                        dbc.ModalHeader(dbc.ModalTitle("About this tool")),
                        dbc.ModalBody(ABOUT_TEXT_1),
                        dbc.ModalBody(ABOUT_TEXT_2),
                        dbc.ModalBody(ABOUT_TEXT_3),
                        dbc.ModalBody(ABOUT_TEXT_4),
                        dbc.ModalFooter(
                            dbc.Button(
                                "Close", id="close", className="ms-auto", n_clicks=0
                            )
                        ),
                    ],
                    id="modal",
                    size='xl',
                    is_open=False,
                )],
                    width="auto",
            ),
            ],
            className="g-0 ms-auto flex-nowrap mt-3 mt-md-0",
            align="center",
        ),
        id="navbar-collapse",
        is_open=False,
        navbar=True,
    )
