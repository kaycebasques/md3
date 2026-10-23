import unittest
from harness import DocsServer, build_docs, run_playwright
from sphinx.errors import ConfigError

DOCS_URL = "components/tabs.html"
DOCS_A11Y_URL = "components/tabs.html#accessibility"
MD3_SPECS_URL = "https://m3.material.io/components/tabs/specs#8602158e-a13b-432e-8133-b9cb34d61678"
MD3_A11Y_URL = "https://m3.material.io/components/tabs/accessibility#a1ebaebd-1bb4-4401-9962-8b30a563e49e"


class TabsTest(unittest.TestCase):
    def test_md3(self):
        files = {
            "conf.py": """
                project = "test_md3"
                extensions = ["md3"]
                html_theme = "md3"
            """,
            "index.rst": """
                ========
                test_md3
                ========

                .. toctree::
                   :hidden:

                   quickstart
            """,
            "quickstart.rst": """
                ==========
                Quickstart
                ==========
            """,
        }
        with build_docs(files) as outdir:
            with DocsServer(outdir) as server:
                with run_playwright() as page:
                    page.goto(server.url_for("index.html"))

                    self.assertTrue(
                        page.evaluate("Boolean(customElements.get('md3-tabs'))"),
                        f"See {DOCS_URL} and {MD3_SPECS_URL}",
                    )

                    nav_tabs = page.locator("md3-tabs")
                    self.assertEqual(
                        nav_tabs.count(),
                        1,
                        f"See {DOCS_URL} and {MD3_SPECS_URL}",
                    )

                    box = nav_tabs.bounding_box()
                    self.assertIsNotNone(box)
                    self.assertAlmostEqual(
                        box["height"],
                        36.0,
                        delta=1.0,
                        msg=f"See {DOCS_URL} and {MD3_SPECS_URL}",
                    )

                    styles = page.evaluate(
                        """() => {
                            const container = document.querySelector('md3-tabs');
                            const inactiveLink = document.querySelector('md3-tabs a:not([aria-current="page"])');
                            const activeLink = document.querySelector('md3-tabs a[aria-current="page"]');
                            const containerCs = window.getComputedStyle(container);
                            const inactiveCs = window.getComputedStyle(inactiveLink);
                            const activeCs = window.getComputedStyle(activeLink);
                            const indicatorCs = window.getComputedStyle(activeLink, '::after');
                            const inactiveIndicatorCs = window.getComputedStyle(inactiveLink, '::after');
                            return {
                                containerBg: containerCs.backgroundColor,
                                borderBottomWidth: containerCs.borderBottomWidth,
                                borderBottomColor: containerCs.borderBottomColor,
                                fontSize: activeCs.fontSize,
                                lineHeight: activeCs.lineHeight,
                                fontWeight: activeCs.fontWeight,
                                activeColor: activeCs.color,
                                inactiveColor: inactiveCs.color,
                                indicatorHeight: indicatorCs.height,
                                indicatorRadius: indicatorCs.borderRadius,
                                indicatorBg: indicatorCs.backgroundColor,
                                inactiveIndicatorContent: inactiveIndicatorCs.content,
                            };
                        }"""
                    )
                    spec_ref = f"See {DOCS_URL} and {MD3_SPECS_URL}"
                    self.assertEqual(styles["containerBg"], "rgb(255, 255, 255)", spec_ref)
                    self.assertEqual(styles["borderBottomWidth"], "1px", spec_ref)
                    self.assertEqual(styles["borderBottomColor"], "rgb(196, 199, 197)", spec_ref)
                    self.assertEqual(styles["fontSize"], "14px", spec_ref)
                    self.assertEqual(styles["lineHeight"], "20px", spec_ref)
                    self.assertEqual(styles["fontWeight"], "500", spec_ref)
                    self.assertEqual(styles["activeColor"], "rgb(11, 87, 208)", spec_ref)
                    self.assertEqual(styles["inactiveColor"], "rgb(68, 71, 70)", spec_ref)
                    self.assertEqual(styles["indicatorHeight"], "3px", spec_ref)
                    self.assertEqual(styles["indicatorRadius"], "3px 3px 0px 0px", spec_ref)
                    self.assertEqual(styles["indicatorBg"], "rgb(11, 87, 208)", spec_ref)
                    self.assertEqual(styles["inactiveIndicatorContent"], "none", spec_ref)

    def test_hierarchy(self):
        files = {
            "conf.py": """
                project = "test_hierarchy"
                extensions = ["md3"]
                html_theme = "md3"
            """,
            "index.rst": """
                ==============
                test_hierarchy
                ==============

                .. toctree::
                   :hidden:

                   guide/index
                   api/index
            """,
            "guide/index.rst": """
                ==========
                User Guide
                ==========

                .. toctree::
                   :hidden:

                   deep_dive
            """,
            "guide/deep_dive.rst": """
                =========
                Deep Dive
                =========
            """,
            "api/index.rst": """
                =============
                API Reference
                =============
            """,
        }
        with build_docs(files) as outdir:
            with DocsServer(outdir) as server:
                with run_playwright() as page:
                    page.goto(server.url_for("guide/deep_dive.html"))

                    tabs = page.locator("md3-tabs a")
                    self.assertEqual(tabs.count(), 3)
                    self.assertEqual(
                        [tabs.nth(i).inner_text().strip() for i in range(3)],
                        ["Home", "User Guide", "API Reference"],
                    )

                    active_tab = page.locator('md3-tabs a[aria-current="page"]')
                    self.assertEqual(active_tab.count(), 1)
                    self.assertEqual(active_tab.inner_text().strip(), "User Guide")

    def test_keyboard(self):
        files = {
            "conf.py": """
                project = "test_keyboard"
                extensions = ["md3"]
                html_theme = "md3"
            """,
            "index.rst": """
                =============
                test_keyboard
                =============

                .. toctree::
                   :hidden:

                   first
                   second
            """,
            "first.rst": """
                =====
                First
                =====
            """,
            "second.rst": """
                ======
                Second
                ======
            """,
        }
        a11y_ref = f"See {DOCS_A11Y_URL} and {MD3_A11Y_URL}"
        with build_docs(files) as outdir:
            with DocsServer(outdir) as server:
                with run_playwright() as page:
                    page.goto(server.url_for("index.html"))

                    tabs = page.locator("md3-tabs a")
                    tabs.nth(0).focus()
                    self.assertEqual(
                        page.evaluate("document.activeElement?.textContent?.trim()"),
                        "Home",
                        a11y_ref,
                    )

                    page.keyboard.press("ArrowRight")
                    self.assertEqual(
                        page.evaluate("document.activeElement?.textContent?.trim()"),
                        "First",
                        a11y_ref,
                    )

                    page.keyboard.press("End")
                    self.assertEqual(
                        page.evaluate("document.activeElement?.textContent?.trim()"),
                        "Second",
                        a11y_ref,
                    )

                    page.keyboard.press("ArrowRight")
                    self.assertEqual(
                        page.evaluate("document.activeElement?.textContent?.trim()"),
                        "Home",
                        a11y_ref,
                    )

                    page.keyboard.press("ArrowLeft")
                    self.assertEqual(
                        page.evaluate("document.activeElement?.textContent?.trim()"),
                        "Second",
                        a11y_ref,
                    )

                    page.keyboard.press("Home")
                    self.assertEqual(
                        page.evaluate("document.activeElement?.textContent?.trim()"),
                        "Home",
                        a11y_ref,
                    )

    def test_no_js(self):
        files = {
            "conf.py": """
                project = "test_no_js"
                extensions = ["md3"]
                html_theme = "md3"
            """,
            "index.rst": """
                ==========
                test_no_js
                ==========

                .. toctree::
                   :hidden:

                   quickstart
            """,
            "quickstart.rst": """
                ==========
                Quickstart
                ==========
            """,
        }
        with build_docs(files) as outdir:
            with DocsServer(outdir) as server:
                with run_playwright(java_script_enabled=False) as page:
                    page.goto(server.url_for("index.html"))

                    quickstart_link = page.locator("md3-tabs a", has_text="Quickstart")
                    self.assertEqual(quickstart_link.count(), 1)
                    quickstart_link.click()

                    self.assertTrue(page.url.endswith("/quickstart.html"))
                    active_tab = page.locator('md3-tabs a[aria-current="page"]')
                    self.assertEqual(active_tab.inner_text().strip(), "Quickstart")

    def test_disabled(self):
        files = {
            "conf.py": """
                project = "test_disabled"
                extensions = ["md3"]
                html_theme = "md3"
                html_theme_options = {"tabs": False}
            """,
            "index.rst": """
                =============
                test_disabled
                =============
            """,
        }
        with build_docs(files) as outdir:
            html = (outdir / "index.html").read_text()
            self.assertNotIn("<md3-tabs>", html)
            self.assertNotIn("md3/tabs.css", html)
            self.assertNotIn("md3/tabs.js", html)

    def test_invalid_option(self):
        files = {
            "conf.py": """
                project = "test_invalid_option"
                extensions = ["md3"]
                html_theme = "md3"
                html_theme_options = {"tabs": "yes"}
            """,
            "index.rst": """
                ===================
                test_invalid_option
                ===================
            """,
        }
        with self.assertRaises(ConfigError):
            with build_docs(files):
                pass

    def test_localization(self):
        files = {
            "conf.py": """
                project = "test_localization"
                extensions = ["md3"]
                html_theme = "md3"
                language = "pt_BR"
            """,
            "index.rst": """
                =================
                test_localization
                =================
            """,
        }
        with build_docs(files) as outdir:
            html = (outdir / "index.html").read_text()
            self.assertIn('aria-label="Navegação de seções"', html)
            self.assertIn('<a href="#" aria-current="page">Início</a>', html)


if __name__ == "__main__":
    unittest.main()
