import unittest
from harness import SphinxTestBase


class TestHtml(SphinxTestBase):
    def test_title(self):
        outdir = self.build_docs(
            conf_content="""
                project = "test_title"
                extensions = ["paz"]
                html_theme = "paz"
            """,
            index_content="""
                ==========
                test_title
                ==========
            """
        )
        html = (outdir / "index.html").read_text()
        self.assertIn("<title>test_title</title>", html)


if __name__ == "__main__":
    unittest.main()
