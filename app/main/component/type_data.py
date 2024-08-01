import dash_bootstrap_components as dbc
from component.result import get__result
from dash import Dash, dash_table, dcc, html


def type_data(name_type: str, col1: Dash, col2: Dash, col3: Dash) -> Dash:
    return html.Div(
        [
            html.H4(
                name_type.upper(),
                className="text-center font-weight-bold text-primary p-3 text-white",
                style={"background-color": "steelblue"},
            ),
            dbc.Row(
                class_name="container text-center",
                children=[
                    dbc.Col(col1),
                    dbc.Col(col2),
                    dbc.Col(col3),
                ],
            ),
        ],
        className="container mt-4 mb-4 pt-3 pb-3     shadow-sm",
    )


full__data__ex = type_data("full", get__result("full__vwcl"), get__result("full__phie"), get__result("full__sw"))
case__1__ex = type_data("case 1", get__result("case1__vwcl"), get__result("case1__phie"), get__result("case1__sw"))
case__2__ex = type_data("case 2", get__result("case2__vwcl"), get__result("case2__phie"), get__result("case2__sw"))

full__data__core = type_data("full", get__result("full__vcl_core"), get__result("full__phi_core"), get__result("full__perm_core"))
case__1__core = type_data("case 1", get__result("case1__vcl_core"), get__result("case1__phi_core"), get__result("case1__perm_core"))
case__2__core = type_data("case 2", get__result("case2__vcl_core"), get__result("case2__phi_core"), get__result("case2__perm_core"))
