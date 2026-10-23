from contextlib import contextmanager
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import os
import pathlib
import tempfile
import textwrap
import threading

from sphinx.application import Sphinx

REF_TOKENS = {
    "--md-ref-palette-primary40": "#0b57d0",
    "--md-ref-palette-secondary40": "#00639b",
    "--md-ref-palette-neutral10": "#1f1f1f",
    "--md-ref-palette-neutral100": "#ffffff",
    "--md-ref-palette-neutral-variant30": "#444746",
    "--md-ref-palette-neutral-variant80": "#c4c7c5",
    "--md-ref-typeface-plain": '"Google Sans Text", system-ui, sans-serif',
    "--md-ref-typeface-weight-medium": "500",
}

SYS_TOKENS = {
    "--md-sys-color-primary": "#0b57d0",
    "--md-sys-color-secondary": "#00639b",
    "--md-sys-color-surface": "#ffffff",
    "--md-sys-color-on-surface": "#1f1f1f",
    "--md-sys-color-on-surface-variant": "#444746",
    "--md-sys-color-outline-variant": "#c4c7c5",
    "--md-sys-typescale-title-small-font": '"Google Sans Text", system-ui, sans-serif',
    "--md-sys-typescale-title-small-size": "0.875rem",
    "--md-sys-typescale-title-small-line-height": "1.25rem",
    "--md-sys-typescale-title-small-weight": "500",
    "--md-sys-typescale-title-small-tracking": "0.00625rem",
    "--md-sys-state-hover-state-layer-opacity": "8%",
    "--md-sys-state-pressed-state-layer-opacity": "10%",
    "--md-sys-state-focus-indicator-thickness": "3px",
}

SYS_COLORS = {
    "primary": "rgb(11, 87, 208)",
    "secondary": "rgb(0, 99, 155)",
    "surface": "rgb(255, 255, 255)",
    "on-surface": "rgb(31, 31, 31)",
    "on-surface-variant": "rgb(68, 71, 70)",
    "outline-variant": "rgb(196, 199, 197)",
}

SYS_TYPESCALE = {
    "title-small": {
        "fontFamily": '"Google Sans Text", system-ui, sans-serif',
        "fontSize": "14px",
        "lineHeight": "20px",
        "fontWeight": "500",
        "letterSpacing": "0.1px",
    },
}

SYS_STATE = {
    "focus-indicator-thickness": "3px",
    "hover": {
        "primary": "color(srgb 0.0431373 0.341176 0.815686 / 0.08)",
        "on-surface": "color(srgb 0.121569 0.121569 0.121569 / 0.08)",
    },
    "pressed": {
        "primary": "color(srgb 0.0431373 0.341177 0.815686 / 0.1)",
        "on-surface": "color(srgb 0.121569 0.121569 0.121569 / 0.1)",
    },
}


def get_chromium_executable() -> str:
    """Returns path to the hermetic Chromium binary from Bazel runfiles."""
    rpath = os.environ.get("PYTHON_RUNFILES") or os.environ.get("RUNFILES_DIR")
    if not rpath and os.environ.get("TEST_SRCDIR"):
        rpath = os.environ["TEST_SRCDIR"]

    if rpath:
        runfiles_base = pathlib.Path(rpath)
        for p in runfiles_base.glob("**/+*playwright_chromium*/**/chrome"):
            if p.is_file() and os.access(p, os.X_OK):
                return str(p)
        for p in runfiles_base.glob("**/playwright_chromium*/**/chrome"):
            if p.is_file() and os.access(p, os.X_OK):
                return str(p)

    for p in pathlib.Path.cwd().glob("**/+*playwright_chromium*/**/chrome"):
        if p.is_file() and os.access(p, os.X_OK):
            return str(p)

    raise FileNotFoundError(
        "Hermetic Chromium binary not found in Bazel runfiles."
    )


@contextmanager
def build_docs(files: dict[str, str]):
    """Builds an isolated Sphinx site in a temporary directory and yields the output path."""
    for required in ("conf.py", "index.rst"):
        if required not in files:
            raise ValueError(f"build_docs requires {required!r} in `files`.")

    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = pathlib.Path(tmp)
        srcdir = tmp_path / "src"
        srcdir.mkdir()

        for fname, content in files.items():
            fpath = srcdir / fname
            fpath.parent.mkdir(parents=True, exist_ok=True)
            fpath.write_text(textwrap.dedent(content))

        outdir = tmp_path / "out"
        outdir.mkdir()
        doctreedir = tmp_path / "doctrees"
        doctreedir.mkdir()

        app = Sphinx(str(srcdir), str(srcdir), str(outdir), str(doctreedir), "html")
        app.build()
        yield outdir


class _QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        pass


class DocsServer:
    """Local HTTP server for serving built documentation during tests."""

    def __init__(self, directory: pathlib.Path):
        self.directory = pathlib.Path(directory)
        handler = partial(_QuietHandler, directory=str(self.directory))
        self.httpd = ThreadingHTTPServer(("127.0.0.1", 0), handler)
        self.port = self.httpd.server_address[1]
        self.thread = threading.Thread(
            target=self.httpd.serve_forever,
            daemon=True,
        )

    def start(self) -> None:
        self.thread.start()

    def stop(self) -> None:
        self.httpd.shutdown()
        self.httpd.server_close()

    def url_for(self, path: str = "") -> str:
        return f"http://127.0.0.1:{self.port}/{path.lstrip('/')}"

    def __enter__(self) -> "DocsServer":
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.stop()


@contextmanager
def run_playwright(viewport=None, java_script_enabled=True, **kwargs):
    """Context manager to run Playwright and yield a page object."""
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=get_chromium_executable())
        context_kwargs = {"java_script_enabled": java_script_enabled}
        if viewport:
            context_kwargs["viewport"] = viewport
        context_kwargs.update(kwargs)
        context = browser.new_context(**context_kwargs)
        timeout_ms = 4000
        context.set_default_timeout(timeout_ms)
        context.set_default_navigation_timeout(timeout_ms)
        page = context.new_page()
        try:
            yield page
        finally:
            browser.close()
