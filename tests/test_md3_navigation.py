import unittest
from harness import SphinxTestBase, md3_conformance


class TestMd3Navigation(SphinxTestBase):
    """Verifies large-site navigation scalability:
    1. Top-level primary navigation tabs (<md3-nav-tabs>) below the header.
    2. One-level-at-a-time progressive disclosure in <md3-sidebar> with ancestor
       drill-up links, child chevron indicators, and live section filtering.
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        conf_content = """
            project = "LargeDocsTest"
            extensions = ["md3"]
            html_theme = "md3"
        """
        index_content = """
            ===============
            Large Docs Home
            ===============

            .. toctree::
               :maxdepth: 2
               :caption: Main Sections

               guide/index
               api/index
               reference/index
        """
        extra_files = {
            "guide/index.rst": """
                ==========
                User Guide
                ==========

                .. toctree::
                   :maxdepth: 2

                   getting-started
                   advanced/index
            """,
            "guide/getting-started.rst": """
                ===============
                Getting Started
                ===============

                Quickstart instructions.
            """,
            "guide/advanced/index.rst": """
                ===============
                Advanced Topics
                ===============

                .. toctree::
                   :maxdepth: 1

                   deep-dive
                   performance
            """,
            "guide/advanced/deep-dive.rst": """
                =========
                Deep Dive
                =========

                Level 3 leaf document.
            """,
            "guide/advanced/performance.rst": """
                ==================
                Performance Tuning
                ==================

                Level 3 sibling document.
            """,
            "api/index.rst": """
                =============
                API Reference
                =============

                .. toctree::
                   :maxdepth: 1

                   client
                   server
            """,
            "api/client.rst": """
                ==========
                Client API
                ==========

                Client documentation.
            """,
            "api/server.rst": """
                ==========
                Server API
                ==========

                Server documentation.
            """,
            "reference/index.rst": """
                ================
                Module Reference
                ================

                .. toctree::
                   :maxdepth: 1
                   :caption: Modules

                   mod01
                   mod02
                   mod03
                   mod04
                   mod05
                   mod06
                   mod07
                   mod08
                   mod09
                   mod10
            """,
        }
        for i in range(1, 11):
            extra_files[f"reference/mod{i:02d}.rst"] = f"""
                =============
                Module {i:02d}
                =============

                Documentation for module {i:02d}.
            """

        outdir = cls.build_docs(
            conf_content,
            index_content,
            extra_files=extra_files,
            outdir_name="nav_out",
        )
        cls.url = cls.start_server(outdir)

    @md3_conformance(spec_key="COMPONENTS_NAV_TABS")
    def test_top_level_nav_tabs_rendered_and_active_across_hierarchy(self):
        """Verifies <md3-nav-tabs> renders top-level sections with compact 36px height
        and highlights the active top-level section even on deeply nested subpages.
        """
        with self.run_playwright() as page:
            page.goto(f"{self.url}/guide/advanced/deep-dive.html")

            nav_tabs = page.locator("md3-nav-tabs#md3-nav-tabs")
            self.assertEqual(nav_tabs.count(), 1)

            box = nav_tabs.bounding_box()
            self.assertIsNotNone(box)
            self.assertAlmostEqual(box["height"], 36.0, delta=1.5)

            tabs = nav_tabs.locator(".md3-nav-tabs__link")
            self.assertEqual(tabs.count(), 4)
            tab_texts = [tabs.nth(i).inner_text().strip() for i in range(4)]
            self.assertEqual(
                tab_texts,
                ["Home", "User Guide", "API Reference", "Module Reference"],
            )

            # On guide/advanced/deep-dive.html, "User Guide" tab must be marked active
            active_tab = nav_tabs.locator(".md3-nav-tabs__link.active")
            self.assertEqual(active_tab.count(), 1)
            self.assertEqual(active_tab.inner_text().strip(), "User Guide")

    @md3_conformance(spec_key="COMPONENTS_NAV_TABS_KEYBOARD")
    def test_nav_tabs_arrow_key_navigation(self):
        """Verifies ArrowRight, ArrowLeft, Home, and End keyboard traversal in <md3-nav-tabs>."""
        with self.run_playwright() as page:
            page.goto(f"{self.url}/index.html")

            tabs = page.locator("md3-nav-tabs .md3-nav-tabs__link")
            tabs.nth(0).focus()
            self.assertEqual(
                page.evaluate("document.activeElement?.textContent?.trim()"),
                "Home",
            )

            page.keyboard.press("ArrowRight")
            self.assertEqual(
                page.evaluate("document.activeElement?.textContent?.trim()"),
                "User Guide",
            )

            page.keyboard.press("End")
            self.assertEqual(
                page.evaluate("document.activeElement?.textContent?.trim()"),
                "Module Reference",
            )

            page.keyboard.press("ArrowRight")
            self.assertEqual(
                page.evaluate("document.activeElement?.textContent?.trim()"),
                "Home",
            )

            page.keyboard.press("ArrowLeft")
            self.assertEqual(
                page.evaluate("document.activeElement?.textContent?.trim()"),
                "Module Reference",
            )

            page.keyboard.press("Home")
            self.assertEqual(
                page.evaluate("document.activeElement?.textContent?.trim()"),
                "Home",
            )

    @md3_conformance(spec_key="COMPONENTS_NAV_PROGRESSIVE_DISCLOSURE")
    def test_progressive_disclosure_shows_one_level_at_a_time(self):
        """Verifies <md3-sidebar> shows strictly one hierarchy level at a time,
        renders ancestor drill-up links on nested pages, and filters large sections.
        """
        with self.run_playwright() as page:
            # 1. Root page: shows only the 3 top-level sections, NOT level-2 or level-3 items
            page.goto(f"{self.url}/index.html")
            root_items = page.locator("#sidebar-nav ul.md3-nav-list li")
            self.assertEqual(root_items.count(), 3)
            root_texts = [root_items.nth(i).inner_text().strip() for i in range(3)]
            self.assertEqual(root_texts, ["User Guide", "API Reference", "Module Reference"])
            # Each top-level section has children so it must have .has-children and chevron icon
            self.assertEqual(
                page.locator("#sidebar-nav ul.md3-nav-list li.has-children").count(),
                3,
            )

            # 2. Level-1 section page (guide/index.html): shows only its 2 immediate children
            page.goto(f"{self.url}/guide/index.html")
            guide_items = page.locator("#sidebar-nav ul.md3-nav-list li")
            self.assertEqual(guide_items.count(), 2)
            guide_texts = [guide_items.nth(i).inner_text().strip() for i in range(2)]
            self.assertEqual(guide_texts, ["Getting Started", "Advanced Topics"])
            # "Getting Started" is a leaf; "Advanced Topics" has children
            self.assertFalse(
                "has-children" in (guide_items.nth(0).get_attribute("class") or "")
            )
            self.assertTrue(
                "has-children" in (guide_items.nth(1).get_attribute("class") or "")
            )

            # 3. Level-3 leaf page (guide/advanced/deep-dive.html):
            # Shows ancestor back-links to "Large Docs Home" and "User Guide",
            # section header "Advanced Topics", and only the 2 level-3 sibling pages
            page.goto(f"{self.url}/guide/advanced/deep-dive.html")
            ancestors = page.locator("#sidebar-nav .md3-sidebar__ancestors li")
            self.assertEqual(ancestors.count(), 3)
            self.assertEqual(ancestors.nth(0).inner_text().strip(), "Large Docs Home")
            self.assertEqual(ancestors.nth(1).inner_text().strip(), "User Guide")
            self.assertEqual(ancestors.nth(2).inner_text().strip(), "Advanced Topics")

            leaf_items = page.locator("#sidebar-nav ul.md3-nav-list li")
            self.assertEqual(leaf_items.count(), 2)
            leaf_texts = [leaf_items.nth(i).inner_text().strip() for i in range(2)]
            self.assertEqual(leaf_texts, ["Deep Dive", "Performance Tuning"])

            # 4. Large section (reference/index.html with 10 items):
            # Renders #sidebar-filter-input and filters items in real time
            page.goto(f"{self.url}/reference/index.html")
            filter_input = page.locator("#sidebar-filter-input")
            self.assertEqual(filter_input.count(), 1)
            self.assertEqual(page.locator("#sidebar-nav ul.md3-nav-list li").count(), 10)

            filter_input.fill("Module 07")
            visible_items = page.locator("#sidebar-nav ul.md3-nav-list li:not([hidden])")
            self.assertEqual(visible_items.count(), 1)
            self.assertEqual(visible_items.first.inner_text().strip(), "Module 07")

            filter_input.fill("")
            self.assertEqual(
                page.locator("#sidebar-nav ul.md3-nav-list li:not([hidden])").count(),
                10,
            )

    @md3_conformance(spec_key="PROGRESSIVE_ENHANCEMENT_JS")
    def test_progressive_enhancement_graph_navigation_without_page_load(self):
        """Verifies that when JS is enabled, clicking ancestor back-links or section items
        with children traverses the navigation graph in-place without loading pages.
        """
        with self.run_playwright(java_script_enabled=True) as page:
            # Start on /guide/index.html
            target_url = f"{self.url}/guide/index.html"
            page.goto(target_url)
            self.assertEqual(page.url, target_url)
            self.assertEqual(
                page.locator("#sidebar-nav").get_attribute("data-active-level"),
                "guide/index",
            )

            # Set a window marker to verify no page reload occurs during graph traversal
            page.evaluate("window.__noReloadMarker = 'alive'")

            # 1. Click '<- Large Docs Home' back-link: should show top-level hierarchy without leaving /guide/index.html
            back_to_root = page.locator('#sidebar-nav a.md3-sidebar__back-link[data-nav-level="index"]')
            self.assertEqual(back_to_root.count(), 1)
            back_to_root.click()

            self.assertEqual(page.url, target_url)
            self.assertEqual(page.evaluate("window.__noReloadMarker"), "alive")
            self.assertEqual(
                page.locator("#sidebar-nav").get_attribute("data-active-level"),
                "index",
            )
            root_items = page.locator("#sidebar-nav ul.md3-nav-list li")
            self.assertEqual(root_items.count(), 3)
            self.assertEqual(
                [root_items.nth(i).inner_text().strip() for i in range(3)],
                ["User Guide", "API Reference", "Module Reference"],
            )

            # 2. Click 'Module Reference' (has-children) to drill down into reference/index without leaving /guide/index.html
            mod_ref_link = page.locator('#sidebar-nav ul.md3-nav-list a[data-nav-level="reference/index"]')
            self.assertEqual(mod_ref_link.count(), 1)
            mod_ref_link.click()

            self.assertEqual(page.url, target_url)
            self.assertEqual(page.evaluate("window.__noReloadMarker"), "alive")
            self.assertEqual(
                page.locator("#sidebar-nav").get_attribute("data-active-level"),
                "reference/index",
            )
            self.assertEqual(page.locator("#sidebar-nav ul.md3-nav-list li").count(), 10)

            # Filter input should automatically unhide because reference/index has 10 (>= 8) items
            filter_wrapper = page.locator(".md3-sidebar__filter")
            self.assertFalse(filter_wrapper.evaluate("el => el.hidden"))
            filter_input = page.locator("#sidebar-filter-input")
            filter_input.fill("Module 05")
            visible_mods = page.locator("#sidebar-nav ul.md3-nav-list li:not([hidden])")
            self.assertEqual(visible_mods.count(), 1)
            self.assertEqual(visible_mods.first.inner_text().strip(), "Module 05")

            # 3. Clicking a leaf document ('Module 05') navigates to that page
            visible_mods.first.locator("a").click()
            self.assertEqual(page.url, f"{self.url}/reference/mod05.html")

    @md3_conformance(spec_key="PROGRESSIVE_ENHANCEMENT_NO_JS")
    def test_progressive_disclosure_fallback_when_js_disabled(self):
        """Verifies that when JS is disabled, clicking ancestor back-links and section links
        navigates across pages via standard HTML links.
        """
        with self.run_playwright(java_script_enabled=False) as page:
            page.goto(f"{self.url}/guide/index.html")
            back_link = page.locator("#sidebar-nav a.md3-sidebar__back-link").first
            self.assertEqual(back_link.inner_text().strip(), "Large Docs Home")
            back_link.click()
            self.assertEqual(page.url, f"{self.url}/index.html")


if __name__ == "__main__":
    unittest.main()
