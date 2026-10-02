import unittest
from harness import SphinxTestBase, md3_conformance


class TestMd3Components(SphinxTestBase):
    """Verifies interactive MD3 web components and runtime behavior."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        conf_content = """
            project = "ComponentsTest"
            extensions = ["md3"]
            html_theme = "md3"
        """
        index_content = """
            ===============
            Components Page
            ===============

            .. toctree::
               :maxdepth: 1

               remote_guide

            Section 1
            =========

            Code snippet to test copy button:

            .. code-block:: python

               def greet(name: str) -> str:
                   return f"Hello {name}"

            Section 2
            =========

            UniqueSearchableTokenXYZ in section two.

            .. raw:: html

               <div style="height: 1400px;">Tall spacer for scroll testing</div>
        """
        extra_files = {
            "remote_guide.rst": """
                ===================
                Remote Guide Manual
                ===================

                Remote Architecture Section
                ===========================

                CrossPageSearchTokenPagefind789 describes full-site indexing across documents.
            """,
        }
        outdir = cls.build_docs(
            conf_content,
            index_content,
            extra_files=extra_files,
            outdir_name="components_out",
        )
        cls.url = cls.start_server(outdir)

    @md3_conformance(spec_key="COMPONENTS_CUSTOM_ELEMENTS")
    def test_custom_elements_registered_and_rendered_in_dom(self):
        """Verifies that all MD3 web components are registered in customElements and rendered in DOM."""
        with self.run_playwright() as page:
            page.goto(f"{self.url}/index.html")

            registered_tags = [
                "paz-app",
                "md3-app",
                "md3-theme-toggle",
                "md3-top-app-bar",
                "md3-nav-tabs",
                "md3-sidebar",
                "md3-toc",
                "md3-search",
                "md3-copy-button",
            ]
            for tag in registered_tags:
                defined = page.evaluate(f"Boolean(customElements.get('{tag}'))")
                self.assertTrue(
                    defined,
                    f"Custom element <{tag}> should be defined in customElements registry",
                )

            rendered_tags = [
                "paz-app",
                "md3-top-app-bar",
                "md3-theme-toggle",
                "md3-sidebar",
                "md3-toc",
                "md3-search",
                "md3-copy-button",
            ]
            for tag in rendered_tags:
                count = page.locator(tag).count()
                self.assertGreaterEqual(
                    count,
                    1,
                    f"Custom element <{tag}> must be rendered in the page DOM",
                )

    def test_top_app_bar_resting_vs_scrolled_elevation_and_color(self):
        """Verifies <md3-top-app-bar> uses surface & Level 0 at rest, and surface-container & Level 2 on scroll."""
        with self.run_playwright() as page:
            page.goto(f"{self.url}/index.html")
            page.evaluate("document.documentElement.dataset.theme = 'light'; window.scrollTo(0, 0);")
            page.wait_for_timeout(50)

            resting = page.evaluate(
                """() => {
                    const bar = document.querySelector('md3-top-app-bar');
                    const cs = window.getComputedStyle(bar);
                    return {
                        scrolled: bar.dataset.scrolled,
                        bg: cs.backgroundColor,
                        shadow: cs.boxShadow,
                    };
                }"""
            )
            with self.spec_context(spec_key="COMPONENTS_TOP_APP_BAR_SCROLL"):
                self.assertEqual(resting["scrolled"], "false")
                self.assertEqual(resting["bg"], "rgb(255, 255, 255)")
                self.assertEqual(resting["shadow"], "none")

            page.evaluate(
                """() => {
                    const bar = document.querySelector('md3-top-app-bar');
                    bar.style.transition = 'none';
                    window.scrollTo({ top: 200, behavior: 'instant' });
                    window.dispatchEvent(new Event('scroll'));
                }"""
            )
            scrolled = page.evaluate(
                """() => {
                    const bar = document.querySelector('md3-top-app-bar');
                    const cs = window.getComputedStyle(bar);
                    return {
                        scrolled: bar.dataset.scrolled,
                        hasClass: bar.classList.contains('scrolled'),
                        bg: cs.backgroundColor,
                        shadow: cs.boxShadow,
                    };
                }"""
            )
            with self.spec_context(spec_key="COMPONENTS_TOP_APP_BAR_SCROLL"):
                self.assertEqual(scrolled["scrolled"], "true")
                self.assertTrue(scrolled["hasClass"])
                # surface-container in light mode is #f0f4f9 -> rgb(240, 244, 249)
                self.assertEqual(scrolled["bg"], "rgb(240, 244, 249)")
                self.assertNotEqual(scrolled["shadow"], "none")

    def test_theme_toggle_switch_and_pygments_sync(self):
        """Verifies that clicking <md3-theme-toggle> switches theme, updates aria-pressed, and syncs Pygments."""
        with self.run_playwright() as page:
            page.goto(f"{self.url}/index.html")

            initial_theme = page.evaluate("document.documentElement.dataset.theme")
            toggle_btn = page.locator("#theme-menu-btn")
            self.assertEqual(toggle_btn.count(), 1)

            with self.spec_context(spec_key="COMPONENTS_THEME_TOGGLE"):
                toggle_btn.click()
                new_theme = page.evaluate("document.documentElement.dataset.theme")
                self.assertNotEqual(initial_theme, new_theme)
                expected_pressed = "true" if new_theme == "dark" else "false"
                self.assertEqual(toggle_btn.get_attribute("aria-pressed"), expected_pressed)

            with self.spec_context(spec_key="SPHINX_PYGMENTS"):
                dark_media = page.evaluate("document.getElementById('pygments_dark_css')?.media")
                self.assertEqual(dark_media, "all" if new_theme == "dark" else "not all")

            with self.spec_context(spec_key="COMPONENTS_THEME_TOGGLE"):
                toggle_btn.click()
                reverted_theme = page.evaluate("document.documentElement.dataset.theme")
                self.assertEqual(initial_theme, reverted_theme)

    @md3_conformance(spec_key="COMPONENTS_CODE_COPY")
    def test_code_copy_button_component(self):
        """Verifies that <md3-copy-button> is injected into code blocks, has a tooltip, and provides visual feedback."""
        with self.run_playwright() as page:
            page.goto(f"{self.url}/index.html")

            copy_btn = page.locator("md3-copy-button.md3-code-copy-btn")
            self.assertEqual(copy_btn.count(), 1)
            self.assertIn("Copy", copy_btn.inner_text())
            self.assertEqual(copy_btn.get_attribute("title"), "Copy code snippet")

            # Click copy button
            copy_btn.click()
            self.assertIn("Copied!", copy_btn.inner_text())
            self.assertIn("copied", copy_btn.get_attribute("class") or "")

    def test_search_dialog_modal_specs_and_live_filtering(self):
        """Verifies <md3-search> dialog dimensions (280px-560px), 28px corners, 32% scrim, live filtering, and focus return."""
        with self.run_playwright() as page:
            page.goto(f"{self.url}/index.html")

            search_bar = page.locator("#search-bar-trigger")
            search_input = page.locator("#md3-search-input")
            results = page.locator("#md3-search-results")

            with self.spec_context(spec_key="COMPONENTS_SEARCH_DIALOG"):
                self.assertFalse(page.evaluate("document.querySelector('#md3-search-dialog').open"))

                # Focus search bar trigger and click to open dialog
                search_bar.focus()
                search_bar.click()
                self.assertTrue(page.evaluate("document.querySelector('#md3-search-dialog').open"))

                dialog_styles = page.evaluate(
                    """() => {
                        const dlg = document.getElementById('md3-search-dialog');
                        const cs = window.getComputedStyle(dlg);
                        const backdropCs = window.getComputedStyle(dlg, '::backdrop');
                        const rect = dlg.getBoundingClientRect();
                        return {
                            radius: cs.borderRadius,
                            minWidth: cs.minWidth,
                            maxWidth: cs.maxWidth,
                            width: rect.width,
                            scrimOpacity: parseFloat(backdropCs.opacity),
                        };
                    }"""
                )
                self.assertEqual(dialog_styles["radius"], "28px")
                self.assertEqual(dialog_styles["minWidth"], "280px")
                self.assertEqual(dialog_styles["maxWidth"], "560px")
                self.assertGreaterEqual(dialog_styles["width"], 280.0)
                self.assertLessEqual(dialog_styles["width"], 560.0)
                self.assertAlmostEqual(dialog_styles["scrimOpacity"], 0.32, delta=0.01)

                # Type query and verify live search results
                search_input.fill("UniqueSearchableTokenXYZ")
                self.assertEqual(results.locator(".md3-search-result-item").count(), 1)
                self.assertIn("Section 2", results.inner_text())

            with self.spec_context(spec_key="COMPONENTS_DIALOG_FOCUS_RETURN"):
                # Press Escape to close dialog and verify focus returns to #search-bar-trigger
                page.keyboard.press("Escape")
                self.assertFalse(page.evaluate("document.querySelector('#md3-search-dialog').open"))
                active_id = page.evaluate("document.activeElement?.id")
                self.assertEqual(active_id, "search-bar-trigger")

    @md3_conformance(spec_key="COMPONENTS_PAGEFIND_SEARCH")
    def test_pagefind_full_site_search_across_pages(self):
        """Verifies that <md3-search> uses Pagefind to search across all pages in the site,
        renders MD3 result cards with <mark> highlighted excerpts, and navigates to the target section.
        """
        with self.run_playwright() as page:
            page.goto(f"{self.url}/index.html")

            search_bar = page.locator("#search-bar-trigger")
            search_input = page.locator("#md3-search-input")
            results = page.locator("#md3-search-results")

            search_bar.click()
            search_input.fill("CrossPageSearchTokenPagefind789")

            # Wait for Pagefind async result item to appear
            result_item = results.locator(".md3-search-result-item").first
            result_item.wait_for(state="visible", timeout=5000)

            self.assertEqual(results.locator(".md3-search-result-item").count(), 1)
            self.assertIn("Remote Guide Manual", results.inner_text())
            self.assertIn("Remote Architecture Section", results.inner_text())

            # Verify Pagefind <mark> highlight is rendered inside snippet
            marks = results.locator(".md3-search-result-snippet mark")
            self.assertGreaterEqual(marks.count(), 1)
            self.assertIn("CrossPageSearchTokenPagefind789", marks.first.inner_text())

            # Click the result link and verify it navigates to remote_guide.html#remote-architecture-section
            results.locator("a.md3-search-result-main-link").first.click()
            self.assertIn("remote_guide.html#remote-architecture-section", page.url)

    @md3_conformance(spec_key="COMPONENTS_TOC_SCROLLSPY")
    def test_toc_component_scrollspy_links(self):
        """Verifies that <md3-toc> renders section links and marks an active section."""
        with self.run_playwright() as page:
            page.goto(f"{self.url}/index.html")

            toc = page.locator("md3-toc#md3-toc")
            links = toc.locator("#md3-toc-nav a")
            self.assertGreaterEqual(links.count(), 2)
            self.assertGreaterEqual(toc.locator("#md3-toc-nav a.active").count(), 1)


if __name__ == "__main__":
    unittest.main()
