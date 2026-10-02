import unittest
from harness import SphinxTestBase


class TestMd3ProgressiveEnhancement(SphinxTestBase):
    """Verifies progressive enhancement and no-JavaScript fallback capabilities:
    1. Mobile viewport access to 'On this page' table of contents.
    2. Mobile navigation drawer opening and closing without JavaScript.
    3. Light/Dark theme switching without JavaScript via CSS :has().
    4. Jinja layout Light DOM rendering of content.
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        conf_content = """
            project = "ProgressiveEnhancementTest"
            extensions = ["md3"]
            html_theme = "md3"
        """
        index_content = """
            ==============================
            Progressive Enhancement Guide
            ==============================

            Section One
            ===========

            Content for section one.

            .. raw:: html

               <div style="height: 800px;">Spacer one</div>

            Section Two
            ===========

            Content for section two with detailed explanations.

            .. raw:: html

               <div style="height: 800px;">Spacer two</div>

            Section Three
            =============

            Content for section three with additional information.
        """
        outdir = cls.build_docs(conf_content, index_content, outdir_name="prog_enh_out")
        cls.url = cls.start_server(outdir)

    def test_mobile_viewport_on_this_page_access_without_js(self):
        """Verifies that on mobile viewports without JS, 'On this page' links are accessible via Popover (mouse and keyboard)."""
        for width in [480, 768, 1024]:
            with self.run_playwright(
                viewport={"width": width, "height": 800},
                java_script_enabled=False,
            ) as page:
                page.goto(f"{self.url}/index.html")

                # Desktop column 3 TOC must be hidden below 1200px
                desktop_toc = page.locator("md3-toc#md3-toc")
                self.assertFalse(desktop_toc.is_visible())

                # Mobile TOC trigger button must be visible
                mobile_btn = page.locator("#toc-mobile-btn")
                self.assertTrue(mobile_btn.is_visible())

                # Mobile TOC menu should be closed initially
                mobile_menu = page.locator("#md3-toc-mobile-menu")
                self.assertFalse(mobile_menu.is_visible())

                # Activate mobile TOC button via keyboard (Enter) without JS
                mobile_btn.focus()
                page.keyboard.press("Enter")
                self.assertTrue(mobile_menu.is_visible())

                # Dismiss via Escape key without JS
                page.keyboard.press("Escape")
                self.assertFalse(mobile_menu.is_visible())

                # Click mobile TOC button to open popover natively without JS
                mobile_btn.click()
                self.assertTrue(mobile_menu.is_visible())

                # Verify 'On this page' headings exist in Light DOM
                links = mobile_menu.locator("a")
                self.assertGreaterEqual(links.count(), 3)
                link_texts = [links.nth(i).inner_text().strip().lower() for i in range(links.count())]
                self.assertTrue(any("section one" in t for t in link_texts))
                self.assertTrue(any("section two" in t for t in link_texts))
                self.assertTrue(any("section three" in t for t in link_texts))

                # Click a section link to jump to anchor
                sec2_link = mobile_menu.locator('a[href*="section-two"]')
                sec2_link.click()
                self.assertIn("section-two", page.url)

    def test_mobile_viewport_on_this_page_access_with_js_progressive_enhancement(self):
        """Verifies that with JS enabled, clicking a TOC link automatically dismisses the popover."""
        with self.run_playwright(
            viewport={"width": 480, "height": 800},
            java_script_enabled=True,
        ) as page:
            page.goto(f"{self.url}/index.html")

            mobile_btn = page.locator("#toc-mobile-btn")
            mobile_menu = page.locator("#md3-toc-mobile-menu")

            mobile_btn.click()
            self.assertTrue(mobile_menu.is_visible())

            # Clicking a link inside popover should automatically close it
            sec2_link = mobile_menu.locator('a[href*="section-two"]')
            sec2_link.click()
            self.assertFalse(mobile_menu.is_visible())
            self.assertIn("section-two", page.url)

    def test_desktop_viewport_hides_mobile_toc_button_and_back_to_top_works_without_js(self):
        """Verifies that on desktop (>=1200px), mobile TOC button is hidden, desktop TOC is shown, and Back to top works without JS."""
        for width in [1200, 1440]:
            with self.run_playwright(
                viewport={"width": width, "height": 800},
                java_script_enabled=False,
            ) as page:
                page.goto(f"{self.url}/index.html")

                mobile_btn = page.locator("#toc-mobile-btn")
                desktop_toc = page.locator("md3-toc#md3-toc")
                back_to_top = page.locator("#back-to-top")

                self.assertFalse(mobile_btn.is_visible())
                self.assertTrue(desktop_toc.is_visible())
                self.assertTrue(back_to_top.is_visible())

                # Click section three in desktop TOC to scroll down without JS
                desktop_toc.locator('a[href*="section-three"]').click()
                page.wait_for_timeout(700)
                scroll_before = page.evaluate("window.scrollY")
                self.assertGreater(scroll_before, 500)

                # Activate #back-to-top via keyboard (Enter) without JS and verify it scrolls back to top
                back_to_top.focus()
                page.keyboard.press("Enter")
                page.wait_for_timeout(800)
                self.assertTrue(page.url.endswith("#body"))
                scroll_after = page.evaluate("window.scrollY")
                self.assertEqual(scroll_after, 0)

    def test_mobile_navigation_drawer_open_and_close_without_js(self):
        """Verifies that navigation drawer opens and closes on mobile without JavaScript via both mouse and keyboard."""
        with self.run_playwright(
            viewport={"width": 480, "height": 800},
            java_script_enabled=False,
        ) as page:
            page.goto(f"{self.url}/index.html")

            drawer_toggle = page.locator("#drawer-toggle")
            sidebar = page.locator("md3-sidebar#md3-sidebar")
            backdrop = page.locator("#md3-backdrop")
            close_btn = page.locator("#sidebar-close")

            self.assertTrue(drawer_toggle.is_visible())

            # Verify sidebar is initially offscreen
            sidebar_box = sidebar.bounding_box()
            self.assertIsNotNone(sidebar_box)
            self.assertLess(sidebar_box["x"] + sidebar_box["width"], 10.0)

            # 1. Open drawer via keyboard (Enter on #drawer-toggle) without JS
            drawer_toggle.focus()
            page.keyboard.press("Enter")
            page.wait_for_timeout(450)

            open_box = sidebar.bounding_box()
            self.assertIsNotNone(open_box)
            self.assertAlmostEqual(open_box["x"], 0.0, delta=2.0)
            self.assertAlmostEqual(open_box["width"], 260.0, delta=20.0)

            # Verify navigation links are visible in Light DOM
            nav_links = sidebar.locator("a")
            self.assertGreaterEqual(nav_links.count(), 1)

            # 2. Close drawer via keyboard (Space on #sidebar-close) without JS
            close_btn.focus()
            page.keyboard.press("Space")
            page.wait_for_timeout(450)
            closed_box = sidebar.bounding_box()
            self.assertIsNotNone(closed_box)
            self.assertLess(closed_box["x"] + closed_box["width"], 10.0)

            # 3. Re-open via click and close via backdrop click at exposed viewport coordinates (x=300, y=200)
            drawer_toggle.click()
            page.wait_for_timeout(450)
            reopened_box = sidebar.bounding_box()
            self.assertAlmostEqual(reopened_box["x"], 0.0, delta=2.0)

            backdrop_box = backdrop.bounding_box()
            self.assertIsNotNone(backdrop_box)
            self.assertEqual(backdrop_box["x"], 0)
            self.assertEqual(backdrop_box["y"], 0)
            self.assertEqual(backdrop_box["width"], 480)
            self.assertEqual(backdrop_box["height"], 800)

            backdrop.click(position={"x": 300, "y": 200})
            page.wait_for_timeout(450)
            final_box = sidebar.bounding_box()
            self.assertLess(final_box["x"] + final_box["width"], 10.0)

    def test_theme_switching_without_js(self):
        """Verifies that theme switching works without JavaScript via Popover and CSS :has() (mouse and keyboard)."""
        with self.run_playwright(
            viewport={"width": 480, "height": 800},
            java_script_enabled=False,
        ) as page:
            page.goto(f"{self.url}/index.html")

            # Initial state without JS (default light)
            theme_btn = page.locator("#theme-menu-btn")
            theme_menu = page.locator("#md3-theme-menu")
            self.assertTrue(theme_btn.is_visible())
            self.assertFalse(theme_menu.is_visible())

            # Activate theme button via keyboard (Enter) to open menu via HTML popovertarget
            theme_btn.focus()
            page.keyboard.press("Enter")
            self.assertTrue(theme_menu.is_visible())

            # Select dark mode radio button without JS
            dark_radio = theme_menu.locator('input[value="dark"]')
            dark_radio.check()

            # Verify that CSS :root.no-js:has(#md3-theme-menu input[value="dark"]:checked) updates tokens
            dark_primary = page.locator("body").evaluate(
                "el => window.getComputedStyle(el).getPropertyValue('--md-sys-color-primary').trim()"
            )
            self.assertEqual(dark_primary, "#a8c7fa")

            # Select light mode radio button without JS
            light_radio = theme_menu.locator('input[value="light"]')
            light_radio.check()

            light_primary = page.locator("body").evaluate(
                "el => window.getComputedStyle(el).getPropertyValue('--md-sys-color-primary').trim()"
            )
            self.assertEqual(light_primary, "#0b57d0")

    def test_light_dom_jinja_rendering_and_clean_aria_hierarchy(self):
        """Verifies Light DOM rendering, absence of nested interactive controls, and clean keyboard tab order."""
        with self.run_playwright(java_script_enabled=False) as page:
            page.goto(f"{self.url}/index.html")

            # Check that elements exist directly in the DOM without requiring JS execution
            self.assertGreater(page.locator("md3-sidebar nav a").count(), 0)
            self.assertGreater(page.locator("#md3-toc-mobile-menu a").count(), 0)
            self.assertEqual(page.locator('#md3-theme-menu input[name="theme"]').count(), 2)
            self.assertGreater(page.locator(".md3-breadcrumbs a").count(), 0)

            # Ensure no <button> is nested inside an element with role="button"
            self.assertEqual(page.locator('[role="button"] button').count(), 0)

            # Ensure no aria-hidden="true" input/button is in the keyboard tab order
            self.assertEqual(page.locator('input[aria-hidden="true"], button[aria-hidden="true"]').count(), 0)


if __name__ == "__main__":
    unittest.main()
