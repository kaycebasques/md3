import unittest
from harness import build_docs


class LayoutTest(unittest.TestCase):
    def test_title(self):
        conf = """
            project = "test_title"
            extensions = ["md3"]
            html_theme = "md3"
        """
        index = """
            ==========
            test_title
            ==========
        """
        files = {"conf.py": conf, "index.rst": index}
        with build_docs(files) as outdir:
            html = (outdir / "index.html").read_text()
            self.assertIn("<title>test_title</title>", html)


if __name__ == "__main__":
    unittest.main()
