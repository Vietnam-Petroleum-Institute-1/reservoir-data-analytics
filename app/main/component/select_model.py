from dash import dcc, html
import dash_bootstrap_components as dbc

def model(model):
    return dbc.Row(
        [
        dbc.Label("Choose Model", html_for="skill-scale", width=2),
        dbc.Col(
            dcc.Dropdown(
                options=[option for option in model],
                value=[],
                id="model",
                multi=True,
            ),
            width=10,
            className="mb-3",
        ),
    ],
    className="mb-3",
)

k__fold = dbc.Row(
    [
        dbc.Label("K-Fold", html_for="k-fold", width=2),
        dbc.Col(
            dcc.Dropdown(
                options=[
                    number for number in range(2, 11)
                ],
                value=5,
                id="k-fold",
            ),
            width=10,
        ),
    ],
    className="mb-3",
)

type__model = dbc.Row(
    [
        dbc.Label("Type Model", html_for="type-model", width=2),
        dbc.Col(
            dcc.RadioItems(
                options=["auto", "apply"],
                value="apply",
                id="type-model",
                className="d-flex justify-content-space-between align-items-center",
                style={"margin": "0 auto", "width": "50%", "justify-content": "space-around"},
            ),
            width=10,
            className="d-flex justify-content-space-between align-items-center",
        ),
    ],
    className="mb-3",
)

tunning__model = dbc.Row(
    [
        dbc.Label("Tunning Model", html_for="tunning-model", width=2),
        dbc.Col(
            dcc.Textarea(
                id="tunning-model",
                value = "Write your tunning model here... \nAfter choose 1 best model, you can tunning it here",
                style={"height": "100px", "width": "100%", "border": "1px solid #ced4da", "border-radius": ".25rem"},
                ),
            width=10,
        ),
    ],
    className="mb-3",
)
    
shuffling = dbc.Row(
    [
        dbc.Label("shuffle", html_for="type-shuffle", width=2),
        dbc.Col(
            dcc.RadioItems(
                options=["True", "False"],
                value="True",
                id="type-shuffle",
                className="d-flex justify-content-space-between align-items-center",
                style={"margin": "0 auto", "width": "50%", "justify-content": "space-around"},
            ),
            width=10,
            className="d-flex justify-content-space-between align-items-center",
        ),
    ],
    className="mb-3",
)

def select__model(Model):
    return html.Div(
                children=[
                    html.H4(
                            "Model Selection",
                            className="text-center font-weight-bold text-primary p-2",
                        ),
                    dbc.Stack(
                        [model(Model),
                        k__fold,
                        tunning__model,
                        type__model,
                        shuffling,
                        dbc.Button("Train Model", color="primary", className="mt-3", id="train-model", outline=True, n_clicks=0),
                         ],
                        id="model-selection",
                        className="p-2 mt10",
                    ),
                    ],
                className="bg-light shadow-sm h-auto mt-3 mb-3 h-100 pt-3 pb-3",
                style={"min-height": "550px"},
                ),