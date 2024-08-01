import dash
from dash import html, dcc

import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from component.processing import data__processing
from component.select_model import select__model
from model import Model, SkillScale, SkillOutlier, RemoveMissing
from component.type_data import full__data__ex, case__1__ex, case__2__ex, full__data__core, case__1__core, case__2__core

dash.register_page(__name__, path='/')

layout = html.Div(children=[
        dbc.Row(
        [
            dbc.Col(
                data__processing(SkillScale(), SkillOutlier(), RemoveMissing()),
                ),
            dbc.Col(
                select__model(Model()),
                ),
        ]
    ),
    dbc.Row(
        html.H4("Result EX", 
                className="text-center font-weight-bold text-primary p-3 text-white",
                style={"background-color": "steelblue"}
        ),
    ),
    full__data__ex,
    case__1__ex,
    case__2__ex,
    dbc.Row(
        html.H4("Result CORE", 
                className="text-center font-weight-bold text-primary p-3 text-white",
                style={"background-color": "steelblue"}
        ),
    ),
    full__data__core,
    case__1__core,
    case__2__core,

])