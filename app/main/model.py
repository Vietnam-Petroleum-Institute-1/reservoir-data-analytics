import os
import sys

import lightgbm as lgb
import xgboost as xgb
from catboost import CatBoostRegressor
from imodels import (AdaBoostRegressor, BoostedRulesRegressor,
                     DecisionTreeCCPRegressor, FIGSRegressor)
from settings import PATH_CODE
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.linear_model import Lasso, LinearRegression, Ridge
from sklearn.neighbors import KNeighborsRegressor
from sklearn.svm import SVR
from sklearn.tree import DecisionTreeRegressor

path = os.path.join(PATH_CODE)
sys.path.append(path)
from src.features.build_features import (loc_lld_lls, remove_missing,
                                         remove_outlier_CD, remove_outlier_IQR,
                                         remove_outlier_std,
                                         remove_outlier_zscore)


class Model:
    _data_default = [
            LinearRegression(),
            Lasso(),
            Ridge(),
            DecisionTreeRegressor(),
            RandomForestRegressor(),
            GradientBoostingRegressor(),
            SVR(),
            KNeighborsRegressor(),
            xgb.XGBRegressor(),
            lgb.LGBMRegressor(),
            AdaBoostRegressor(),
            BoostedRulesRegressor(),
            DecisionTreeCCPRegressor(estimator_=DecisionTreeRegressor()),
            FIGSRegressor(),
            CatBoostRegressor(logging_level="Silent"),
            xgb.XGBRFRegressor(),
        ]
    _data_boost = [xgb.XGBRFRegressor(), xgb.XGBRegressor(), lgb.LGBMRegressor(), CatBoostRegressor(logging_level="Silent")]
        
    def __init__(self, models: list = None):
        self._data = list(self._data_default) if models is None else models
        self._name = [model.__class__.__name__ for model in self._data]
        self._model = dict(zip(self._name, self._data))
    
    @classmethod
    def switch_modelboost(cls):
        return cls(models=cls._data_boost)
    

    def __getitem__(self, name):
        return self._model[name]

    def __iter__(self):
        return iter(self._model)

    def __len__(self):
        return len(self._model)

    def __repr__(self):
        return f"{self._name}"

    def __str__(self):
        return f"{self._name}"
    


class SkillOutlier:
    def __init__(self):
        self._data = [
            remove_outlier_IQR,
            remove_outlier_zscore,
            remove_outlier_std,
            remove_outlier_CD,
            loc_lld_lls,
        ]
        self._name = ["IQR", "ZSCORE", "STD", "COOKS DISTANCE", "By Hand (LLD > 2000)"]
        self._model = dict(zip(self._name, self._data))

    def __getitem__(self, name):
        return self._model[name]

    def __iter__(self):
        return iter(self._model)

    def __len__(self):
        return len(self._model)

    def __repr__(self):
        return f"{self._name}"

    def __str__(self):
        return f"{self._name}"


class SkillScale:
    def __init__(self):
        self._name = ["Standard", "MinMax", "Robust", "MaxAbs", "Power", "Quantile"]
        self._model = dict(zip(self._name, self._name))

    def __getitem__(self, name):
        return self._model[name]

    def __iter__(self):
        return iter(self._model)

    def __len__(self):
        return len(self._model)

    def __repr__(self):
        return f"{self._name}"

    def __str__(self):
        return f"{self._name}"


class RemoveMissing:
    def __init__(self):
        self.data = remove_missing
        self._name = [
            "Any",
            "All",
            "Keep 2 col",
            "Keep 3 col",
            "Keep 4 col",
        ]
        self._model = dict(zip(self._name, [self.data for _ in range(len(self._name))]))

    def __getitem__(self, name):
        return self._model[name]

    def __iter__(self):
        return iter(self._model)

    def __len__(self):
        return len(self._model)

    def __repr__(self):
        return f"{self._name}"

    def __str__(self):
        return f"{self._name}"
    
class OrtherSkills:
    _data_default = [
        "Pca",
        "Poly"
    ]
    _data_change_datamissing = []
    def __init__(self, data: list = None):
        self._name = list(self._data_default) if data is None else data 
        self._model = dict(zip(self._name, self._name))
    
    @classmethod
    def switch_skillmissing(cls):
        return cls(data=cls._data_change_datamissing)
    
    def __getitem__(self, name):
        return self._model[name]

    def __iter__(self):
        return iter(self._model)

    def __len__(self):
        return len(self._model)

    def __repr__(self):
        return f"{self._name}"

    def __str__(self):
        return f"{self._name}"
        
class ColsData:
    def __init__(self):
        self._cols = ["vwcl", "phie", "sw", "perm_core", "phi_core", "vcl_core"]
        self._type__data = ["full", "case1", "case2"]
        self._data = dict(zip(self._cols, self._cols))
    
    @property
    def cols(self):
        return self._cols
    
    @property
    def type_data(self):
        return self._type__data
    
    def __setitem__(self, name, value):
        self._data[name] = value