import gradio as gr
from omegaconf import DictConfig
from src.core.utils import *
import numpy as np
from src.ui.tabs.add_tab import add
from src.ui.tabs.delete_tab import delete_handler


def empty_list(cfg: DictConfig):
    lst = []
    for k, v in cfg.columns.items():
        lst.append(v.gr_clear)
    return lst


def show_data(selected_project, cfg):
    df = load_data(cfg)
    row = df[df.iloc[:, 0] == selected_project]
    if len(row) == 0:
        return empty_list(cfg)

    row = row.iloc[0].to_list()
    lst = []
    for item in row:
        if isinstance(item, np.ndarray):
            lst.append(item.tolist())
        else:
            lst.append(item)

    return lst


def edit(project_name, data_type, technique, problem_type,
         domain, tools, level, outcome, note, link,
         project_id, cfg):
    if project_name.strip() == "":
        gr.Warning("❌ **Error:** Project name is required!")
        return (project_name, data_type, technique, problem_type,
                domain, tools, level, outcome, note, link, project_id)

    if project_id == project_name:
        delete_handler(cfg, project_id, 'Edited_2')
        output = add(project_name, data_type, technique, problem_type,
                     domain, tools, level, outcome, note, link, cfg, 'Edited_1')

    else:
        output = add(project_name, data_type, technique, problem_type,
                     domain, tools, level, outcome, note, link, cfg, 'Edited_1')
        if output[0] == "":
            delete_handler(cfg, project_id, 'Edited_2')

    return *output, project_id


def create_edit_tab(cfg):
    """Create the add project tab with form inputs."""
    with gr.Tab("➕ Edit Project"):
        gr.Markdown("### ➕ Edit Existing Project")
        df = load_data(cfg)
        names = df.iloc[:, 0].tolist()
        with gr.Row():
            refresh_btn = gr.Button("🔄 update data")
            project_id = gr.Dropdown(
                choices=names,
                label="Select project to delete",
                interactive=True,
                allow_custom_value=True,

            )

        refresh_btn.click(
            fn=update_dropdown,
            inputs=[gr.State(cfg)],
            outputs=[project_id]
        )

        project_name = gr.Textbox(**cfg.columns.project_name.gr_kwargs)
        data_type = gr.CheckboxGroup(**cfg.columns.data_type.gr_kwargs)
        technique = gr.CheckboxGroup(**cfg.columns.technique.gr_kwargs)
        problem_type = gr.CheckboxGroup(**cfg.columns.problem_type.gr_kwargs)
        domain = gr.CheckboxGroup(**cfg.columns.domain.gr_kwargs)
        tools = gr.CheckboxGroup(**cfg.columns.tools.gr_kwargs)
        level = gr.Dropdown(**cfg.columns.level.gr_kwargs)
        outcome = gr.CheckboxGroup(**cfg.columns.outcome.gr_kwargs)
        note = gr.Textbox(**cfg.columns.note.gr_kwargs, lines=3)
        link = gr.Textbox(**cfg.columns.link.gr_kwargs, lines=1)

        edit_btn = gr.Button("✅ Edit Project", variant="primary")

        project_id.change(
            fn=show_data,
            inputs=[project_id, gr.State(cfg)],
            outputs=[
                project_name, data_type, technique, problem_type,
                domain, tools, level, outcome, note, link
            ]
        )

        edit_btn.click(
            fn=edit,
            inputs=[project_name, data_type, technique, problem_type,
                    domain, tools, level, outcome, note, link, project_id,
                    gr.State(cfg)],

            outputs=[project_name, data_type, technique, problem_type,
                     domain, tools, level, outcome, note, link, project_id
                     ]
        )
