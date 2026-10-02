import unittest
from playwright.sync_api import expect
from harness import SphinxTestBase


class TestHiRole(SphinxTestBase):
    def test_link(self):
        outdir = self.build_docs(
            conf_content="""
                project = "test_link"
                extensions = ["paz"]
                html_theme = "paz"
            """,
            index_content="""
                =========
                test_link
                =========

                `click me <https://example.com>`__
            """
        )
        url = self.start_server(outdir)
        with self.run_playwright() as page:
            page.goto(f"{url}/")
            page.get_by_role("link", name="click me").click()
            expect(page).to_have_url("https://example.com/")


if __name__ == "__main__":
    unittest.main()
