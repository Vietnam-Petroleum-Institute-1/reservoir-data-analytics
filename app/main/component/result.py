from dash import dash_table, dcc, html


def result(id):
    return dash_table.DataTable(
        id=id,
        page_size=10,
        page_current=0,
        page_action="custom",
        sort_action="custom",
        sort_mode="multi",
        sort_by=[],
        style_table={"overflowX": "auto"},
        style_cell={
            "textAlign": "center",
            "minWidth": "100px",
            "width": "100px",
            "maxWidth": "100px",
            "whiteSpace": "normal",
        },
        style_header={"fontWeight": "bold"},
        style_data_conditional=[
            {"if": {"row_index": "odd"}, "backgroundColor": "rgb(248, 248, 248)"}
        ],
        style_cell_conditional=[{"if": {"column_id": "index"}, "width": "50px"}],
        style_as_list_view=True,
    )


def box__result(id: str):
    return html.Div(
        children=[
            html.H4(
                id.upper(),
                className="text-center font-weight-bold text-primary p-2",
            ),
            result(f"result-{id}"),
        ],
        className="bg-light shadow-sm h-auto mt-3 mb-3 h-100 pt-3 pb-3",
    )


def get__result(name: str):
    return box__result(name)
