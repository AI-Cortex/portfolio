from src.ui.layout import build_ui
import os
import argparse


def main():
    os.environ["NO_PROXY"] = "127.0.0.1,localhost"
    os.environ["http_proxy"] = ""
    os.environ["https_proxy"] = ""
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--share")
    args = parser.parse_args()
    
    demo = build_ui()
    demo.launch(share=args.share)


if __name__ == "__main__":
    main()
