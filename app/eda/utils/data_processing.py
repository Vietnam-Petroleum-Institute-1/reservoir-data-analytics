from typing import List, Literal
from settings import PATH_RESULT_DATA
import pandas as pd
import os
import numpy as np


def get_data(data_type: Literal["FULL", "CASE1", "CASE2"]):
    if data_type == "FULL":
        df = pd.read_csv(f"{PATH_RESULT_DATA}full.csv")
    elif data_type == "CASE1":
        df = pd.read_csv(f"{PATH_RESULT_DATA}case1.csv")
    elif data_type == "CASE2":
        df = pd.read_csv(f"{PATH_RESULT_DATA}case2.csv")
    return df


def get_name_group(data_type: Literal["FULL", "CASE1", "CASE2"]):
    if data_type == "CASE1":
        name_group = "GROUP_DISTANCE"
    elif data_type == "CASE2":
        name_group = "GROUP_DEPTH"
    else:
        name_group = None
    return name_group


def loc_df(
    df: pd.DataFrame,
    data_type: Literal["FULL", "CASE1", "CASE2"],
    group: str = None,
    well: str = None,
):
    name_group = get_name_group(data_type)
    return (
        df[(df["WELLBORE"] == well) & (df[name_group] == group)]
        if data_type != "FULL"
        else df[df["WELLBORE"] == well]
    )

def get_eda_data(data_type: Literal["FULL", "CASE1", "CASE2"]):
    if data_type == "FULL":
        data_path = f"{PATH_RESULT_DATA}full/"
    elif data_type == "CASE1":
        data_path = f"{PATH_RESULT_DATA}case1/"
    elif data_type == "CASE2":
        data_path = f"{PATH_RESULT_DATA}case2/"
    return data_path

def avg_eda_value(
    data_type: Literal["FULL", "CASE1", "CASE2"],    
    data_path: str = None,
    group: str = None,
    well: str = None,
):
    
    r2_train = []
    r2_test = []
    mse = []
    rmse = []
    mae = []
    smape = []
    evs = []

    for file in os.listdir(data_path):
        
        data = pd.read_pickle(f"{data_path}{file}")
        data = data[data["well"] == int(well)]
        if (group is not None) & (data_type != 'FULL'):
            data = data[data["group"] == int(group)]
        data_r2_train = np.average(data["r2_train"])
        data_r2_test = np.average(data["r2_test"])
        data_mse = np.average(data["mse"])
        data_rmse = np.average(data["rmse"])
        data_mae = np.average(data["mae"])
        data_smape = np.average(data["smape"])
        data_evs = np.average(data["evs"])

        r2_train.append(data_r2_train)
        r2_test.append(data_r2_test)
        mse.append(data_mse)
        rmse.append(data_rmse)
        mae.append(data_mae)
        smape.append(data_smape)
        evs.append(data_evs)

    return np.average(r2_train), np.average(r2_test), np.average(mse), np.average(rmse), np.average(mae), np.average(smape), np.average(evs)

def eda_value(
    data_type: Literal["FULL", "CASE1", "CASE2"],    
    data_path: str = None,
    col: str = None,
    group: str = None,
    well: str = None,
):
    data = pd.read_pickle(f"{data_path}{col}.pkl")
    data = data[data["well"] == int(well)]
    if (group is not None) & (data_type != 'FULL'):
        data = data[data["group"] == int(group)]
    
    r2_train = np.average(data["r2_train"])
    r2_test = np.average(data["r2_test"])
    mse = np.average(data["mse"])
    rmse = np.average(data["rmse"])
    mae = np.average(data["mae"])
    smape = np.average(data["smape"])
    evs = np.average(data["evs"])

    return r2_train, r2_test, mse, rmse, mae, smape, evs