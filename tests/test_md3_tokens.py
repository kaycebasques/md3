import math
import re
import unittest
from pathlib import Path
from harness import SphinxTestBase, md3_conformance


def hex_to_relative_luminance(hex_str: str) -> float:
    """Calculates relative luminance for a given hex color per WCAG 2.1 specs."""
    hex_clean = hex_str.strip().lstrip("#")
    if len(hex_clean) == 3:
        hex_clean = "".join(c * 2 for c in hex_clean)
    r = int(hex_clean[0:2], 16) / 255.0
    g = int(hex_clean[2:4], 16) / 255.0
    b = int(hex_clean[4:6], 16) / 255.0

    def to_linear(c):
        return c / 12.92 if c <= 0.03928 else math.pow((c + 0.055) / 1.055, 2.4)

    rl = to_linear(r)
    gl = to_linear(g)
    bl = to_linear(b)
    return 0.2126 * rl + 0.7152 * gl + 0.0722 * bl


def contrast_ratio(hex1: str, hex2: str) -> float:
    """Calculates contrast ratio between two hex colors."""
    l1 = hex_to_relative_luminance(hex1)
    l2 = hex_to_relative_luminance(hex2)
    lighter = max(l1, l2)
    darker = min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)


class TestMd3TokensConformance(SphinxTestBase):
    """Verifies compliance with Google Material Design 3 Design Token Specifications
    both statically and via live Playwright computed style inspection, with granular
    spec_context deeplinks for every token category.
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        css_path = Path(__file__).resolve().parent.parent / "md3" / "components" / "app.css"
        cls.css_content = css_path.read_text(encoding="utf-8")

        cls.light_vars = {}
        cls.dark_vars = {}

        clean_css = re.sub(r"/\*.*?\*/", "", cls.css_content, flags=re.DOTALL)

        root_match = re.search(r":root\s*\{([^}]+)\}", clean_css)
        if root_match:
            for line in root_match.group(1).split(";"):
                line = line.strip()
                if ":" in line and line.startswith("--"):
                    k, v = line.split(":", 1)
                    cls.light_vars[k.strip()] = v.strip()

        dark_match = re.search(r'\[data-theme="dark"\][^{]*\{([^}]+)\}', clean_css)
        if dark_match:
            for line in dark_match.group(1).split(";"):
                line = line.strip()
                if ":" in line and line.startswith("--"):
                    k, v = line.split(":", 1)
                    cls.dark_vars[k.strip()] = v.strip()

        conf_content = """
            project = "TokensConformanceTest"
            extensions = ["md3"]
            html_theme = "md3"
        """
        index_content = """
            =======================
            Tokens Conformance Test
            =======================

            .. raw:: html

               <div id="typescale-specimens">
                 <div class="md-typescale-display-large" id="ts-display-large">Display Large</div>
                 <div class="md-typescale-display-medium" id="ts-display-medium">Display Medium</div>
                 <div class="md-typescale-display-small" id="ts-display-small">Display Small</div>
                 <div class="md-typescale-headline-large" id="ts-headline-large">Headline Large</div>
                 <div class="md-typescale-headline-medium" id="ts-headline-medium">Headline Medium</div>
                 <div class="md-typescale-headline-small" id="ts-headline-small">Headline Small</div>
                 <div class="md-typescale-title-large" id="ts-title-large">Title Large</div>
                 <div class="md-typescale-title-medium" id="ts-title-medium">Title Medium</div>
                 <div class="md-typescale-title-small" id="ts-title-small">Title Small</div>
                 <div class="md-typescale-body-large" id="ts-body-large">Body Large</div>
                 <div class="md-typescale-body-medium" id="ts-body-medium">Body Medium</div>
                 <div class="md-typescale-body-small" id="ts-body-small">Body Small</div>
                 <div class="md-typescale-label-large" id="ts-label-large">Label Large</div>
                 <div class="md-typescale-label-medium" id="ts-label-medium">Label Medium</div>
                 <div class="md-typescale-label-small" id="ts-label-small">Label Small</div>
               </div>
               <div id="component-specimens">
                 <button class="md3-btn md3-btn--filled" id="btn-filled">Filled</button>
                 <button class="md3-btn md3-btn--tonal" id="btn-tonal">Tonal</button>
                 <button class="md3-btn md3-btn--elevated" id="btn-elevated">Elevated</button>
                 <button class="md3-btn md3-btn--outlined" id="btn-outlined">Outlined</button>
                 <button class="md3-btn md3-btn--text" id="btn-text">Text</button>
                 <span class="md3-chip" id="chip-assist">Assist Chip</span>
                 <span class="md3-chip md3-chip--selected" id="chip-filter">Filter Chip</span>
                 <div class="md3-card md3-card--outlined" id="card-outlined">Outlined Card</div>
                 <div class="md3-card md3-card--filled" id="card-filled">Filled Card</div>
                 <div class="md3-card md3-card--elevated" id="card-elevated">Elevated Card</div>
                 <hr class="md3-divider" id="divider-specimen" />
               </div>
        """
        outdir = cls.build_docs(conf_content, index_content, outdir_name="tokens_out")
        cls.url = cls.start_server(outdir)

    @md3_conformance(spec_key="COLOR_PALETTE_TONES")
    def test_md3_reference_palette_tokens_conformance(self):
        """Validates that official Google MD3 reference palette tokens (--md-ref-palette-*) exist."""
        expected_ref_tokens = {
            "--md-ref-palette-black": "#000000",
            "--md-ref-palette-white": "#ffffff",
            "--md-ref-palette-primary10": "#041e49",
            "--md-ref-palette-primary20": "#062e6f",
            "--md-ref-palette-primary30": "#0842a0",
            "--md-ref-palette-primary40": "#0b57d0",
            "--md-ref-palette-primary80": "#a8c7fa",
            "--md-ref-palette-primary90": "#d3e3fd",
            "--md-ref-palette-secondary10": "#001d35",
            "--md-ref-palette-secondary20": "#003355",
            "--md-ref-palette-secondary30": "#004a77",
            "--md-ref-palette-secondary40": "#00639b",
            "--md-ref-palette-secondary80": "#7fcfff",
            "--md-ref-palette-secondary90": "#c2e7ff",
            "--md-ref-palette-tertiary10": "#072711",
            "--md-ref-palette-tertiary20": "#0a3818",
            "--md-ref-palette-tertiary30": "#0f5223",
            "--md-ref-palette-tertiary40": "#146c2e",
            "--md-ref-palette-tertiary80": "#6dd58c",
            "--md-ref-palette-tertiary90": "#c4eed0",
            "--md-ref-palette-error10": "#410e0b",
            "--md-ref-palette-error20": "#601410",
            "--md-ref-palette-error30": "#8c1d18",
            "--md-ref-palette-error40": "#b3261e",
            "--md-ref-palette-error80": "#f2b8b5",
            "--md-ref-palette-error90": "#f9dedc",
            "--md-ref-palette-neutral6": "#131314",
            "--md-ref-palette-neutral10": "#1f1f1f",
            "--md-ref-palette-neutral90": "#e3e3e3",
            "--md-ref-palette-neutral100": "#ffffff",
            "--md-ref-palette-neutral-variant30": "#444746",
            "--md-ref-palette-neutral-variant50": "#747775",
            "--md-ref-palette-neutral-variant60": "#8e918f",
            "--md-ref-palette-neutral-variant80": "#c4c7c5",
            "--md-ref-palette-neutral-variant90": "#e1e3e1",
        }
        for token, expected in expected_ref_tokens.items():
            self.assertIn(token, self.light_vars, f"Missing reference palette token: {token}")
            self.assertEqual(self.light_vars[token], expected)

    def test_required_md3_color_roles_exist_in_light_and_dark_themes(self):
        """Validates that all MD3 system color role groups exist in light and dark themes."""
        role_groups = {
            "COLOR_PRIMARY": ["primary", "on-primary", "primary-container", "on-primary-container"],
            "COLOR_SECONDARY": ["secondary", "on-secondary", "secondary-container", "on-secondary-container"],
            "COLOR_TERTIARY": ["tertiary", "on-tertiary", "tertiary-container", "on-tertiary-container"],
            "COLOR_ERROR": ["error", "on-error", "error-container", "on-error-container"],
            "COLOR_FIXED_ACCENTS": [
                "primary-fixed", "primary-fixed-dim", "on-primary-fixed", "on-primary-fixed-variant",
                "secondary-fixed", "secondary-fixed-dim", "on-secondary-fixed", "on-secondary-fixed-variant",
                "tertiary-fixed", "tertiary-fixed-dim", "on-tertiary-fixed", "on-tertiary-fixed-variant",
            ],
            "COLOR_SURFACE": [
                "background", "on-background", "surface", "on-surface",
                "surface-variant", "on-surface-variant", "surface-tint", "shadow", "scrim",
            ],
            "COLOR_SURFACE_CONTAINERS": [
                "surface-container-lowest", "surface-container-low", "surface-container",
                "surface-container-high", "surface-container-highest",
            ],
            "COLOR_BRIGHT_DIM": ["surface-bright", "surface-dim"],
            "COLOR_OUTLINE": ["outline", "outline-variant"],
            "COLOR_INVERSE": ["inverse-surface", "inverse-on-surface", "inverse-primary"],
        }
        for spec_key, roles in role_groups.items():
            with self.spec_context(spec_key=spec_key):
                for role in roles:
                    token = f"--md-sys-color-{role}"
                    self.assertIn(token, self.light_vars, f"Missing light color token: {token}")
                    self.assertIn(token, self.dark_vars, f"Missing dark color token: {token}")

    def test_md3_color_contrast_conformance(self):
        """Validates WCAG 2.1 AA contrast ratios (>= 4.5:1 text pairs and >= 3.0:1 outline boundaries)."""
        text_color_pairs = [
            ("--md-sys-color-on-primary", "--md-sys-color-primary"),
            ("--md-sys-color-on-secondary", "--md-sys-color-secondary"),
            ("--md-sys-color-on-tertiary", "--md-sys-color-tertiary"),
            ("--md-sys-color-on-error", "--md-sys-color-error"),
            ("--md-sys-color-on-background", "--md-sys-color-background"),
            ("--md-sys-color-on-surface", "--md-sys-color-surface"),
            ("--md-sys-color-on-surface-variant", "--md-sys-color-surface"),
            ("--md-sys-color-on-primary-container", "--md-sys-color-primary-container"),
            ("--md-sys-color-on-secondary-container", "--md-sys-color-secondary-container"),
            ("--md-sys-color-on-tertiary-container", "--md-sys-color-tertiary-container"),
            ("--md-sys-color-on-error-container", "--md-sys-color-error-container"),
            ("--md-sys-color-inverse-on-surface", "--md-sys-color-inverse-surface"),
        ]

        with self.spec_context(spec_key="COLOR_CONTRAST_WCAG"):
            for fg_key, bg_key in text_color_pairs:
                fg = self.light_vars[fg_key]
                bg = self.light_vars[bg_key]
                ratio = contrast_ratio(fg, bg)
                self.assertGreaterEqual(
                    ratio,
                    4.5,
                    f"Light contrast failure between {fg_key} ({fg}) and {bg_key} ({bg}): {ratio:.2f} < 4.5",
                )

            for fg_key, bg_key in text_color_pairs:
                fg = self.dark_vars[fg_key]
                bg = self.dark_vars[bg_key]
                ratio = contrast_ratio(fg, bg)
                self.assertGreaterEqual(
                    ratio,
                    4.5,
                    f"Dark contrast failure between {fg_key} ({fg}) and {bg_key} ({bg}): {ratio:.2f} < 4.5",
                )

        with self.spec_context(spec_key="COLOR_OUTLINE"):
            light_outline_ratio = contrast_ratio(
                self.light_vars["--md-sys-color-outline"],
                self.light_vars["--md-sys-color-surface"],
            )
            self.assertGreaterEqual(
                light_outline_ratio,
                3.0,
                f"Light outline contrast {light_outline_ratio:.2f} < 3.0",
            )
            dark_outline_ratio = contrast_ratio(
                self.dark_vars["--md-sys-color-outline"],
                self.dark_vars["--md-sys-color-surface"],
            )
            self.assertGreaterEqual(
                dark_outline_ratio,
                3.0,
                f"Dark outline contrast {dark_outline_ratio:.2f} < 3.0",
            )

    def test_md3_shape_elevation_state_and_motion_tokens_conformance(self):
        """Validates shape, elevation, state layer, focus ring, motion, and spacing tokens with granular spec_context."""
        with self.spec_context(spec_key="SHAPE_CORNER_RADIUS_SCALE"):
            expected_shapes = {
                "--md-sys-shape-corner-none": "0px",
                "--md-sys-shape-corner-extra-small": "4px",
                "--md-sys-shape-corner-small": "8px",
                "--md-sys-shape-corner-medium": "12px",
                "--md-sys-shape-corner-large": "16px",
                "--md-sys-shape-corner-large-increased": "20px",
                "--md-sys-shape-corner-extra-large": "28px",
                "--md-sys-shape-corner-extra-large-increased": "32px",
                "--md-sys-shape-corner-extra-extra-large": "48px",
                "--md-sys-shape-corner-full": "9999px",
            }
            for token, expected_val in expected_shapes.items():
                self.assertEqual(self.light_vars.get(token), expected_val)

        with self.spec_context(spec_key="ELEVATION_TOKENS"):
            expected_elevation_dp = {
                "--md-sys-elevation-level0-value": "0px",
                "--md-sys-elevation-level1-value": "1px",
                "--md-sys-elevation-level2-value": "3px",
                "--md-sys-elevation-level3-value": "6px",
                "--md-sys-elevation-level4-value": "8px",
                "--md-sys-elevation-level5-value": "12px",
            }
            for token, expected_dp in expected_elevation_dp.items():
                self.assertEqual(self.light_vars.get(token), expected_dp)
            for level in range(6):
                token = f"--md-sys-elevation-level{level}"
                self.assertIn(token, self.light_vars)
                if level == 0:
                    self.assertEqual(self.light_vars[token], "none")
                else:
                    self.assertIn("rgba", self.light_vars[token])

        with self.spec_context(spec_key="STATE_LAYERS"):
            self.assertEqual(self.light_vars.get("--md-sys-state-hover-state-layer-opacity"), "0.08")
            self.assertEqual(self.light_vars.get("--md-sys-state-focus-state-layer-opacity"), "0.10")
            self.assertEqual(self.light_vars.get("--md-sys-state-pressed-state-layer-opacity"), "0.10")
            self.assertEqual(self.light_vars.get("--md-sys-state-dragged-state-layer-opacity"), "0.16")
            self.assertEqual(self.light_vars.get("--md-sys-state-disabled-state-layer-opacity"), "0.38")

        with self.spec_context(spec_key="ACCESSIBILITY_FOCUS_RING"):
            self.assertEqual(self.light_vars.get("--md-sys-state-focus-indicator-thickness"), "3px")
            self.assertEqual(self.light_vars.get("--md-sys-state-focus-indicator-outer-offset"), "2px")
            self.assertEqual(self.light_vars.get("--md-sys-state-focus-indicator-inner-offset"), "-3px")

        with self.spec_context(spec_key="MOTION_SPECS"):
            expected_easings = {
                "--md-sys-motion-easing-linear": "cubic-bezier(0, 0, 1, 1)",
                "--md-sys-motion-easing-standard": "cubic-bezier(0.2, 0, 0, 1)",
                "--md-sys-motion-easing-standard-accelerate": "cubic-bezier(0.3, 0, 1, 1)",
                "--md-sys-motion-easing-standard-decelerate": "cubic-bezier(0, 0, 0, 1)",
                "--md-sys-motion-easing-emphasized": "cubic-bezier(0.2, 0, 0, 1)",
                "--md-sys-motion-easing-emphasized-accelerate": "cubic-bezier(0.3, 0, 0.8, 0.15)",
                "--md-sys-motion-easing-emphasized-decelerate": "cubic-bezier(0.05, 0.7, 0.1, 1)",
            }
            for token, val in expected_easings.items():
                self.assertEqual(self.light_vars.get(token), val)
            expected_durations = {
                "short1": "50ms", "short2": "100ms", "short3": "150ms", "short4": "200ms",
                "medium1": "250ms", "medium2": "300ms", "medium3": "350ms", "medium4": "400ms",
                "long1": "450ms", "long2": "500ms", "long3": "550ms", "long4": "600ms",
                "extra-long1": "700ms", "extra-long2": "800ms", "extra-long3": "900ms", "extra-long4": "1000ms",
            }
            for dur, ms in expected_durations.items():
                self.assertEqual(self.light_vars.get(f"--md-sys-motion-duration-{dur}"), ms)

        with self.spec_context(spec_key="SPACING_SYSTEM_TOKENS"):
            expected_spacing = {
                "--md-sys-measurement-space0": "0px",
                "--md-sys-measurement-space25": "2px",
                "--md-sys-measurement-space50": "4px",
                "--md-sys-measurement-space75": "6px",
                "--md-sys-measurement-space100": "8px",
                "--md-sys-measurement-space125": "10px",
                "--md-sys-measurement-space150": "12px",
                "--md-sys-measurement-space175": "14px",
                "--md-sys-measurement-space200": "16px",
                "--md-sys-measurement-space250": "20px",
                "--md-sys-measurement-space300": "24px",
                "--md-sys-measurement-space400": "32px",
                "--md-sys-measurement-space450": "36px",
                "--md-sys-measurement-space500": "40px",
                "--md-sys-measurement-space600": "48px",
                "--md-sys-measurement-space700": "56px",
                "--md-sys-measurement-space800": "64px",
                "--md-sys-measurement-space900": "72px",
            }
            for token, px in expected_spacing.items():
                self.assertEqual(self.light_vars.get(token), px)

    def test_md3_official_component_tokens_conformance(self):
        """Validates official MD3 component tokens (--md-comp-*) with granular spec_context per component."""
        with self.spec_context(spec_key="DENSITY_BUTTONS"):
            button_tokens = {
                "--md-comp-button-xsmall-container-height": "32px",
                "--md-comp-button-xsmall-leading-space": "12px",
                "--md-comp-button-xsmall-trailing-space": "12px",
                "--md-comp-button-xsmall-icon-size": "20px",
                "--md-comp-button-xsmall-icon-label-space": "8px",
                "--md-comp-button-xsmall-container-shape-round": "var(--md-sys-shape-corner-full)",
                "--md-comp-button-xsmall-container-shape-square": "var(--md-sys-shape-corner-medium)",
                "--md-comp-button-small-container-height": "40px",
                "--md-comp-button-small-leading-space": "16px",
                "--md-comp-button-small-trailing-space": "16px",
            }
            for token, expected in button_tokens.items():
                self.assertEqual(self.light_vars.get(token), expected)

        with self.spec_context(spec_key="SHAPE_MORPH_INTERACTION"):
            self.assertEqual(
                self.light_vars.get("--md-comp-button-xsmall-pressed-container-shape"),
                "var(--md-sys-shape-corner-small)",
            )
            self.assertEqual(
                self.light_vars.get("--md-comp-icon-button-xsmall-pressed-container-shape"),
                "var(--md-sys-shape-corner-small)",
            )

        with self.spec_context(spec_key="COMPONENTS_BUTTON_VARIANTS"):
            variant_tokens = {
                "--md-comp-filled-button-container-color": "var(--md-sys-color-primary)",
                "--md-comp-filled-button-label-text-color": "var(--md-sys-color-on-primary)",
                "--md-comp-filled-tonal-button-container-color": "var(--md-sys-color-secondary-container)",
                "--md-comp-filled-tonal-button-label-text-color": "var(--md-sys-color-on-secondary-container)",
                "--md-comp-elevated-button-container-color": "var(--md-sys-color-surface-container-low)",
                "--md-comp-elevated-button-label-text-color": "var(--md-sys-color-primary)",
                "--md-comp-elevated-button-container-elevation": "var(--md-sys-elevation-level1)",
                "--md-comp-outlined-button-outline-color": "var(--md-sys-color-outline)",
                "--md-comp-outlined-button-outline-width": "1px",
                "--md-comp-outlined-button-label-text-color": "var(--md-sys-color-primary)",
                "--md-comp-text-button-label-text-color": "var(--md-sys-color-primary)",
            }
            for token, expected in variant_tokens.items():
                self.assertEqual(self.light_vars.get(token), expected)

        with self.spec_context(spec_key="DENSITY_ICON_BUTTONS"):
            self.assertEqual(self.light_vars.get("--md-comp-icon-button-xsmall-container-height"), "32px")
            self.assertEqual(self.light_vars.get("--md-comp-icon-button-xsmall-icon-size"), "20px")
            self.assertEqual(self.light_vars.get("--md-comp-icon-button-small-container-height"), "40px")
            self.assertEqual(self.light_vars.get("--md-comp-icon-button-small-icon-size"), "24px")

        with self.spec_context(spec_key="DENSITY_CHIPS"):
            self.assertEqual(self.light_vars.get("--md-comp-assist-chip-container-height"), "32px")
            self.assertEqual(self.light_vars.get("--md-comp-assist-chip-container-shape"), "var(--md-sys-shape-corner-small)")
            self.assertEqual(self.light_vars.get("--md-comp-assist-chip-with-icon-icon-size"), "18px")
            self.assertEqual(self.light_vars.get("--md-comp-assist-chip-flat-outline-color"), "var(--md-sys-color-outline-variant)")
            self.assertEqual(self.light_vars.get("--md-comp-filter-chip-container-height"), "32px")
            self.assertEqual(
                self.light_vars.get("--md-comp-filter-chip-flat-selected-container-color"),
                "var(--md-sys-color-secondary-container)",
            )

        with self.spec_context(spec_key="COMPONENTS_TOP_APP_BAR"):
            self.assertEqual(self.light_vars.get("--md-comp-top-app-bar-small-container-height"), "56px")
            self.assertEqual(self.light_vars.get("--md-comp-top-app-bar-small-container-color"), "var(--md-sys-color-surface)")
            self.assertEqual(
                self.light_vars.get("--md-comp-top-app-bar-small-on-scroll-container-color"),
                "var(--md-sys-color-surface-container)",
            )

        with self.spec_context(spec_key="DENSITY_NAV_DRAWER"):
            self.assertEqual(self.light_vars.get("--md-comp-navigation-drawer-container-width"), "260px")
            self.assertEqual(self.light_vars.get("--md-comp-navigation-drawer-active-indicator-height"), "32px")
            self.assertEqual(
                self.light_vars.get("--md-comp-navigation-drawer-active-indicator-shape"),
                "var(--md-sys-shape-corner-full)",
            )
            self.assertEqual(self.light_vars.get("--md-comp-navigation-drawer-scrim-opacity"), "0.32")

        with self.spec_context(spec_key="COMPONENTS_LISTS"):
            self.assertEqual(self.light_vars.get("--md-comp-list-list-item-one-line-container-height"), "32px")
            self.assertEqual(self.light_vars.get("--md-comp-list-list-item-leading-space"), "12px")
            self.assertEqual(self.light_vars.get("--md-comp-list-list-item-trailing-space"), "12px")

        with self.spec_context(spec_key="DENSITY_SEARCH"):
            self.assertEqual(self.light_vars.get("--md-comp-search-bar-container-height"), "36px")
            self.assertEqual(
                self.light_vars.get("--md-comp-search-bar-container-color"),
                "var(--md-sys-color-surface-container-high)",
            )
            self.assertEqual(
                self.light_vars.get("--md-comp-search-bar-container-shape"),
                "var(--md-sys-shape-corner-full)",
            )

        with self.spec_context(spec_key="COMPONENTS_SEARCH_DIALOG"):
            self.assertEqual(
                self.light_vars.get("--md-comp-dialog-container-color"),
                "var(--md-sys-color-surface-container-high)",
            )
            self.assertEqual(
                self.light_vars.get("--md-comp-dialog-container-shape"),
                "var(--md-sys-shape-corner-extra-large)",
            )
            self.assertEqual(
                self.light_vars.get("--md-comp-dialog-container-elevation"),
                "var(--md-sys-elevation-level3)",
            )

        with self.spec_context(spec_key="COMPONENTS_CARDS"):
            self.assertEqual(
                self.light_vars.get("--md-comp-outlined-card-container-shape"),
                "var(--md-sys-shape-corner-medium)",
            )
            self.assertEqual(
                self.light_vars.get("--md-comp-filled-card-container-color"),
                "var(--md-sys-color-surface-container-highest)",
            )
            self.assertEqual(
                self.light_vars.get("--md-comp-elevated-card-container-color"),
                "var(--md-sys-color-surface-container-low)",
            )
            self.assertEqual(
                self.light_vars.get("--md-comp-elevated-card-container-elevation"),
                "var(--md-sys-elevation-level1)",
            )

        with self.spec_context(spec_key="COMPONENTS_DIVIDER"):
            self.assertEqual(self.light_vars.get("--md-comp-divider-color"), "var(--md-sys-color-outline-variant)")
            self.assertEqual(self.light_vars.get("--md-comp-divider-thickness"), "1px")

    @md3_conformance(spec_key="TYPOGRAPHY_TYPESCALE_TOKENS")
    def test_playwright_computed_typescale_conformance(self):
        """Uses Playwright getComputedStyle to verify all 15 MD3 typescale classes render with exact px sizes."""
        expected_scales = {
            "display-large": ("57px", "64px", "400"),
            "display-medium": ("45px", "52px", "400"),
            "display-small": ("36px", "44px", "400"),
            "headline-large": ("32px", "40px", "400"),
            "headline-medium": ("28px", "36px", "400"),
            "headline-small": ("24px", "32px", "400"),
            "title-large": ("22px", "28px", "400"),
            "title-medium": ("16px", "24px", "500"),
            "title-small": ("14px", "20px", "500"),
            "body-large": ("16px", "24px", "400"),
            "body-medium": ("14px", "20px", "400"),
            "body-small": ("12px", "16px", "400"),
            "label-large": ("14px", "20px", "500"),
            "label-medium": ("12px", "16px", "500"),
            "label-small": ("11px", "16px", "500"),
        }
        with self.run_playwright() as page:
            page.goto(f"{self.url}/index.html")
            for scale, (exp_size, exp_lh, exp_weight) in expected_scales.items():
                computed = page.evaluate(
                    f"""() => {{
                        const el = document.getElementById('ts-{scale}');
                        const cs = window.getComputedStyle(el);
                        return {{
                            fontSize: cs.fontSize,
                            lineHeight: cs.lineHeight,
                            fontWeight: cs.fontWeight,
                        }};
                    }}"""
                )
                self.assertEqual(
                    computed["fontSize"],
                    exp_size,
                    f"Typescale {scale} fontSize: expected {exp_size}, got {computed['fontSize']}",
                )
                self.assertEqual(
                    computed["lineHeight"],
                    exp_lh,
                    f"Typescale {scale} lineHeight: expected {exp_lh}, got {computed['lineHeight']}",
                )
                self.assertEqual(
                    computed["fontWeight"],
                    exp_weight,
                    f"Typescale {scale} fontWeight: expected {exp_weight}, got {computed['fontWeight']}",
                )

    def test_playwright_computed_colors_and_component_styles_light_and_dark(self):
        """Uses Playwright getComputedStyle to verify resolved tokens and component styles in light and dark modes."""
        with self.run_playwright() as page:
            page.goto(f"{self.url}/index.html")

            page.evaluate("document.documentElement.dataset.theme = 'light'")
            light_styles = page.evaluate(
                """() => {
                    const rootCs = window.getComputedStyle(document.documentElement);
                    const bodyCs = window.getComputedStyle(document.body);
                    const filledBtnCs = window.getComputedStyle(document.getElementById('btn-filled'));
                    const tonalBtnCs = window.getComputedStyle(document.getElementById('btn-tonal'));
                    const elevatedBtnCs = window.getComputedStyle(document.getElementById('btn-elevated'));
                    const outlinedCardCs = window.getComputedStyle(document.getElementById('card-outlined'));
                    const elevatedCardCs = window.getComputedStyle(document.getElementById('card-elevated'));
                    return {
                        primaryToken: rootCs.getPropertyValue('--md-sys-color-primary').trim(),
                        bodyBg: bodyCs.backgroundColor,
                        bodyColor: bodyCs.color,
                        filledBtnBg: filledBtnCs.backgroundColor,
                        filledBtnColor: filledBtnCs.color,
                        filledBtnHeight: filledBtnCs.height,
                        filledBtnRadius: filledBtnCs.borderRadius,
                        tonalBtnBg: tonalBtnCs.backgroundColor,
                        elevatedBtnBg: elevatedBtnCs.backgroundColor,
                        elevatedBtnShadow: elevatedBtnCs.boxShadow,
                        outlinedCardRadius: outlinedCardCs.borderRadius,
                        elevatedCardBg: elevatedCardCs.backgroundColor,
                        elevatedCardShadow: elevatedCardCs.boxShadow,
                    };
                }"""
            )
            with self.spec_context(spec_key="COLOR_PRIMARY"):
                self.assertEqual(light_styles["primaryToken"], "#0b57d0")
            with self.spec_context(spec_key="COLOR_SURFACE"):
                self.assertEqual(light_styles["bodyBg"], "rgb(255, 255, 255)")
                self.assertEqual(light_styles["bodyColor"], "rgb(31, 31, 31)")
            with self.spec_context(spec_key="COMPONENTS_BUTTON_VARIANTS"):
                self.assertEqual(light_styles["filledBtnBg"], "rgb(11, 87, 208)")
                self.assertEqual(light_styles["filledBtnColor"], "rgb(255, 255, 255)")
                self.assertEqual(light_styles["tonalBtnBg"], "rgb(194, 231, 255)")
                self.assertEqual(light_styles["elevatedBtnBg"], "rgb(248, 250, 253)")
                self.assertNotEqual(light_styles["elevatedBtnShadow"], "none")
            with self.spec_context(spec_key="DENSITY_BUTTONS"):
                self.assertEqual(light_styles["filledBtnHeight"], "32px")
                self.assertEqual(light_styles["filledBtnRadius"], "9999px")
            with self.spec_context(spec_key="COMPONENTS_CARDS"):
                self.assertEqual(light_styles["outlinedCardRadius"], "12px")
                self.assertEqual(light_styles["elevatedCardBg"], "rgb(248, 250, 253)")
                self.assertNotEqual(light_styles["elevatedCardShadow"], "none")

            # Toggle to dark mode via <md3-theme-toggle>
            page.locator("md3-theme-toggle").click()
            dark_styles = page.evaluate(
                """() => {
                    const rootCs = window.getComputedStyle(document.documentElement);
                    const bodyCs = window.getComputedStyle(document.body);
                    const filledBtnCs = window.getComputedStyle(document.getElementById('btn-filled'));
                    const tonalBtnCs = window.getComputedStyle(document.getElementById('btn-tonal'));
                    const elevatedBtnCs = window.getComputedStyle(document.getElementById('btn-elevated'));
                    return {
                        primaryToken: rootCs.getPropertyValue('--md-sys-color-primary').trim(),
                        bodyBg: bodyCs.backgroundColor,
                        bodyColor: bodyCs.color,
                        filledBtnBg: filledBtnCs.backgroundColor,
                        filledBtnColor: filledBtnCs.color,
                        tonalBtnBg: tonalBtnCs.backgroundColor,
                        elevatedBtnBg: elevatedBtnCs.backgroundColor,
                    };
                }"""
            )
            with self.spec_context(spec_key="COLOR_THEME_SWITCHING"):
                self.assertEqual(dark_styles["primaryToken"], "#a8c7fa")
                self.assertEqual(dark_styles["bodyBg"], "rgb(19, 19, 20)")
                self.assertEqual(dark_styles["bodyColor"], "rgb(227, 227, 227)")
                self.assertEqual(dark_styles["filledBtnBg"], "rgb(168, 199, 250)")
                self.assertEqual(dark_styles["filledBtnColor"], "rgb(6, 46, 111)")
                self.assertEqual(dark_styles["tonalBtnBg"], "rgb(0, 74, 119)")
                self.assertEqual(dark_styles["elevatedBtnBg"], "rgb(27, 27, 27)")


if __name__ == "__main__":
    unittest.main()
