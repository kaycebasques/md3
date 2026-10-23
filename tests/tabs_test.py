import unittest
from harness import (
    SYS_COLORS,
    SYS_STATE,
    SYS_TYPESCALE,
    DocsServer,
    build_docs,
    run_playwright,
)
from sphinx.errors import ConfigError

DOCS_URL = "components/tabs.html"
DOCS_A11Y_URL = "components/tabs.html#accessibility"
DOCS_DENSITY_URL = "md3.html#density"
DOCS_DEVIATIONS_URL = "md3.html#deviations"
DOCS_TABS_DENSITY_URL = "components/tabs.html#density"
MD3_SPECS_URL = "https://m3.material.io/components/tabs/specs#8602158e-a13b-432e-8133-b9cb34d61678"
MD3_DENSITY_URL = "https://m3.material.io/foundations/layout/grids-spacing/density"
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
        spec_ref = f"See {DOCS_URL} and {MD3_SPECS_URL}"
        density_ref = (
            f"See {DOCS_DENSITY_URL}, {DOCS_DEVIATIONS_URL}, "
            f"{DOCS_TABS_DENSITY_URL}, {MD3_SPECS_URL}, and {MD3_DENSITY_URL}"
        )
        with build_docs(files) as outdir:
            with DocsServer(outdir) as server:
                with run_playwright() as page:
                    page.goto(server.url_for("index.html"))

                    self.assertTrue(
                        page.evaluate("Boolean(customElements.get('md3-tabs'))"),
                        spec_ref,
                    )

                    nav_tabs = page.locator("md3-tabs")
                    self.assertEqual(
                        nav_tabs.count(),
                        1,
                        spec_ref,
                    )

                    box = nav_tabs.bounding_box()
                    self.assertIsNotNone(box)
                    self.assertAlmostEqual(
                        box["height"],
                        36.0,
                        delta=1.0,
                        msg=density_ref,
                    )

                    styles = page.evaluate(
                        """() => {
                            const container = document.querySelector('md3-tabs');
                            const nav = document.querySelector('md3-tabs nav');
                            const list = document.querySelector('md3-tabs ul');
                            const inactiveLink = document.querySelector('md3-tabs a:not([aria-current="page"])');
                            const activeLink = document.querySelector('md3-tabs a[aria-current="page"]');
                            const containerCs = window.getComputedStyle(container);
                            const navCs = window.getComputedStyle(nav);
                            const listCs = window.getComputedStyle(list);
                            const inactiveCs = window.getComputedStyle(inactiveLink);
                            const activeCs = window.getComputedStyle(activeLink);
                            const indicatorCs = window.getComputedStyle(activeLink, '::after');
                            const inactiveIndicatorCs = window.getComputedStyle(inactiveLink, '::after');
                            return {
                                containerBg: containerCs.backgroundColor,
                                borderBottomWidth: containerCs.borderBottomWidth,
                                borderBottomColor: containerCs.borderBottomColor,
                                navPaddingLeft: navCs.paddingLeft,
                                navPaddingRight: navCs.paddingRight,
                                listGap: listCs.gap,
                                linkPaddingLeft: activeCs.paddingLeft,
                                linkPaddingRight: activeCs.paddingRight,
                                fontFamily: activeCs.fontFamily,
                                fontSize: activeCs.fontSize,
                                lineHeight: activeCs.lineHeight,
                                fontWeight: activeCs.fontWeight,
                                letterSpacing: activeCs.letterSpacing,
                                activeColor: activeCs.color,
                                inactiveColor: inactiveCs.color,
                                indicatorMinWidth: indicatorCs.minWidth,
                                indicatorHeight: indicatorCs.height,
                                indicatorRadius: indicatorCs.borderRadius,
                                indicatorBg: indicatorCs.backgroundColor,
                                inactiveIndicatorContent: inactiveIndicatorCs.content,
                            };
                        }"""
                    )
                    title_small = SYS_TYPESCALE["title-small"]
                    self.assertEqual(styles["containerBg"], SYS_COLORS["surface"], spec_ref)
                    self.assertEqual(styles["borderBottomWidth"], "1px", spec_ref)
                    self.assertEqual(styles["borderBottomColor"], SYS_COLORS["outline-variant"], spec_ref)
                    self.assertEqual(styles["navPaddingLeft"], "16px", spec_ref)
                    self.assertEqual(styles["navPaddingRight"], "16px", spec_ref)
                    self.assertEqual(styles["listGap"], "4px", spec_ref)
                    self.assertEqual(styles["linkPaddingLeft"], "16px", spec_ref)
                    self.assertEqual(styles["linkPaddingRight"], "16px", spec_ref)
                    self.assertEqual(styles["fontFamily"], title_small["fontFamily"], spec_ref)
                    self.assertEqual(styles["fontSize"], title_small["fontSize"], spec_ref)
                    self.assertEqual(styles["lineHeight"], title_small["lineHeight"], spec_ref)
                    self.assertEqual(styles["fontWeight"], title_small["fontWeight"], spec_ref)
                    self.assertEqual(styles["letterSpacing"], title_small["letterSpacing"], spec_ref)
                    self.assertEqual(styles["activeColor"], SYS_COLORS["primary"], spec_ref)
                    self.assertEqual(styles["inactiveColor"], SYS_COLORS["on-surface-variant"], spec_ref)
                    self.assertEqual(styles["indicatorMinWidth"], "24px", spec_ref)
                    self.assertEqual(styles["indicatorHeight"], "3px", spec_ref)
                    self.assertEqual(styles["indicatorRadius"], "3px 3px 0px 0px", spec_ref)
                    self.assertEqual(styles["indicatorBg"], SYS_COLORS["primary"], spec_ref)
                    self.assertEqual(styles["inactiveIndicatorContent"], "none", spec_ref)

                    active_link = page.locator('md3-tabs a[aria-current="page"]')
                    inactive_link = page.locator('md3-tabs a:not([aria-current="page"])')

                    inactive_link.hover()
                    inactive_hover = page.evaluate(
                        """() => {
                            const cs = window.getComputedStyle(
                                document.querySelector('md3-tabs a:not([aria-current="page"])')
                            );
                            return { bg: cs.backgroundColor, color: cs.color };
                        }"""
                    )
                    self.assertEqual(inactive_hover["bg"], SYS_STATE["hover"]["on-surface"], spec_ref)
                    self.assertEqual(inactive_hover["color"], SYS_COLORS["on-surface"], spec_ref)

                    page.mouse.down()
                    inactive_active = page.evaluate(
                        """() => {
                            const cs = window.getComputedStyle(
                                document.querySelector('md3-tabs a:not([aria-current="page"])')
                            );
                            return { bg: cs.backgroundColor, color: cs.color };
                        }"""
                    )
                    page.mouse.up()
                    self.assertEqual(inactive_active["bg"], SYS_STATE["pressed"]["on-surface"], spec_ref)
                    self.assertEqual(inactive_active["color"], SYS_COLORS["on-surface"], spec_ref)

                    active_link.hover()
                    active_hover = page.evaluate(
                        """() => {
                            const cs = window.getComputedStyle(
                                document.querySelector('md3-tabs a[aria-current="page"]')
                            );
                            return { bg: cs.backgroundColor, color: cs.color };
                        }"""
                    )
                    self.assertEqual(active_hover["bg"], SYS_STATE["hover"]["primary"], spec_ref)
                    self.assertEqual(active_hover["color"], SYS_COLORS["primary"], spec_ref)

                    page.mouse.down()
                    active_active = page.evaluate(
                        """() => {
                            const cs = window.getComputedStyle(
                                document.querySelector('md3-tabs a[aria-current="page"]')
                            );
                            return { bg: cs.backgroundColor, color: cs.color };
                        }"""
                    )
                    page.mouse.up()
                    self.assertEqual(active_active["bg"], SYS_STATE["pressed"]["primary"], spec_ref)
                    self.assertEqual(active_active["color"], SYS_COLORS["primary"], spec_ref)

                    active_link.focus()
                    page.keyboard.press("ArrowRight")
                    focus_styles = page.evaluate(
                        """() => {
                            const cs = window.getComputedStyle(document.activeElement);
                            return {
                                outlineWidth: cs.outlineWidth,
                                outlineStyle: cs.outlineStyle,
                                outlineColor: cs.outlineColor,
                                outlineOffset: cs.outlineOffset,
                            };
                        }"""
                    )
                    self.assertEqual(focus_styles["outlineWidth"], SYS_STATE["focus-indicator-thickness"], spec_ref)
                    self.assertEqual(focus_styles["outlineStyle"], "solid", spec_ref)
                    self.assertEqual(focus_styles["outlineColor"], SYS_COLORS["secondary"], spec_ref)
                    self.assertEqual(focus_styles["outlineOffset"], f"-{SYS_STATE['focus-indicator-thickness']}", spec_ref)

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

    def test_density(self):
        density_ref = (
            f"See {DOCS_DENSITY_URL}, {DOCS_TABS_DENSITY_URL}, "
            f"{MD3_SPECS_URL}, and {MD3_DENSITY_URL}"
        )
        with run_playwright() as page:
            for scale, expected_height in ((-3, 36.0), (-2, 40.0), (-1, 44.0), (0, 48.0)):
                files = {
                    "conf.py": f"""
                        project = "test_density"
                        extensions = ["md3"]
                        html_theme = "md3"
                        html_theme_options = {{"density": {scale}}}
                    """,
                    "index.rst": """
                        ============
                        test_density
                        ============
                    """,
                }
                with build_docs(files) as outdir:
                    with DocsServer(outdir) as server:
                        page.goto(server.url_for("index.html"))
                        box = page.locator("md3-tabs").bounding_box()
                        self.assertIsNotNone(box)
                        self.assertAlmostEqual(
                            box["height"],
                            expected_height,
                            delta=1.0,
                            msg=density_ref,
                        )

    def test_invalid_option(self):
        for options in (
            '{"tabs": "yes"}',
            '{"density": -4}',
            '{"density": 1}',
            '{"density": True}',
            '{"density": "compact"}',
        ):
            files = {
                "conf.py": f"""
                    project = "test_invalid_option"
                    extensions = ["md3"]
                    html_theme = "md3"
                    html_theme_options = {options}
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
