import unittest
from harness import DocsServer, build_docs, run_playwright


class ConsoleTest(unittest.TestCase):
    def test_no_errors(self):
        conf = """
            project = "test_no_errors"
            extensions = ["md3"]
            html_theme = "md3"
        """
        index = """
            ==============
            test_no_errors
            ==============
        """
        files = {"conf.py": conf, "index.rst": index}
        with build_docs(files) as outdir:
            with DocsServer(outdir) as server:
                with run_playwright() as page:
                    errors = []
                    page.on(
                        "console",
                        lambda msg: errors.append(msg.text) if msg.type == "error" else None,
                    )
                    page.on("pageerror", lambda err: errors.append(str(err)))

                    page.goto(server.url_for("index.html"))
                    self.assertEqual(errors, [])


if __name__ == "__main__":
    unittest.main()
