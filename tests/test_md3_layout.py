import unittest
from harness import SphinxTestBase, md3_conformance


class TestMd3LayoutConformance(SphinxTestBase):
    """Verifies compliance with MD3 responsive window size classes and 3-pane documentation scaffold."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        conf_content = """
            project = "LayoutTest"
            extensions = ["md3"]
            html_theme = "md3"
        """
        index_content = """
            ===========
            Layout Test
            ===========

            Section One
            ===========

            Content for section one.

            Section Two
            ===========

            Content for section two.
        """
        outdir = cls.build_docs(conf_content, index_content, outdir_name="layout_out")
        cls.url = cls.start_server(outdir)

    @md3_conformance(spec_key="LAYOUT_SCAFFOLD")
    def test_three_column_desktop_layout(self):
        """Verifies that all 3 panes exist side-by-side in Large (>=1200px) and Extra-Large (>=1600px) window size classes."""
        for width in [1200, 1280, 1600]:
            with self.run_playwright(viewport={"width": width, "height": 800}) as page:
                page.goto(f"{self.url}/index.html")

                # Column 1: Left Navigation Sidebar (<md3-sidebar>)
                sidebar = page.locator("md3-sidebar#md3-sidebar")
                self.assertTrue(sidebar.is_visible())
                sidebar_box = sidebar.bounding_box()
                self.assertIsNotNone(sidebar_box)
                self.assertAlmostEqual(sidebar_box["width"], 260.0, delta=2.0)

                # Column 2: Center Main Content (<main>)
                main = page.locator("#main")
                self.assertTrue(main.is_visible())
                main_box = main.bounding_box()
                self.assertIsNotNone(main_box)
                self.assertGreaterEqual(main_box["x"], sidebar_box["x"] + sidebar_box["width"] - 2)

                # Column 3: Right On-Page Table of Contents (<md3-toc>)
                toc = page.locator("md3-toc#md3-toc")
                self.assertTrue(toc.is_visible())
                toc_box = toc.bounding_box()
                self.assertIsNotNone(toc_box)
                self.assertGreater(toc_box["x"], main_box["x"])
                self.assertGreaterEqual(toc_box["width"], 180.0)

                # Check "On this page" text in column 3
                self.assertIn("on this page", toc.inner_text().lower())

    def test_tablet_responsive_layout_collapses_toc(self):
        """Verifies Expanded window size class (840px–1199px) displays 2 panes (sidebar + main) and hides TOC."""
        for width in [840, 1024, 1199]:
            with self.run_playwright(viewport={"width": width, "height": 800}) as page:
                page.goto(f"{self.url}/index.html")

                sidebar = page.locator("md3-sidebar#md3-sidebar")
                main = page.locator("#main")
                toc = page.locator("md3-toc#md3-toc")
                drawer_toggle = page.locator("#drawer-toggle")

                with self.spec_context(spec_key="LAYOUT_TWO_PANE_EXPANDED"):
                    self.assertTrue(sidebar.is_visible())
                    self.assertTrue(main.is_visible())
                    self.assertFalse(toc.is_visible())

                with self.spec_context(spec_key="LAYOUT_BREAKPOINTS"):
                    self.assertFalse(drawer_toggle.is_visible())

    def test_mobile_responsive_drawer_interaction(self):
        """Verifies Compact (<600px) and Medium (600px–839px) viewports use a modal navigation drawer with scrim and focus restoration."""
        for width in [480, 768]:
            with self.run_playwright(viewport={"width": width, "height": 800}) as page:
                page.goto(f"{self.url}/index.html")

                drawer_toggle = page.locator("#drawer-toggle")
                sidebar = page.locator("md3-sidebar#md3-sidebar")
                backdrop = page.locator("#md3-backdrop")

                with self.spec_context(spec_key="LAYOUT_MODAL_DRAWER"):
                    self.assertTrue(drawer_toggle.is_visible())
                    self.assertNotIn("open", sidebar.get_attribute("class") or "")
                    self.assertEqual(drawer_toggle.get_attribute("aria-expanded"), "false")

                    # Verify modal drawer right corners are 16px (corner-large) and scrim opacity is 0.32
                    drawer_styles = page.evaluate(
                        """() => {
                            const cs = window.getComputedStyle(document.getElementById('md3-sidebar'));
                            const beforeCs = window.getComputedStyle(document.getElementById('md3-backdrop'), '::before');
                            return {
                                topRightRadius: cs.borderTopRightRadius,
                                bottomRightRadius: cs.borderBottomRightRadius,
                                scrimOpacity: parseFloat(beforeCs.opacity),
                            };
                        }"""
                    )
                    self.assertEqual(drawer_styles["topRightRadius"], "16px")
                    self.assertEqual(drawer_styles["bottomRightRadius"], "16px")
                    self.assertAlmostEqual(drawer_styles["scrimOpacity"], 0.32, delta=0.01)

                    # Click hamburger to open drawer
                    drawer_toggle.focus()
                    drawer_toggle.click()
                    self.assertIn("open", sidebar.get_attribute("class") or "")
                    self.assertIn("open", backdrop.get_attribute("class") or "")
                    self.assertEqual(drawer_toggle.get_attribute("aria-expanded"), "true")

                with self.spec_context(spec_key="LAYOUT_DRAWER_DISMISS"):
                    # Click backdrop to close drawer and verify focus returns to drawer-toggle
                    backdrop.click()
                    self.assertNotIn("open", sidebar.get_attribute("class") or "")
                    self.assertNotIn("open", backdrop.get_attribute("class") or "")
                    self.assertEqual(drawer_toggle.get_attribute("aria-expanded"), "false")
                    active_id = page.evaluate("document.activeElement?.id")
                    self.assertEqual(active_id, "drawer-toggle")

                    # Re-open drawer and press Escape to close drawer and verify focus returns
                    drawer_toggle.focus()
                    drawer_toggle.click()
                    self.assertIn("open", sidebar.get_attribute("class") or "")
                    page.keyboard.press("Escape")
                    self.assertNotIn("open", sidebar.get_attribute("class") or "")
                    active_id_after_esc = page.evaluate("document.activeElement?.id")
                    self.assertEqual(active_id_after_esc, "drawer-toggle")


if __name__ == "__main__":
    unittest.main()
