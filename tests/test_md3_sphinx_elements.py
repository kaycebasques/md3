import unittest
from harness import SphinxTestBase, md3_conformance


class TestMd3SphinxElements(SphinxTestBase):
    """Verifies that Sphinx docutils elements and Pygments highlighting receive proper MD3 styling."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        conf_content = """
            project = "ElementsTest"
            extensions = ["md3"]
            html_theme = "md3"
        """
        index_content = """
            =============
            Elements Test
            =============

            .. toctree::
               :maxdepth: 2

               page_b

            Body paragraph with `an inline hyperlink <https://example.com>`__ inside article prose.

            ----

            .. note::
               This is a note callout.

            .. tip::
               This is a tip callout.

            .. warning::
               This is a warning callout.

            .. danger::
               This is a danger callout.

            .. code-block:: python

               def compute(x: int) -> str:
                   return "result"

            .. list-table:: Sample Table
               :header-rows: 1

               * - Heading 1
                 - Heading 2
               * - Data 1
                 - Data 2
        """
        page_b_content = """
            ======
            Page B
            ======

            Content on page B.
        """
        outdir = cls.build_docs(
            conf_content,
            index_content,
            extra_files={"page_b.rst": page_b_content},
            outdir_name="elements_out",
        )
        cls.url = cls.start_server(outdir)

    @md3_conformance(spec_key="SPHINX_ADMONITIONS")
    def test_admonitions_rendered_with_md3_containers_and_colors(self):
        """Verifies that admonitions (note, tip, warning, danger) render with MD3 container tokens."""
        with self.run_playwright() as page:
            page.goto(f"{self.url}/index.html")

            for kind, label in [
                ("note", "Note"),
                ("tip", "Tip"),
                ("warning", "Warning"),
                ("danger", "Danger"),
            ]:
                adm = page.locator(f".admonition.{kind}")
                self.assertEqual(adm.count(), 1)
                self.assertIn(label, adm.inner_text())

            # Verify computed border-radius matches --md-sys-shape-corner-medium (12px)
            radius = page.evaluate(
                "window.getComputedStyle(document.querySelector('.admonition.note')).borderRadius"
            )
            self.assertEqual(radius, "12px")

    def test_hyperlinks_underlined_and_dividers_styled(self):
        """Verifies inline body hyperlinks are underlined in primary color and horizontal dividers use 1px outline-variant."""
        with self.run_playwright() as page:
            page.goto(f"{self.url}/index.html")
            page.evaluate("document.documentElement.dataset.theme = 'light'")

            with self.spec_context(spec_key="TYPOGRAPHY_HYPERLINKS"):
                link_styles = page.evaluate(
                    """() => {
                        const link = document.querySelector('.md3-article p a.reference.external');
                        const headerlink = document.querySelector('.md3-article a.headerlink');
                        const lcs = window.getComputedStyle(link);
                        const hcs = window.getComputedStyle(headerlink);
                        return {
                            linkColor: lcs.color,
                            linkDecoration: lcs.textDecorationLine,
                            headerlinkDecoration: hcs.textDecorationLine,
                        };
                    }"""
                )
                self.assertEqual(link_styles["linkColor"], "rgb(11, 87, 208)")
                self.assertIn("underline", link_styles["linkDecoration"])
                self.assertEqual(link_styles["headerlinkDecoration"], "none")

            with self.spec_context(spec_key="COMPONENTS_DIVIDER"):
                hr_styles = page.evaluate(
                    """() => {
                        const hr = document.querySelector('.md3-article hr');
                        const cs = window.getComputedStyle(hr);
                        return {
                            borderTopWidth: cs.borderTopWidth,
                            borderTopColor: cs.borderTopColor,
                        };
                    }"""
                )
                self.assertEqual(hr_styles["borderTopWidth"], "1px")
                # outline-variant in light mode is #c4c7c5 -> rgb(196, 199, 197)
                self.assertEqual(hr_styles["borderTopColor"], "rgb(196, 199, 197)")

    @md3_conformance(spec_key="SPHINX_PYGMENTS")
    def test_pygments_syntax_highlighting_stylesheets_loaded_and_active(self):
        """Verifies that pygments.css and pygments_dark.css are loaded and highlight code tokens."""
        with self.run_playwright() as page:
            page.goto(f"{self.url}/index.html")

            stylesheets = page.evaluate(
                "Array.from(document.querySelectorAll('link[rel=\"stylesheet\"]')).map(l => l.getAttribute('href'))"
            )
            self.assertTrue(
                any(href.endswith("pygments.css") for href in stylesheets),
                f"Expected pygments.css in stylesheets, found {stylesheets}",
            )
            self.assertTrue(
                any(href.endswith("pygments_dark.css") for href in stylesheets),
                f"Expected pygments_dark.css in stylesheets, found {stylesheets}",
            )

            page.evaluate(
                "document.documentElement.dataset.theme = 'light'; document.getElementById('pygments_dark_css').media = 'not all';"
            )
            light_kw_color = page.evaluate(
                "window.getComputedStyle(document.querySelector('.highlight .k')).color"
            )
            light_body_color = page.evaluate(
                "window.getComputedStyle(document.querySelector('.highlight pre')).color"
            )
            self.assertNotEqual(
                light_kw_color,
                light_body_color,
                "Keyword token (.highlight .k) should be syntax-highlighted in light mode",
            )

            page.locator("md3-theme-toggle").click()
            dark_kw_color = page.evaluate(
                "window.getComputedStyle(document.querySelector('.highlight .k')).color"
            )
            self.assertNotEqual(
                dark_kw_color,
                light_kw_color,
                "Keyword token (.highlight .k) color should switch to monokai dark palette in dark mode",
            )

    def test_tables_rendered_with_md3_styles_and_tabular_numerals(self):
        """Verifies data tables render with MD3 styling and tabular-nums."""
        with self.run_playwright() as page:
            page.goto(f"{self.url}/index.html")

            with self.spec_context(spec_key="DENSITY_TABLES"):
                table = page.locator("table.docutils")
                self.assertEqual(table.count(), 1)
                th = page.locator("table.docutils th").first
                self.assertIn("Heading 1", th.inner_text())

            with self.spec_context(spec_key="TYPOGRAPHY_TABULAR_NUMERALS"):
                fvn = page.evaluate(
                    "window.getComputedStyle(document.querySelector('table.docutils')).fontVariantNumeric"
                )
                self.assertIn("tabular-nums", fvn)

    @md3_conformance(spec_key="SPHINX_PAGINATION")
    def test_pagination_cards(self):
        """Verifies pagination next card appears on first page of multi-page doc."""
        with self.run_playwright() as page:
            page.goto(f"{self.url}/index.html")

            next_card = page.locator(".md3-pagination__next")
            self.assertEqual(next_card.count(), 1)
            self.assertIn("next", next_card.inner_text().lower())
            self.assertIn("Page B", next_card.inner_text())

            # Navigate to Page B
            next_card.click()
            page.wait_for_url("**/page_b.html")

            # Page B has Previous card linking back to Elements Test
            prev_card = page.locator(".md3-pagination__prev")
            self.assertEqual(prev_card.count(), 1)
            self.assertIn("previous", prev_card.inner_text().lower())
            self.assertIn("Elements Test", prev_card.inner_text())

    @md3_conformance(spec_key="SPHINX_BREADCRUMBS")
    def test_breadcrumbs_rendered(self):
        """Verifies breadcrumbs navigation renders project and page trail."""
        with self.run_playwright() as page:
            page.goto(f"{self.url}/page_b.html")

            breadcrumbs = page.locator(".md3-breadcrumbs")
            self.assertEqual(breadcrumbs.count(), 1)
            self.assertIn("ElementsTest", breadcrumbs.inner_text())
            self.assertIn("Page B", breadcrumbs.inner_text())


if __name__ == "__main__":
    unittest.main()
