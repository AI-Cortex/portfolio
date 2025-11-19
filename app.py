from src.ui.layout import build_ui
import os


def main():
    os.environ["NO_PROXY"] = "127.0.0.1,localhost"
    os.environ["http_proxy"] = ""
    os.environ["https_proxy"] = ""
    demo = build_ui()
    demo.launch()


if __name__ == "__main__":
    main()
