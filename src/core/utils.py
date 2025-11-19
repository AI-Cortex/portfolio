from typing import Union
from omegaconf import DictConfig, OmegaConf, ListConfig
import pandas as pd
import os
from pathlib import Path
import gradio as gr
from collections import OrderedDict
from pandas import DataFrame

CONFIG_PATH = "config/config.yaml"


def get_columns(cfg: Union[DictConfig, ListConfig]):
    col = []
    for key, value in cfg.columns.items():
        col.append(value.name)
    return col


def load_data(cfg: Union[DictConfig, ListConfig]):
    path = cfg.data_path
    columns = get_columns(cfg)

    if Path(path).exists():
        df = pd.read_parquet(path, engine="fastparquet")
    else:
        df = pd.DataFrame(columns=columns)
        save_data(df, cfg)
    return df


def save_data(df: pd.DataFrame, cfg: Union[DictConfig, ListConfig]):
    path = cfg.data_path
    df.to_parquet(path, engine="fastparquet")


def load_config(path: str = CONFIG_PATH):
    return OmegaConf.load(path)


def update_dropdown(cfg: Union[DictConfig, ListConfig]):
    df = load_data(cfg)
    names = df.iloc[:, 0].tolist()
    return gr.update(choices=names, value=names[0])


class Fields:
    def __init__(self):
        self.d = OrderedDict()

    def add(self, d: OrderedDict):
        self.d.update(d)

    def values(self):
        return list(self.d.values())

    def empty_values(self):
        lst = []
        for k in self.d.keys():
            # string type
            if isinstance(self.d[k], str):
                lst.append("")
            # list type
            elif isinstance(self.d[k], list):
                lst.append([])
            else:
                lst.append(None)
        return lst

    def new_row(self, cfg: DictConfig):
        cfg = cfg.columns
        d = OrderedDict()
        for (key, value) in self.d.items():
            d[cfg[key].name] = value
        return d

    def condition(self, df: DataFrame):
        if not self.d["project_name"].strip():
            return False, "❌ **Error:** Project name is required!"
        if self.d['project_name'].strip() in df.iloc[:, 0].tolist():
            return False, "❌ **Error:** Project name already exists!"
        return True, ""
