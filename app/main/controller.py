import base64
import io
import os
import sys
from typing import Any, Literal, Union

import pandas as pd
from dash import (Dash, Input, Output, State, callback, ctx, dash_table, dcc,
                  html)
from model import Model, RemoveMissing, SkillOutlier, SkillScale, OrtherSkills, ColsData
from settings import (NAME_FULLDF_APP, PATH_CODE, PATH_EXTERNAL_DATA,
                      PATH_INTERIM_APP)

path = os.path.join(PATH_CODE)
sys.path.append(path)
from src.data.make_dataset import transform_to_processed
from src.features.build_features import loc_colpercent, loc_df_dependent_col
from src.features.groups import GroupDepth, GroupDistance
from src.models.train_model_old import cross_validate_kfold
from src.read import read, read_h5
from src.save import save
from src.settings import NAMEFULLDF, PATH_PROCESSED_DATA

def clean_external_data(file_endwith: Literal[".h5", ".csv", ".xls", ".asc"]) -> None:
    for file in os.listdir(PATH_EXTERNAL_DATA):
        if any(x in file for x in file_endwith):
            os.remove(os.path.join(PATH_EXTERNAL_DATA, file))


def parse_contents(
    contents, filename, date, file_supported: list = ["csv", "asc", "h5", "xls"]
):
    content_type, content_string = contents.split(",")
    decoded = base64.b64decode(content_string)
    try:
        if any(x in filename for x in file_supported):
            df = read(io.StringIO(decoded.decode("utf-8")), filename.split(".")[-1])
            save(df, filename.split(".")[0], os.path.join(PATH_EXTERNAL_DATA), "h5")
    except Exception as e:
        print(e)
        return html.Div([f"file not supported {filename}"])

    return html.Div([f"File {filename} has been uploaded successfully."])


def check_feature(
    df: pd.DataFrame,
    value: Any,
    type: Literal["Outlier", "RemoveMissing", "Normalizer"],
    dependent_col: str = None,
):
    type__data = dict(
        Outlier=SkillOutlier(), Normalizer=loc_colpercent, RemoveMissing=RemoveMissing()
    )
    if value is not None and type != "Normalizer":
        if type == "RemoveMissing":
            missing_col = [2, 3, 4]
            for col in missing_col:
                if str(col) in value:
                    return type__data[type][value](df, int(col))
            return type__data[type][value](df, value)
        if value == "COOKS DISTANCE" and dependent_col is not None:
            return type__data[type][value](df, dependent_col)
        return type__data[type][value](df)
    if value is not None and type == "Normalizer":
        return type__data[type](df)
    return df


def get_full_data() -> pd.DataFrame:
    if os.path.exists(f"{PATH_PROCESSED_DATA}/{NAME_FULLDF_APP}.h5"):
        return read_h5(f"{PATH_PROCESSED_DATA}/{NAME_FULLDF_APP}.h5")
    if os.path.exists(f"{PATH_PROCESSED_DATA}/{NAMEFULLDF}.h5"):
        return read_h5(f"{PATH_PROCESSED_DATA}/{NAMEFULLDF}.h5")
    return ValueError("File not found")


def get_data_type(
    df: pd.DataFrame,
    type: Literal["full", "case1", "case2"],
    dependent_col: str,
    models: list,
    type_model: str,
    skill_scale: str,
    k_fold: int,
    shuffle: bool,
    pca: bool,
    poly: bool,
):
    if type == "case1":
        case1 = GroupDistance(df=df, DEPENDENT_COL=dependent_col.upper())
        result = list()
        for group in sorted(case1.df["GROUP_DISTANCE"].dropna().unique()):
            df_group = case1.get_group(group)
            if df_group.shape[0] >= 10:
                df_result = strat_train(
                    df=df_group.drop(["GROUP_DISTANCE", "WELLBORE"], axis=1),
                    model=[Model()[model] for model in models],
                    type_model=type_model,
                    dependent_col=dependent_col.upper(),
                    type_scale=SkillScale()[skill_scale],
                    k_fold=int(k_fold),
                    shuffle=bool(shuffle),
                    pca=bool(pca),
                    poly=bool(poly),
                )
                df_result = df_result.round(2).reset_index()
                df_result["GROUP"] = group
                result.append(df_result)
        return pd.concat(result)
    if type == "case2":
        case2 = GroupDepth(df=df, DEPENDENT_COL=dependent_col.upper())
        result = list()
        for group in sorted(case2.df["GROUP_DEPTH"].dropna().unique()):
            df_group = case2.get_group(group)
            if df_group.shape[0] >= 10:
                df_result = strat_train(
                    df=df_group.drop(["GROUP_DEPTH", "WELLBORE"], axis=1),
                    model=[Model()[model] for model in models],
                    type_model=type_model,
                    dependent_col=dependent_col.upper(),
                    type_scale=SkillScale()[skill_scale],
                    k_fold=int(k_fold),
                    shuffle=bool(shuffle),
                    pca=bool(pca),
                    poly=bool(poly),
                )
                df_result = df_result.round(2).reset_index()
                df_result["GROUP"] = group
                result.append(df_result)
        return pd.concat(result)
    return (
        strat_train(
            df=df.drop(["WELLBORE"], axis=1),
            model=[Model()[model] for model in models],
            type_model=type_model,
            dependent_col=dependent_col.upper(),
            type_scale=SkillScale()[skill_scale],
            k_fold=int(k_fold),
            shuffle=bool(shuffle),
        )
        .round(2)
        .reset_index()
    )


def strat_train(
    df: pd.DataFrame,
    model: list,
    type_model: str,
    dependent_col: str,
    type_scale: SkillScale,
    k_fold: int = 5,
    shuffle: bool = True,
    randomstate: int = 42,
    pca: bool = False,
    poly: bool = False,
):
    if type_model == "auto":
        return cross_validate_kfold(
            df=df,
            dependent_col=dependent_col,
            n_splits=k_fold,
            random_state=randomstate,
            shuffle=shuffle,
            scale=type_scale,
            pca=pca,
            poly=poly,
        )
    return cross_validate_kfold(
        df=df,
        dependent_col=dependent_col,
        n_splits=k_fold,
        random_state=randomstate,
        shuffle=shuffle,
        scale=type_scale,
        models=model,
        pca=poly,
        poly=poly,
    )


def callbacks_uploaddata(app: Dash) -> None:
    @app.callback(
        Output("box-upload-file", "children"),
        Input("upload-data", "contents"),
        State("upload-data", "filename"),
        State("upload-data", "last_modified"),
    )
    def update_output(list_of_contents, list_of_names, list_of_dates):
        file_supported = ["csv", "asc", "h5", "xls"]
        clean_external_data(file_endwith=file_supported)
        if list_of_contents is not None:
            children = [
                parse_contents(c, n, d, file_supported)
                for c, n, d in zip(list_of_contents, list_of_names, list_of_dates)
            ]
            transform_to_processed(
                NAME_FULLDF_APP,
                PATH_EXTERNAL_DATA,
                PATH_INTERIM_APP,
                import_file_endswith="h5",
            )
            return children
        return None


def callbacks_feature(app: Dash) -> None:
    cols = ["vwcl", "phie", "sw", "perm_core", "phi_core", "vcl_core"]
    type__data = ["full", "case1", "case2"]

    @app.callback(
        [
            Output(f"result-{type}__{col}", "data")
            for type in ColsData().type_data
            for col in ColsData().cols
        ],
        [
            Input("train-model", "n_clicks"),
            State("skill-outlier", "value"),
            State("skill-scale", "value"),
            State("missing-value", "value"),
            State("orther-processing", "value"),
            State("standerize-column", "value"),
            State("model", "value"),
            State("k-fold", "value"),
            State("type-model", "value"),
            State("type-shuffle", "value"),
        ],
    )
    def build_model(
        click,
        skill_outlier: SkillOutlier,
        skill_scale: SkillScale,
        missing_value: RemoveMissing,
        orther_processing: str,
        standerize_column: str,
        models: Model,
        k_fold: int,
        type_model: bool,
        shuffle: bool,
    ):
        if "train-model" == ctx.triggered_id:
            df = get_full_data()
            result = list()
            for type_data in type__data:
                for col in cols:
                    df_tmp = loc_df_dependent_col(df, col.upper(), ["WELLBORE"])
                    df_tmp = df_tmp.astype({col.upper(): "float64"})
                    df_tmp = check_feature(df_tmp, skill_scale, type="Normalizer")
                    df_tmp = check_feature(df_tmp, missing_value, type="RemoveMissing")
                    df_tmp = check_feature(
                        df_tmp, skill_outlier, type="Outlier", dependent_col=col.upper()
                    )
                    df_tmp = check_feature(df_tmp, missing_value, type="RemoveMissing")
                    df_tmp = df_tmp.dropna(subset=[col.upper()])
                    print(df_tmp)
                    result_col = get_data_type(
                        df_tmp,
                        type=type_data,
                        dependent_col=col,
                        models=models,
                        type_model=type_model,
                        skill_scale=skill_scale,
                        k_fold=k_fold,
                        shuffle=shuffle,
                        pca=("Pca" in orther_processing),
                        poly=("Poly" in orther_processing),
                    )
                    result.append(result_col.to_dict("records"))
            return tuple(result)
        return tuple([None for _ in range(len(type__data) * len(cols))])


def callbacks_update_model(app: Dash) -> None:
    @app.callback(
        Output("model", "options"),
        Input("missing-value", "value"),
    )
    def update_model(missing_value: RemoveMissing):
        return (
            [{"label": model, "value": model} for model in Model.switch_modelboost()]
            if missing_value != RemoveMissing()._name[0]
            else [{"label": model, "value": model} for model in Model()]
        )
def callbacks_update_orther_processing(app: Dash) -> None:
    @app.callback(
        Output("orther-processing", "options"),
        Input("missing-value", "value"),
    )
    def update_orther_processing(missing_value: RemoveMissing):
        return (
            [{"label": skill, "value": skill} for skill in OrtherSkills.switch_skillmissing()]
            if missing_value != RemoveMissing()._name[0] and missing_value is not None
            else [{"label": skill, "value": skill} for skill in OrtherSkills()]
        )
            

def callbacks(app: Dash) -> None:
    callbacks_uploaddata(app)
    callbacks_update_model(app)
    callbacks_update_orther_processing(app)
    callbacks_feature(app)
