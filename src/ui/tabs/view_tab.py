import gradio as gr
from src.core.utils import load_data


def create_view_tab(df, cfg):

    with gr.Tab("📋 View Projects"):
        df_view = gr.Dataframe(
            df,
            interactive=False,
            wrap=True,
            datatype=["markdown"] * len(df.columns)
        )

        refresh_btn = gr.Button("🔄 update data")

        refresh_btn.click(
            fn=load_data,
            inputs=[gr.State(cfg)],
            outputs=[df_view]
        )
