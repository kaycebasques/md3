import unittest
from harness import SphinxTestBase, md3_conformance


class TestMd3Accessibility(SphinxTestBase):
    """Verifies compliance with Material Design 3 Accessibility and Interaction specifications."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        conf_content = """
            project = "AccessibilityTest"
            extensions = ["md3"]
            html_theme = "md3"
        """
        index_content = """
            ==================
            Accessibility Test
            ==================

            .. toctree::
               :maxdepth: 2

               subpage_a

            Section Alpha
            =============

            Sample paragraph.

            .. raw:: html

               <div id="test-buttons">
                 <button class="md3-btn md3-btn--filled" id="acc-filled-btn">Filled Action</button>
                 <button class="md3-icon-btn" id="acc-icon-btn" aria-label="Settings Action" title="Settings Action">
                   <svg class="md3-icon" viewBox="0 0 24 24" width="20" height="20">
                     <path d="M19.14 12.94c.04-.3.06-.61.06-.94 0-.32-.02-.64-.07-.94l2.03-1.58c.18-.14.23-.41.12-.61l-1.92-3.32c-.12-.22-.37-.29-.59-.22l-2.39.96c-.5-.38-1.03-.7-1.62-.94l-.36-2.54c-.04-.24-.24-.41-.48-.41h-3.84c-.24 0-.43.17-.47.41l-.36 2.54c-.59.24-1.13.57-1.62.94l-2.39-.96c-.22-.08-.47 0-.59.22L2.74 8.87c-.12.21-.08.47.12.61l2.03 1.58c-.05.3-.09.63-.09.94s.02.64.07.94l-2.03 1.58c-.18.14-.23.41-.12.61l1.92 3.32c.12.22.37.29.59.22l2.39-.96c.5.38 1.03.7 1.62.94l.36 2.54c.05.24.24.41.48.41h3.84c.24 0 .44-.17.47-.41l.36-2.54c.59-.24 1.13-.56 1.62-.94l2.39.96c.22.08.47 0 .59-.22l1.92-3.32c.12-.22.07-.47-.12-.61l-2.01-1.58zM12 15.6c-1.98 0-3.6-1.62-3.6-3.6s1.62-3.6 3.6-3.6 3.6 1.62 3.6 3.6-1.62 3.6-3.6 3.6z"/>
                   </svg>
                 </button>
               </div>
        """
        extra = {
            "subpage_a.rst": """
                =========
                Subpage A
                =========
                Subpage text.
            """
        }
        outdir = cls.build_docs(
            conf_content,
            index_content,
            extra_files=extra,
            outdir_name="accessibility_out",
        )
        cls.url = cls.start_server(outdir)

    @md3_conformance(spec_key="ACCESSIBILITY_FOCUS_RING")
    def test_focus_visible_indicator_styling(self):
        """Verifies that interactive elements specify high-contrast focus rings for keyboard navigation."""
        with self.run_playwright() as page:
            page.goto(f"{self.url}/index.html")

            focus_styles = page.evaluate(
                """() => {
                    const btn = document.getElementById('acc-filled-btn');
                    btn.focus();
                    const rootCs = window.getComputedStyle(document.documentElement);
                    return {
                        focusThickness: rootCs.getPropertyValue('--md-sys-state-focus-indicator-thickness').trim(),
                        focusOuterOffset: rootCs.getPropertyValue('--md-sys-state-focus-indicator-outer-offset').trim(),
                        focusInnerOffset: rootCs.getPropertyValue('--md-sys-state-focus-indicator-inner-offset').trim(),
                        secondaryColor: rootCs.getPropertyValue('--md-sys-color-secondary').trim(),
                    };
                }"""
            )
            self.assertEqual(focus_styles["focusThickness"], "3px")
            self.assertEqual(focus_styles["focusOuterOffset"], "2px")
            self.assertEqual(focus_styles["focusInnerOffset"], "-3px")
            self.assertTrue(focus_styles["secondaryColor"].startswith("#"))

    @md3_conformance(spec_key="STATE_LAYERS")
    def test_button_hover_state_elevation_and_transition(self):
        """Verifies that hovering over buttons updates elevation or background per MD3 state guidelines."""
        with self.run_playwright() as page:
            page.goto(f"{self.url}/index.html")

            btn = page.locator("#acc-filled-btn")
            box_before = page.evaluate(
                """() => {
                    const el = document.getElementById('acc-filled-btn');
                    return window.getComputedStyle(el).boxShadow;
                }"""
            )
            btn.hover()
            page.wait_for_timeout(100)
            box_after = page.evaluate(
                """() => {
                    const el = document.getElementById('acc-filled-btn');
                    return window.getComputedStyle(el).boxShadow;
                }"""
            )
            self.assertNotEqual(box_before, box_after)
            self.assertIn("rgba", box_after)

    def test_aria_landmarks_and_semantics(self):
        """Verifies standard landmark roles, accessibility labels, and icon button tooltips."""
        with self.run_playwright() as page:
            page.goto(f"{self.url}/index.html")

            with self.spec_context(spec_key="ACCESSIBILITY_WEB_LANDMARKS"):
                self.assertEqual(page.locator("header[role='banner'], md3-top-app-bar[role='banner']").count(), 1)
                self.assertEqual(page.locator("md3-sidebar[role='navigation']").count(), 1)
                self.assertEqual(page.locator("main[role='main']").count(), 1)
                self.assertEqual(page.locator("md3-toc[role='complementary']").count(), 1)
                self.assertEqual(page.locator("footer[role='contentinfo']").count(), 1)

                # Multiple navigation/landmark regions have distinct aria-labels
                self.assertEqual(
                    page.locator("md3-sidebar").get_attribute("aria-label"),
                    "Documentation navigation",
                )
                self.assertEqual(
                    page.locator(".md3-breadcrumbs").get_attribute("aria-label"),
                    "Breadcrumb",
                )
                self.assertEqual(
                    page.locator("md3-toc").get_attribute("aria-label"),
                    "On this page",
                )

            with self.spec_context(spec_key="ACCESSIBILITY_ARIA_SEMANTICS"):
                drawer_toggle = page.locator("#drawer-toggle")
                self.assertEqual(drawer_toggle.get_attribute("aria-label"), "Toggle navigation drawer")
                self.assertEqual(drawer_toggle.get_attribute("aria-controls"), "md3-sidebar")
                self.assertEqual(drawer_toggle.get_attribute("aria-expanded"), "false")
                # Labels must not include the element role name "button"
                self.assertNotIn("button", (drawer_toggle.get_attribute("aria-label") or "").lower())

                theme_toggle = page.locator("#theme-menu-btn")
                self.assertIsNone(page.locator("md3-theme-toggle").get_attribute("role"))
                self.assertEqual(theme_toggle.get_attribute("aria-label"), "Toggle color theme")
                self.assertNotIn("button", (theme_toggle.get_attribute("aria-label") or "").lower())
                self.assertIn(theme_toggle.get_attribute("aria-pressed"), ["false", "true"])

            with self.spec_context(spec_key="COMPONENTS_ICON_BUTTON_TOOLTIP"):
                for selector, expected_tooltip in [
                    ("#drawer-toggle", "Toggle navigation drawer"),
                    ("#theme-menu-btn", "Toggle color theme"),
                    ("#md3-search-close", "Close search"),
                ]:
                    el = page.locator(selector)
                    self.assertEqual(el.get_attribute("title"), expected_tooltip)

    @md3_conformance(spec_key="COMPONENTS_THEME_TOGGLE")
    def test_keyboard_activation_of_theme_toggle(self):
        """Verifies that pressing Space or Enter on the theme toggle button activates theme switching."""
        with self.run_playwright() as page:
            page.goto(f"{self.url}/index.html")

            initial_theme = page.evaluate("document.documentElement.dataset.theme")
            toggle = page.locator("#theme-menu-btn")
            toggle.focus()
            page.keyboard.press("Enter")
            switched_theme = page.evaluate("document.documentElement.dataset.theme")
            self.assertNotEqual(initial_theme, switched_theme)

            page.keyboard.press("Space")
            reverted_theme = page.evaluate("document.documentElement.dataset.theme")
            self.assertEqual(initial_theme, reverted_theme)


if __name__ == "__main__":
    unittest.main()
