import gradio as gr
from src.core.utils import load_data, load_config
from src.ui.tabs.view_tab import create_view_tab
from src.ui.tabs.add_tab import create_add_tab
from src.ui.tabs.delete_tab import create_delete_tab
from src.ui.tabs.edit_tab import create_edit_tab
from omegaconf import DictConfig, ListConfig
from typing import cast
from gradio.themes import Soft


PATH = "config/config.yaml"


def build_ui():
    cfg = cast(DictConfig, load_config(PATH))
    df = load_data(cfg)

    with gr.Blocks(theme=Soft()) as demo:
        gr.Markdown(f"# {cfg['title']}\n{cfg['description']}")

        create_view_tab(df, cfg)

        create_add_tab(cfg)
        create_delete_tab(cfg)
        create_edit_tab(cfg)

    return demo
