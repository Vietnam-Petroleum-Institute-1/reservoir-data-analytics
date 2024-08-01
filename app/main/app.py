from dataclasses import dataclass, field

import dash
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
import pandas as pd
from controller import callbacks
from dash import Dash, dcc, html
from model import Model


@dataclass
class DashApp:
    df: pd.DataFrame = field(default_factory=lambda: None)
    app: Dash = field(
        default_factory=lambda: Dash(
            __name__,
            external_stylesheets=[dmc.theme.DEFAULT_COLORS, dbc.themes.BOOTSTRAP],
            use_pages=True,
        )
    )
    MODEL: list = field(default_factory=lambda: Model())

    def body(self):
        self.app.layout = html.Div(
            [
                dbc.Row(
                    dbc.Col(
                        html.Div(
                            className="navbar navbar-expand-lg navbar-light bg-light shadow-sm justify-content-between",
                            children=[
                                html.Img(
                                    src="/assets/VPI_logo.png",
                                    className="logo mr-3 ml-3",
                                ),
                                html.Div(
                                    children=[
                                        dcc.Link(
                                            f'{page["name"]}',
                                            href=page["relative_path"],
                                            className="m-3 font-weight-bold text-primary text-decoration-none",
                                        )
                                        for page in dash.page_registry.values()
                                    ],
                                    className="mr-3 font-weight-bold text-primary",
                                ),
                            ],
                        )
                    )
                ),
                dash.page_container,
            ],
            className="w-100",
        )
        return self.app

    def controller(self):
        callbacks(self.app)
        return self.app

    def __post_init__(self):
        self.body()
        self.controller()
        self.app.run_server(port=8050, debug=True)


if __name__ == "__main__":
    DashApp()
