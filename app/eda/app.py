from dataclasses import dataclass, field
from typing import Literal

import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
import pandas as pd
from dash import Dash, Input, Output, callback, dcc, html
from utils.data_processing import get_data, loc_df, get_eda_data, avg_eda_value, eda_value
from utils.other_helpers import get_filter, update_well
from utils.plot_helpers import fig


@dataclass
class DashApp:
    df: pd.DataFrame = field(default_factory=lambda: None)
    app: Dash = field(
        default_factory=lambda: Dash(
            __name__,
            external_stylesheets=[dmc.theme.DEFAULT_COLORS, dbc.themes.BOOTSTRAP],
        )
    )
    IVCOLS: list = field(default_factory=lambda: ["VWCL", "PHIE", "SW"])
    data_types: list = field(default_factory=lambda: ["FULL", "CASE1", "CASE2"])
    data_type: Literal["FULL", "CASE1", "CASE2"] = field(default="FULL")

    def DashBody(self):
        self.app.layout = html.Div(
            [
                html.Div(
                    className="app-header",
                    children=[
                        html.Img(src="/assets/VPI_logo.png", className="logo"),
                        html.Div("EDA Dash App", className="app-header--title"),
                    ],
                ),
                html.Div(
                    children=[
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.H2("Filter By"),
                                        html.Div(
                                            [
                                                dmc.RadioGroup(
                                                    [
                                                        dmc.Radio(
                                                            i,
                                                            value=i,
                                                            className="group",
                                                        )
                                                        for i in self.data_types
                                                    ],
                                                    value=self.data_types[0],
                                                    id="data_type",
                                                    size="sm",
                                                ),
                                            ],
                                            className="group_choose",
                                        ),
                                        html.Div(
                                            id="type_choose",
                                        ),
                                    ],
                                    className="left__up",
                                ),
                                html.Div(
                                    [
                                        html.Div(
                                            [
                                                html.P("R2 Train", className="label"),
                                                html.Div(
                                                    [html.P(id="r2_train")],
                                                    className="box-pie",
                                                    id="hover-target-r2-train",
                                                ),
                                                dbc.Popover(
                                                    (
                                                        html.Div(
                                                            [
                                                                html.P("VWCL", className="label"),
                                                                html.P(id="vwcl-r2-train"),
                                                                
                                                            ],
                                                            id="hover-target-vwcl-r2-train",
                                                        ),
                                                        html.Div(
                                                            [
                                                                html.P("PHIE", className="label"),
                                                                html.P(id="phie-r2-train"),
                                                            ],
                                                            id="hover-target-phie-r2-train",
                                                        ),
                                                        html.Div(
                                                            [
                                                                html.P("SW", className="label"),
                                                                html.P(id="sw-r2-train"),
                                                            ],
                                                            id="hover-target-sw-r2-train",
                                                        ),
                                                    ),
                                                    target="hover-target-r2-train",
                                                    body=True,
                                                    trigger="hover",
                                                ),
                                            ]
                                        ),
                                        html.Div(
                                            [
                                                html.P("R2 Test", className="label"),
                                                html.Div(
                                                    [html.P(id="r2_test")],
                                                    className="box-pie",
                                                    id="hover-target-r2-test",
                                                ),
                                                dbc.Popover(
                                                    (
                                                        html.Div(
                                                            [
                                                                html.P("VWCL", className="label"),
                                                                html.P(id="vwcl-r2-test"),
                                                            ],
                                                            id="hover-target-vwcl-r2-test",
                                                        ),
                                                        html.Div(
                                                            [
                                                                html.P("PHIE", className="label"),
                                                                html.P(id="phie-r2-test"),
                                                            ],
                                                            id="hover-target-phie-r2-test",
                                                        ),
                                                        html.Div(
                                                            [
                                                                html.P("SW", className="label"),
                                                                html.P(id="sw-r2-test"),
                                                            ],
                                                            id="hover-target-sw-r2-test",
                                                        ),
                                                    ),
                                                    target="hover-target-r2-test",
                                                    body=True,
                                                    trigger="hover",
                                                ),
                                            ]
                                        ),
                                        html.Div(
                                            [
                                                html.P("MSE", className="label"),
                                                html.P(id="mse"),
                                            ],
                                            id="hover-target-mse",
                                        ),
                                        dbc.Popover(
                                            (
                                                html.Div(
                                                    [
                                                        html.P("VWCL", className="label"),
                                                        html.P(id="vwcl-mse"),
                                                    ],
                                                    id="hover-target-vwcl-mse",
                                                ),
                                                html.Div(
                                                    [
                                                        html.P("PHIE", className="label"),
                                                        html.P(id="phie-mse"),
                                                    ],
                                                    id="hover-target-phie-mse",
                                                ),
                                                html.Div(
                                                    [
                                                        html.P("SW", className="label"),
                                                        html.P(id="sw-mse"),
                                                    ],
                                                    id="hover-target-sw-mse",
                                                ),
                                            ),
                                            target="hover-target-mse",
                                            body=True,
                                            trigger="hover",
                                        ),
                                        html.Div(
                                            [
                                                html.P("MAE", className="label"),
                                                html.P(id="mae"),
                                            ],
                                            id="hover-target-mae",
                                        ),
                                        dbc.Popover(
                                            (
                                                html.Div(
                                                    [
                                                        html.P("VWCL", className="label"),
                                                        html.P(id="vwcl-mae"),
                                                    ],
                                                    id="hover-target-vwcl-mae",
                                                ),
                                                html.Div(
                                                    [
                                                        html.P("PHIE", className="label"),
                                                        html.P(id="phie-mae"),
                                                    ],
                                                    id="hover-target-phie-mae",
                                                ),
                                                html.Div(
                                                    [
                                                        html.P("SW", className="label"),
                                                        html.P(id="sw-mae"),
                                                    ],
                                                    id="hover-target-sw-mae",
                                                ),
                                            ),
                                            target="hover-target-mae",
                                            body=True,
                                            trigger="hover",
                                        ),
                                        html.Div(
                                            [
                                                html.P("RMSE", className="label"),
                                                html.P(id="rmse"),
                                            ],
                                            id="hover-target-rmse",
                                        ),
                                        dbc.Popover(
                                            (
                                                html.Div(
                                                    [
                                                        html.P("VWCL", className="label"),
                                                        html.P(id="vwcl-rmse"),
                                                    ],
                                                    id="hover-target-vwcl-rmse",
                                                ),
                                                html.Div(
                                                    [
                                                        html.P("PHIE", className="label"),
                                                        html.P(id="phie-rmse"),
                                                    ],
                                                    id="hover-target-phie-rmse",
                                                ),
                                                html.Div(
                                                    [
                                                        html.P("SW", className="label"),
                                                        html.P(id="sw-rmse"),
                                                    ],
                                                    id="hover-target-sw-rmse",
                                                ),
                                            ),
                                            target="hover-target-rmse",
                                            body=True,
                                            trigger="hover",
                                        ),
                                        html.Div(
                                            [
                                                html.P("SMAPE", className="label"),
                                                html.P(id="smape"),
                                            ],
                                            id="hover-target-smape",
                                        ),
                                        dbc.Popover(
                                            (
                                                html.Div(
                                                    [
                                                        html.P("VWCL", className="label"),
                                                        html.P(id="vwcl-smape"),
                                                    ],
                                                    id="hover-target-vwcl-smape",
                                                ),
                                                html.Div(
                                                    [
                                                        html.P("PHIE", className="label"),
                                                        html.P(id="phie-smape"),
                                                    ],
                                                    id="hover-target-phie-smape",
                                                ),
                                                html.Div(
                                                    [
                                                        html.P("SW", className="label"),
                                                        html.P(id="sw-smape"),
                                                    ],
                                                    id="hover-target-sw-smape",
                                                ),
                                            ),
                                            target="hover-target-smape",
                                            body=True,
                                            trigger="hover",
                                        ),
                                        # html.Div(
                                        #     [
                                        #         html.P("MAP", className="label"),
                                        #         html.P(id="map"),
                                        #     ],
                                        #     id="hover-target-map",
                                        # ),
                                        # dbc.Popover(
                                        #     "r2 test",
                                        #     target="hover-target-map",
                                        #     body=True,
                                        #     trigger="hover",
                                        # ),
                                        html.Div(
                                            [
                                                html.P("EVS", className="label"),
                                                html.P(id="evs"),
                                            ],
                                            id="hover-target-evs",
                                        ),
                                        dbc.Popover(
                                            (
                                                html.Div(
                                                    [
                                                        html.P("VWCL", className="label"),
                                                        html.P(id="vwcl-evs"),
                                                    ],
                                                    id="hover-target-vwcl-evs",
                                                ),
                                                html.Div(
                                                    [
                                                        html.P("PHIE", className="label"),
                                                        html.P(id="phie-evs"),
                                                    ],
                                                    id="hover-target-phie-evs",
                                                ),
                                                html.Div(
                                                    [
                                                        html.P("SW", className="label"),
                                                        html.P(id="sw-evs"),
                                                    ],
                                                    id="hover-target-sw-evs",
                                                ),
                                            ),
                                            target="hover-target-evs",
                                            body=True,
                                            trigger="hover",
                                        ),
                                    ],
                                    className="left__down",
                                ),
                            ],
                            className="Left",
                        ),
                        html.Div(
                            [
                                dcc.Graph(id="scatter-plot"),
                                dcc.Slider(
                                    id="slider-circular",
                                    min=0,
                                    max=20,
                                    marks={i: str(i) for i in range(21)},
                                    value=3,
                                    className="slide__depth",
                                ),
                            ],
                            className="Right",
                        ),
                    ],
                    className="box_chart",
                ),
            ]
        )
        @self.app.callback(
            Output(component_id="type_choose", component_property="children"),
            Input(component_id="data_type", component_property="value"),
        )
        def update_type(data_type):
            data_path = get_eda_data(data_type)
            self.data_type = data_type
            return get_filter(data_path=data_path, data_type=data_type)

        @self.app.callback(
            [
                Output(component_id="well", component_property="options"),
                Output(component_id="scatter-plot", component_property="figure"),
            ],
            [
                Input(component_id="data_type", component_property="value"),
                Input(component_id="group", component_property="value"),
                Input(component_id="well", component_property="value"),
            ],
            prevent_initial_call=True
        )
        def update_well_options(data_type, group, well):
            data_path = get_eda_data(data_type)
            wells = update_well(data_path=data_path, data_type=data_type, group=group)
            figure = fig(data_path=data_path, well=well, group=group, ivcols=self.IVCOLS, data_type=data_type)
            return wells, figure
        
        @self.app.callback(
            [
                Output(component_id="hover-target-r2-train", component_property="children"),
                Output(component_id="hover-target-r2-test", component_property="children"),
                Output(component_id="mse", component_property="children"),
                Output(component_id="rmse", component_property="children"),
                Output(component_id="mae", component_property="children"),
                Output(component_id="smape", component_property="children"),
                Output(component_id="evs", component_property="children"),
            ],
            [
                Input(component_id="data_type", component_property="value"),
                Input(component_id="group", component_property="value"),
                Input(component_id="well", component_property="value"),
            ],
            prevent_initial_call=True
        )
        def eda_value_outputs(data_type, group, well):
            data_path = get_eda_data(data_type)
            r2_train, r2_test, mse, rmse, mae, smape, evs = avg_eda_value(data_path=data_path, group=group, well=well, data_type=data_type)
            return round(r2_train, 2), round(r2_test, 2), round(mse, 2), round(rmse, 2), round(mae, 2), round(smape, 2), round(evs, 2)

        # VWCL callback
        @self.app.callback(
            [
                Output(component_id="hover-target-vwcl-r2-train", component_property="children"),
                Output(component_id="hover-target-vwcl-r2-test", component_property="children"),
                Output(component_id="hover-target-vwcl-mse", component_property="children"),
                Output(component_id="hover-target-vwcl-mae", component_property="children"),
                Output(component_id="hover-target-vwcl-rmse", component_property="children"),
                Output(component_id="hover-target-vwcl-smape", component_property="children"),
                Output(component_id="hover-target-vwcl-evs", component_property="children"),
            ],
            [
                Input(component_id="data_type", component_property="value"),
                Input(component_id="group", component_property="value"),
                Input(component_id="well", component_property="value"),
            ],
            prevent_initial_call=True
        )
        def eda_vwcl_value_output(data_type, group, well):
            data_path = get_eda_data(data_type)
            col = "vwcl"
            r2_train, r2_test, mse, rmse, mae, smape, evs = eda_value(data_path=data_path, col=col, group=group, well=well, data_type=data_type)
            return f"VWCL: {round(r2_train, 2)}", f"VWCL: {round(r2_test, 2)}", f"VWCL: {round(mse, 2)}", f"VWCL: {round(rmse, 2)}", f"VWCL: {round(mae, 2)}", f"VWCL: {round(smape, 2)}", f"VWCL: {round(evs, 2)}"

        # PHIE callback
        @self.app.callback(
            [
                Output(component_id="hover-target-phie-r2-train", component_property="children"),
                Output(component_id="hover-target-phie-r2-test", component_property="children"),
                Output(component_id="hover-target-phie-mse", component_property="children"),
                Output(component_id="hover-target-phie-mae", component_property="children"),
                Output(component_id="hover-target-phie-rmse", component_property="children"),
                Output(component_id="hover-target-phie-smape", component_property="children"),
                Output(component_id="hover-target-phie-evs", component_property="children"),
            ],
            [
                Input(component_id="data_type", component_property="value"),
                Input(component_id="group", component_property="value"),
                Input(component_id="well", component_property="value"),
            ],
            prevent_initial_call=True
        )
        def eda_vwcl_value_output(data_type, group, well):
            data_path = get_eda_data(data_type)
            col = "phie"
            r2_train, r2_test, mse, rmse, mae, smape, evs = eda_value(data_path=data_path, col=col, group=group, well=well, data_type=data_type)
            return f"PHIE: {round(r2_train, 2)}", f"PHIE: {round(r2_test, 2)}", f"PHIE: {round(mse, 2)}", f"PHIE: {round(rmse, 2)}", f"PHIE: {round(mae, 2)}", f"PHIE: {round(smape, 2)}", f"PHIE: {round(evs, 2)}"

        # SW callback
        @self.app.callback(
            [
                Output(component_id="hover-target-sw-r2-train", component_property="children"),
                Output(component_id="hover-target-sw-r2-test", component_property="children"),
                Output(component_id="hover-target-sw-mse", component_property="children"),
                Output(component_id="hover-target-sw-mae", component_property="children"),
                Output(component_id="hover-target-sw-rmse", component_property="children"),
                Output(component_id="hover-target-sw-smape", component_property="children"),
                Output(component_id="hover-target-sw-evs", component_property="children"),
            ],
            [
                Input(component_id="data_type", component_property="value"),
                Input(component_id="group", component_property="value"),
                Input(component_id="well", component_property="value"),
            ],
            prevent_initial_call=True
        )
        def eda_vwcl_value_output(data_type, group, well):
            data_path = get_eda_data(data_type)
            col = "sw"
            r2_train, r2_test, mse, rmse, mae, smape, evs = eda_value(data_path=data_path, col=col, group=group, well=well, data_type=data_type)
            return f"SW: {round(r2_train, 2)}", f"SW: {round(r2_test, 2)}", f"SW: {round(mse, 2)}", f"SW: {round(rmse, 2)}", f"SW: {round(mae, 2)}", f"SW: {round(smape, 2)}", f"SW: {round(evs, 2)}"

        self.app.config.suppress_callback_exceptions = True
        
        return self.app

    def __post_init__(self):
        self.DashBody().run_server(port=8051, debug=True)


if __name__ == "__main__":
    DashApp()
