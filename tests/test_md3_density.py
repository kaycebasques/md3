import unittest
from harness import SphinxTestBase, md3_conformance


class TestMd3DensityConformance(SphinxTestBase):
    """Verifies compliance with high information density / small MD3 component options.

    Per prompt requirements:
    "emphasize information density e.g. use the 'small' options in md3 to get
    more elements on page (avoiding gigantic buttons)."
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        conf_content = """
            project = "DensityTest"
            extensions = ["md3"]
            html_theme = "md3"
        """
        index_content = """
            ============
            Density Page
            ============

            .. toctree::
               :maxdepth: 2

               subpage

            Intro text with `a link <https://example.com>`__.

            Section 1
            =========

            Content with a code block:

            .. code-block:: python

               x = 42

            .. list-table::
               :header-rows: 1

               * - Col 1
                 - Col 2
               * - Val 1
                 - Val 2

            .. raw:: html

               <div id="density-samples">
                 <button class="md3-btn md3-btn--filled" id="sample-filled-btn">Action</button>
                 <button class="md3-btn md3-btn--tonal" id="sample-tonal-btn">Tonal</button>
                 <button class="md3-btn md3-btn--elevated" id="sample-elevated-btn">Elevated</button>
                 <button class="md3-btn md3-btn--outlined" id="sample-outlined-btn">Outlined</button>
                 <button class="md3-btn md3-btn--text" id="sample-text-btn">Text</button>
                 <button class="md3-btn md3-btn--filled md3-btn--square" id="sample-square-btn">Square</button>
                 <button class="md3-btn md3-btn--filled" id="sample-disabled-btn" disabled>Disabled</button>
                 <span class="md3-chip" id="sample-chip">v0.1.0</span>
                 <span class="md3-chip md3-chip--selected" id="sample-selected-chip">Selected</span>
               </div>
        """
        subpage_content = """
            =======
            Subpage
            =======

            Subpage content.
        """
        outdir = cls.build_docs(
            conf_content,
            index_content,
            extra_files={"subpage.rst": subpage_content},
            outdir_name="density_out",
        )
        cls.url = cls.start_server(outdir)

    def test_button_xsmall_compact_height_and_shapes(self):
        """Verifies buttons use MD3 xsmall (32px) compact spec, round/square shapes, and disabled opacity."""
        with self.run_playwright() as page:
            page.goto(f"{self.url}/index.html")

            with self.spec_context(spec_key="DENSITY_BUTTONS"):
                for selector in [
                    "#back-to-top",
                    "#sample-filled-btn",
                    "#sample-tonal-btn",
                    "#sample-elevated-btn",
                    "#sample-outlined-btn",
                    "#sample-text-btn",
                    "#sample-square-btn",
                ]:
                    btn = page.locator(selector)
                    self.assertEqual(btn.count(), 1)
                    box = btn.bounding_box()
                    self.assertIsNotNone(box)
                    self.assertAlmostEqual(
                        box["height"],
                        32.0,
                        delta=1.0,
                        msg=f"Button {selector} height {box['height']}px must match MD3 xsmall 32px spec",
                    )
                    self.assertLessEqual(box["height"], 36.0)

                round_radius = page.evaluate(
                    "window.getComputedStyle(document.getElementById('sample-filled-btn')).borderRadius"
                )
                square_radius = page.evaluate(
                    "window.getComputedStyle(document.getElementById('sample-square-btn')).borderRadius"
                )
                self.assertEqual(round_radius, "9999px")
                self.assertEqual(square_radius, "12px")

            with self.spec_context(spec_key="COMPONENTS_BUTTON_VARIANTS"):
                # Text buttons must not be underlined per MD3 Button guidelines
                for selector in ["#sample-filled-btn", "#sample-text-btn", "#sample-elevated-btn"]:
                    td_line = page.evaluate(
                        f"window.getComputedStyle(document.querySelector('{selector}')).textDecorationLine"
                    )
                    self.assertEqual(td_line, "none")

            with self.spec_context(spec_key="STATE_LAYERS"):
                disabled_opacity = page.evaluate(
                    "parseFloat(window.getComputedStyle(document.getElementById('sample-disabled-btn')).opacity)"
                )
                self.assertAlmostEqual(disabled_opacity, 0.38, delta=0.01)

    @md3_conformance(spec_key="DENSITY_NAV_DRAWER")
    def test_navigation_item_compact_height(self):
        """Verifies navigation drawer items use compact 32px active-indicator height."""
        with self.run_playwright() as page:
            page.goto(f"{self.url}/index.html")

            nav_item = page.locator("#sidebar-nav a").first
            self.assertEqual(nav_item.count(), 1)
            box = nav_item.bounding_box()
            self.assertIsNotNone(box)
            self.assertAlmostEqual(box["height"], 32.0, delta=1.0)
            self.assertLessEqual(
                box["height"],
                36.0,
                f"Nav item height {box['height']}px exceeds compact limit of 36px",
            )

    @md3_conformance(spec_key="DENSITY_SEARCH")
    def test_search_bar_compact_height(self):
        """Verifies top search bar uses compact 36px height (height <= 40px)."""
        with self.run_playwright() as page:
            page.goto(f"{self.url}/index.html")

            search_bar = page.locator("#search-bar-trigger")
            self.assertEqual(search_bar.count(), 1)
            box = search_bar.bounding_box()
            self.assertIsNotNone(box)
            self.assertAlmostEqual(box["height"], 36.0, delta=1.0)
            self.assertLessEqual(
                box["height"],
                40.0,
                f"Search bar height {box['height']}px exceeds compact limit of 40px",
            )

    @md3_conformance(spec_key="DENSITY_ICON_BUTTONS")
    def test_icon_buttons_xsmall_size(self):
        """Verifies icon buttons use MD3 icon-button-xsmall (32x32px) spec."""
        with self.run_playwright() as page:
            page.goto(f"{self.url}/index.html")

            theme_toggle = page.locator("md3-theme-toggle")
            self.assertEqual(theme_toggle.count(), 1)
            box = theme_toggle.bounding_box()
            self.assertIsNotNone(box)
            self.assertAlmostEqual(box["height"], 32.0, delta=1.0)
            self.assertAlmostEqual(box["width"], 32.0, delta=1.0)

    @md3_conformance(spec_key="DENSITY_CHIPS")
    def test_chip_compact_size_and_selected_variant(self):
        """Verifies assist and filter chips use MD3 32px height, 8px corner radius, and secondary-container fill."""
        with self.run_playwright() as page:
            page.goto(f"{self.url}/index.html")

            chip = page.locator("#sample-chip")
            selected_chip = page.locator("#sample-selected-chip")
            self.assertEqual(chip.count(), 1)
            self.assertEqual(selected_chip.count(), 1)

            box = chip.bounding_box()
            self.assertIsNotNone(box)
            self.assertAlmostEqual(box["height"], 32.0, delta=1.0)

            styles = page.evaluate(
                """() => {
                    const cs1 = window.getComputedStyle(document.getElementById('sample-chip'));
                    const cs2 = window.getComputedStyle(document.getElementById('sample-selected-chip'));
                    return {
                        radius: cs1.borderRadius,
                        selectedBg: cs2.backgroundColor,
                    };
                }"""
            )
            self.assertEqual(styles["radius"], "8px")
            self.assertNotEqual(styles["selectedBg"], "rgba(0, 0, 0, 0)")

    def test_table_compact_cell_padding_and_tabular_numerals(self):
        """Verifies table cells have compact 8px vertical padding and tabular numerals."""
        with self.run_playwright() as page:
            page.goto(f"{self.url}/index.html")

            td = page.locator("table.docutils td").first
            self.assertEqual(td.count(), 1)
            with self.spec_context(spec_key="DENSITY_TABLES"):
                padding_top = page.evaluate(
                    "parseFloat(window.getComputedStyle(document.querySelector('table.docutils td')).paddingTop)"
                )
                self.assertEqual(padding_top, 8.0)
                self.assertLessEqual(padding_top, 12.0)

            with self.spec_context(spec_key="TYPOGRAPHY_TABULAR_NUMERALS"):
                fvn = page.evaluate(
                    "window.getComputedStyle(document.querySelector('table.docutils')).fontVariantNumeric"
                )
                self.assertIn("tabular-nums", fvn)

    @md3_conformance(spec_key="COMPONENTS_TOP_APP_BAR")
    def test_top_app_bar_small_height(self):
        """Verifies small top app bar container height is 56px per MD3 specs."""
        with self.run_playwright() as page:
            page.goto(f"{self.url}/index.html")

            bar = page.locator("md3-top-app-bar.md3-top-app-bar")
            self.assertEqual(bar.count(), 1)
            box = bar.bounding_box()
            self.assertIsNotNone(box)
            self.assertAlmostEqual(box["height"], 56.0, delta=1.0)

    @md3_conformance(spec_key="DENSITY_SCALE")
    def test_density_scale_variable_conformance(self):
        """Verifies --md-density-scale is configured to -2 for compact density."""
        with self.run_playwright() as page:
            page.goto(f"{self.url}/index.html")

            scale = page.evaluate(
                "window.getComputedStyle(document.documentElement).getPropertyValue('--md-density-scale').trim()"
            )
            self.assertEqual(scale, "-2")


if __name__ == "__main__":
    unittest.main()
