import unittest
from harness import SphinxTestBase


class TestApp(SphinxTestBase):
    def test_app_exists_with_paz_extension(self):
        outdir = self.build_docs(
            conf_content="""
                project = "test_app"
                extensions = ["paz"]
                html_theme = "paz"
            """,
            index_content="""
                ========
                test_app
                ========
            """,
            outdir_name="out_paz",
        )
        url = self.start_server(outdir)
        with self.run_playwright() as page:
            page.goto(f"{url}/index.html")
            self.assertEqual(page.locator("paz-app").count(), 1)
            self.assertTrue(page.evaluate("Boolean(customElements.get('paz-app'))"))

    def test_app_exists_with_md3_extension(self):
        outdir = self.build_docs(
            conf_content="""
                project = "test_md3_app"
                extensions = ["md3"]
                html_theme = "md3"
            """,
            index_content="""
                ============
                test_md3_app
                ============
            """,
            outdir_name="out_md3",
        )
        url = self.start_server(outdir)
        with self.run_playwright() as page:
            page.goto(f"{url}/index.html")
            self.assertEqual(page.locator("paz-app").count(), 1)
            self.assertTrue(page.evaluate("Boolean(customElements.get('md3-app'))"))


if __name__ == "__main__":
    unittest.main()
