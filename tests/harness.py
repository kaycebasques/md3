import http.server
import pathlib
import socketserver
import tempfile
import textwrap
import threading
import unittest
from contextlib import contextmanager

from playwright.sync_api import sync_playwright
from sphinx.application import Sphinx

from md3_spec import (
    MD3_SPECS,
    Md3ConformanceMixin,
    format_md3_failure,
    md3_conformance,
)


class SphinxTestBase(Md3ConformanceMixin, unittest.TestCase):
    """Base class for Sphinx theme and extension tests.

    Handles temporary directories, HTTP server lifecycle, and MD3 conformance assertions.
    """
    @classmethod
    def setUpClass(cls):
        cls.temp_dir = tempfile.TemporaryDirectory()
        cls.tmp_path = pathlib.Path(cls.temp_dir.name)
        cls.httpd = None
        cls.server_thread = None

    @classmethod
    def tearDownClass(cls):
        if cls.httpd:
            try:
                cls.httpd.shutdown()
                cls.httpd.server_close()
            except Exception:
                pass
        cls.temp_dir.cleanup()

    @classmethod
    def build_docs(cls, conf_content, index_content, extra_files=None, outdir_name="out"):
        """Builds Sphinx documentation in the temp directory."""
        srcdir = cls.tmp_path / f"src_{outdir_name}"
        srcdir.mkdir(parents=True, exist_ok=True)
        (srcdir / "conf.py").write_text(textwrap.dedent(conf_content))
        (srcdir / "index.rst").write_text(textwrap.dedent(index_content))

        if extra_files:
            for fname, content in extra_files.items():
                fpath = srcdir / fname
                fpath.parent.mkdir(parents=True, exist_ok=True)
                fpath.write_text(textwrap.dedent(content))

        outdir = cls.tmp_path / outdir_name
        outdir.mkdir(parents=True, exist_ok=True)
        doctreedir = cls.tmp_path / f"doctrees_{outdir_name}"
        doctreedir.mkdir(parents=True, exist_ok=True)

        app = Sphinx(str(srcdir), str(srcdir), str(outdir), str(doctreedir), "html")
        app.build()
        return outdir

    @classmethod
    def start_server(cls, directory):
        """Starts an in-process HTTP server serving the specified directory."""
        if cls.httpd:
            try:
                cls.httpd.shutdown()
                cls.httpd.server_close()
            except Exception:
                pass

        directory = str(directory)

        class QuietHandler(http.server.SimpleHTTPRequestHandler):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, directory=directory, **kwargs)

            def log_message(self, format, *args):
                pass

        cls.httpd = socketserver.TCPServer(("127.0.0.1", 0), QuietHandler)
        cls.port = cls.httpd.server_address[1]
        cls.server_thread = threading.Thread(target=cls.httpd.serve_forever, daemon=True)
        cls.server_thread.start()
        return f"http://127.0.0.1:{cls.port}"

    @contextmanager
    def run_playwright(self, viewport=None, java_script_enabled=True, **kwargs):
        """Context manager to run Playwright and yield a page object."""
        with sync_playwright() as p:
            browser = p.chromium.launch()
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
