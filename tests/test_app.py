import unittest
from harness import SphinxTestBase


class TestApp(SphinxTestBase):
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
            self.assertEqual(page.locator("md3-app").count(), 1)
            self.assertTrue(page.evaluate("Boolean(customElements.get('md3-app'))"))

    def test_app_exists_with_material3_theme_alias(self):
        outdir = self.build_docs(
            conf_content="""
                project = "test_material3_app"
                extensions = ["md3"]
                html_theme = "material3"
            """,
            index_content="""
                ==================
                test_material3_app
                ==================
            """,
            outdir_name="out_material3",
        )
        url = self.start_server(outdir)
        with self.run_playwright() as page:
            page.goto(f"{url}/index.html")
            self.assertEqual(page.locator("md3-app").count(), 1)
            self.assertTrue(page.evaluate("Boolean(customElements.get('md3-app'))"))


if __name__ == "__main__":
    unittest.main()
