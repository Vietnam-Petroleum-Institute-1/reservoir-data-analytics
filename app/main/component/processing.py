import dash_bootstrap_components as dbc
from dash import dcc, html

def skill__outlier(model):
    return dbc.Row(
    [
        dbc.Label("Outlier", html_for="skill-outlier", width=2),
        dbc.Col(
            dcc.Dropdown(
                options=[option for option in model],
                value=None,
                id="skill-outlier",
            ),
            width=10,
        ),
    ],
    className="mb-3",
)

def skill__scaling(model):
    return dbc.Row(
        [
        dbc.Label("Scale", html_for="skill-scale", width=2),
        dbc.Col(
            dcc.Dropdown(
                options=[option for option in model],
                value=None,
                id="skill-scale",
            ),
            width=10,
        ),
    ],
    className="mb-3",
)

orther = dbc.Row(
    [
        dbc.Label("Other", html_for="missing-value", width=2),
        dbc.Col(
            dcc.Dropdown(
                options=["Pca", "Poly"],
                value=[],
                multi=True,
                id="orther-processing",
            ),
            width=10,
        ),
    ],
    className="mb-3",
)

def remove__missing(model):
    return dbc.Row(
    [
        dbc.Label("Remove Missing Value", html_for="missing-value", width=2),
        dbc.Col(
            dcc.Dropdown(
                options=[option for option in model],
                value=None,
                id="missing-value",
            ),
            width=10,
        ),
    ],
    className="mb-3",
)

box__upload_file = html.Div(
    id="box-upload-file",
    style={
            "height": "60px",
            "lineHeight": "60px",
            "borderWidth": "1px",
            "borderStyle": "dashed",
            "borderRadius": "5px",
            "textAlign": "center",
            "margin": "10px",
            "overflow": "scroll",
            "overflow-x": "hidden",
        },
)

def data__processing(Scalermodel, Outliermodel, RemoveMissingmodel):
    return html.Div(
    children=[
        html.H4(
            "Data Processing",
            className="text-center font-weight-bold text-primary p-2",
        ),
        dcc.Upload(
            id="upload-data",
            children=html.Div(
                [
                    "Drag and Drop or ",
                    html.A("Select Files"),
                ]
            ),
            style={
                "height": "60px",
                "lineHeight": "60px",
                "borderWidth": "1px",
                "borderStyle": "dashed",
                "borderRadius": "5px",
                "textAlign": "center",
                "margin": "10px",
            },
            multiple=True,
        ),
        box__upload_file,
        html.P("Select Data Type: "),
        skill__outlier(Outliermodel),
        skill__scaling(Scalermodel),
        remove__missing(RemoveMissingmodel),
        orther,
        html.Div(
            dcc.Checklist(
                options=[{'label': 'Standerize Column back to original value', 'value': 'Standerize_column'}],
                value=['Standerize_column'],
                id="standerize-column",
            ),
        ),
    ],
    className="bg-light shadow-sm h-auto mt-3 mb-3 h-100 pt-3 pb-3",
    style={"min-height": "550px"},
)
