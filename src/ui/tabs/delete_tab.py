import gradio as gr
from omegaconf import DictConfig
import pandas as pd
from pandas import DataFrame
from src.core.utils import *
from typing import List
import numpy as np


def row_to_md(project_name, cfg):

    df = load_data(cfg)
    seri = df[df.iloc[:, 0] == project_name]
    if len(seri) == 0:
        return "## ❌ Project not found!"
    else:
        seri = seri.iloc[0]

    md = ""
    for idx, value in seri.items():
        md += f"# **{idx}:** \n"
        if isinstance(value, np.ndarray):
            for item in value:
                md += f"- {item}\n"
        else:
            md += str(value)
        md += "\n\n"
    return md


def delete_handler(cfg: DictConfig, project_name: str, msg: str = 'delete'):
    """Handle deleting a project."""
    df = load_data(cfg)
    if project_name not in df.iloc[:, 0].tolist():
        gr.Warning("Project not found!")
        return update_dropdown(cfg)

    df = df[df.iloc[:, 0] != project_name]
    save_data(df, cfg)
    gr.Info(f"✅ Project {msg} successfully!")
    return update_dropdown(cfg)


def create_delete_tab(cfg: Union[DictConfig, ListConfig]):

    # project name
    with gr.Tab("📋 Delete Projects"):
        df = load_data(cfg)
        names = df.iloc[:, 0].tolist()

        with gr.Row():
            refresh_btn = gr.Button("🔄 update data")
            project_name = gr.Dropdown(
                choices=names,
                label="Select project to delete",
                interactive=True,
                allow_custom_value=True,

            )

        project_info = gr.Markdown(
            row_to_md(names[0] if names else "No Project", cfg))
        del_btn = gr.Button("🗑️ Delete Project", variant="stop")

        refresh_btn.click(
            fn=update_dropdown,
            inputs=[gr.State(cfg)],
            outputs=[project_name]
        )

        project_name.change(
            fn=row_to_md,
            inputs=[project_name, gr.State(cfg)],
            outputs=project_info
        )

        del_btn.click(
            fn=delete_handler,
            inputs=[gr.State(cfg), project_name],
            outputs=[project_name]
        )
