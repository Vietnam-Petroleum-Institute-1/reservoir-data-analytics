from dash import dcc, html
from typing import Literal, Union
from .data_processing import get_name_group
import pandas as pd
import os

def get_filter(data_path: str, data_type: Literal["FULL", "CASE1", "CASE2"]):
    well_list = []
    for file in os.listdir(data_path):
        data = pd.read_pickle(f"{data_path}{file}")
        well_list += data["well"].unique().tolist()
    well_list = [*set(well_list)]
    well_list.sort()

    if data_type != 'FULL':
        group_list = []
        for file in os.listdir(data_path):
            data = pd.read_pickle(f"{data_path}{file}")
            group_list += data["group"].unique().tolist()
        group_list = [*set(group_list)]
        group_list.sort()
        
    if data_type == "FULL":
        return (
            html.Div(
                [
                    html.Div(
                        [
                            html.P("Group: ", className="label"),
                            dcc.Dropdown(
                                value=None,
                                id="group",
                                className="dropdown",
                            ),
                        ],
                        style={"display": "none"},
                    ),
                    html.Div(
                        [
                            html.P("Well: ", className="label"),
                            dcc.Dropdown(
                                options=[
                                    {"label": i, "value": i}
                                    for i in well_list
                                ],
                                value=well_list[0],
                                id="well",
                                className="dropdown",
                            ),
                        ],
                    ),
                ]
            )
        )       
    else:
        return (
            html.Div(
                [
                    html.Div(
                        [
                            html.P("Group: ", className="label"),
                            dcc.Dropdown(
                                options=[
                                    {"label": i, "value": i}
                                    for i in group_list
                                ],
                                value=group_list[0],
                                id="group",
                                className="dropdown",
                            ),
                        ],
                    ),
                    html.Div(
                        [
                            html.P("Well: ", className="label"),
                            dcc.Dropdown(
                                options=[
                                    {"label": i, "value": i}
                                    for i in well_list
                                ],
                                value=well_list[0],
                                id="well",
                                className="dropdown",
                            ),
                        ],
                    ),
                ]
            )
        )
    
def update_well(
    data_type: Literal["FULL", "CASE1", "CASE2"],
    data_path,
    group,
):
    well_list = []
    for file in os.listdir(data_path):
        data = pd.read_pickle(f"{data_path}{file}")
        if (data_type != "FULL") & (group is not None):
            well_list += data[data["group"] == int(group)]["well"].unique().tolist()
        else:
            well_list += data["well"].unique().tolist()
            
    well_list = [*set(well_list)]
    well_list.sort()
    return [{"label": i, "value": i} for i in well_list]
