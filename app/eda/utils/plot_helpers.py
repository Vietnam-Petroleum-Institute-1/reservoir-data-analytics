from typing import List
from typing import Literal, Union

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def fig(data_path, well ,group , ivcols: List[str], data_type: Literal["FULL", "CASE1", "CASE2"]):
    fig = make_subplots(rows=3, cols=1, subplot_titles=ivcols)
    for i, iv_col in enumerate(ivcols):
        df = pd.read_pickle(f"{data_path}{iv_col.lower()}.pkl")
        df = df[df["well"] == int(well)]
        if (data_type != "FULL") & (group is not None):
            df = df[(df["group"] == int(group))]
        df_tmp = df[["depth", f"{iv_col.lower()}", f"{iv_col.lower()}_predict"]].dropna().reset_index(drop=True)

        fig.add_trace(
            go.Scatter(
                x=df_tmp.depth,
                y=df_tmp[f"{iv_col.lower()}"],
                mode="lines+markers",
                name=f"Acutal {iv_col}",
            ),
            row=i + 1,
            col=1,
        )
        fig.add_trace(
            go.Scatter(
                x=df_tmp.depth,
                y=df_tmp[f"{iv_col.lower()}_predict"],
                mode="lines+markers",
                name=f"Predicted {iv_col}",
            ),
            row=i + 1,
            col=1,
        )
    fig.update_layout(  # customize font and legend orientation & position
        font=dict(
            family="Courier New, monospace",
            size=13,
            color="#7f7f7f",
        ),
    )
    return fig