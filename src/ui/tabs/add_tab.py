import gradio as gr
from omegaconf import DictConfig
import pandas as pd
from pandas import DataFrame
from src.core.utils import *
from typing import List
from collections import OrderedDict


def add_project(df, new_row, cfg):

    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    save_data(df, cfg)
    return df


def add_handler(fields: Fields, cfg, msg: str = 'added'):
    """Handle adding a new project."""

    df = load_data(cfg)
    condition_result, condition_msg = fields.condition(df)
    if not condition_result:
        return condition_msg
    new_row = fields.new_row(cfg)

    try:
        # Add the project
        updated_df = add_project(df, new_row, cfg)
        success_msg = f"✅ **Success:** Project has been {msg} successfully!"
        return success_msg

    except Exception as e:
        error_msg = f"❌ **Error:** Failed to {msg} project. {str(e)}"
        return error_msg


def add(project_name, data_type, technique, problem_type,
        domain, tools, level, outcome, link, cfg, msg: str = 'added'):
    fields = Fields()
    d = OrderedDict([
        ("project_name", project_name),
        ("data_type", data_type),
        ("technique", technique),
        ("problem_type", problem_type),
        ("domain", domain),
        ("tools", tools),
        ("level", level),
        ("outcome", outcome),
        ("link", link),
    ])
    fields.add(d)

    msg = add_handler(fields, cfg, msg)

    if msg.startswith("✅"):  # Return cleared form values
        gr.Info(msg)
        return fields.empty_values()
    else:  # Return original values to keep form filled
        gr.Warning(msg)
        return fields.values()


def create_add_tab(cfg):
    """Create the add project tab with form inputs."""

    with gr.Tab("➕ Add Project"):
        gr.Markdown("### ➕ Add New Project")

        project_name = gr.Textbox(**cfg.columns.project_name.gr_kwargs)
        data_type = gr.CheckboxGroup(**cfg.columns.data_type.gr_kwargs)
        technique = gr.CheckboxGroup(**cfg.columns.technique.gr_kwargs)
        problem_type = gr.CheckboxGroup(**cfg.columns.problem_type.gr_kwargs)
        domain = gr.CheckboxGroup(**cfg.columns.domain.gr_kwargs)
        tools = gr.CheckboxGroup(**cfg.columns.tools.gr_kwargs)
        level = gr.Dropdown(**cfg.columns.level.gr_kwargs)
        outcome = gr.CheckboxGroup(**cfg.columns.outcome.gr_kwargs)
        link = gr.Textbox(**cfg.columns.link.gr_kwargs)

        add_btn = gr.Button("✅ Add Project", variant="primary")

        add_btn.click(
            fn=add,
            inputs=[project_name, data_type, technique, problem_type,
                    domain, tools, level, outcome, link,

                    gr.State(cfg)],

            outputs=[project_name, data_type, technique, problem_type,
                     domain, tools, level, outcome, link,]
        )
