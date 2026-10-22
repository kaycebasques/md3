from pathlib import Path


def setup(app):
    app.add_html_theme("md3", Path(__file__).resolve().parent)
    return {
        "version": "0.0.0",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
