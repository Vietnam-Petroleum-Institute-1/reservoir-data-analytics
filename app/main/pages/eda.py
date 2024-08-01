import dash
from dash import html, dcc
import numpy as np
import pandas as pd
from ydata_profiling import ProfileReport
import dash_bootstrap_components as dbc


df = pd.DataFrame(np.random.rand(100, 5), columns=["a", "b", "c", "d", "e"])
profile = ProfileReport(df, title="Profiling Report")

dash.register_page(__name__)


def comparison__body(profile__1, profile__2):
    return html.Div(
        dbc.Row(
            [
                dbc.Col(
                    html.Iframe(
                        id="eda",
                        srcDoc=profile__1.to_html(),
                        style={"height": "100vh", "width": "100%"},
                    )
                ),
                dbc.Col(
                    html.Iframe(
                        id="eda",
                        srcDoc=profile__2.to_html(),
                        style={"height": "100vh", "width": "100%"},
                    )
                ),
            ],
            align="start",
        ),
    )


layout = html.Div(
    [
        dbc.Row(
           [ html.H5("Comparison", className="font-size-1 text-center mb-3"),
             dcc.Dropdown(
                options=[number for number in range(2, 11)],
                value=5,
                id="type__data_comparison",
                className="d-flex pb-3 justify-content-center align-items-center w-25 m-auto",
            ),
            dcc.Dropdown(
                options=[number for number in range(2, 11)],
                value=5,
                id="type__col_comparison",
                className="d-flex justify-content-center align-items-center w-25 m-auto",
            )],
        class_name="d-flex justify-content-center align-items-center w-100 mt-3 mb-3",
        ),
        dbc.Row(id="report__data", children=comparison__body(profile, profile)),
    ]
)
