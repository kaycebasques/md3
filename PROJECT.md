# Material Design 3 (MD3) Sphinx Theme: Project Overview

## 1. Executive Summary & Goals

This project provides an elegant, complete, production-grade [Sphinx](https://www.sphinx-doc.org) HTML documentation theme compliant with Google's **Material Design 3 (MD3)** design system.

The project is published to PyPI as a Python wheel (`md3-0.1.0-py3-none-any.whl`), built and orchestrated hermetically using [Bazel](https://bazel.build) via `./bazelisk`. It provides theme and extension registration (`extensions = ["md3"]` / `html_theme = "md3"`, with an alias for `material3`).

### Primary Objectives

1. **Strict Material Design 3 Compliance**:
   - Built on official Google Material Design 3 v35.0+ design tokens from the Design System Database (DSDB) and Carbon CMS specifications: reference palettes (`--md-ref-palette-*`), system color roles (`--md-sys-color-*`), system typography typescales (`--md-sys-typescale-*`), corner radius shapes (`--md-sys-shape-corner-*`), elevation levels (`--md-sys-elevation-level*`), motion curves (`--md-sys-motion-*`), state layers (`--md-sys-state-*`), 4dp spatial measurement tokens (`--md-sys-measurement-space*`), and component tokens (`--md-comp-*`).
   - Audited and validated against official MD3 specifications published at [`https://m3.material.io/`](https://m3.material.io/).
2. **High Information Density (Anti-Bloat Philosophy)**:
   - Optimized specifically for technical documentation (similar to Stripe, MDN, Mintlify).
   - Uses MD3's official **compact and extra-small (`xsmall`)** component specifications (`--md-density-scale: -2`), ensuring compact button heights (32px), dense navigation tree items (32px), compact search bar (36px), compact icon buttons (32px), compact chips (32px), and dense data tables (8px vertical padding)—avoiding oversized touch targets on desktop viewports.
3. **Modern 3-Column Documentation Architecture & Large-Site Scalability**:
   - **Top-Level Navigation Tabs (`<md3-nav-tabs>`)**: Primary navigation tab bar (`40px` compact height) directly below the header for switching between top-level documentation sections.
   - **Column 1 (Left Sidebar)**: Sticky 256px progressive-disclosure navigation drawer (`<md3-sidebar>`) showing **strictly one hierarchy level at a time**, with ancestor drill-up back-links, child chevron indicators, MD3 pill active indicators (`secondary-container` fill, `on-secondary-container` text), and a live filter input (`#sidebar-filter-input`) when a section has 8+ items.
   - **Column 2 (Center Content)**: 820px readable content container (~60–75ch optimal line length) with breadcrumbs, typography hierarchy, callout admonitions, dividers, and previous/next pagination cards.
   - **Column 3 (Right On-Page TOC)**: Sticky on-page table of contents with `IntersectionObserver` scrollspy heading tracking and smooth back-to-top action.
4. **Dedicated Component Docs & Dual-Target Conformance Deeplinks**:
   - 18 individual component documentation pages under `docs/components/*.rst` explaining how each component conforms to the MD3 specification and linking to `https://m3.material.io/`.
   - 12 automated test suites executed via Bazel and Playwright in headless Chromium.
   - Every single test assertion maps via `tests/md3_spec.py` (54 catalog entries) to **both** a section in our component docs (`components/<slug>.html#<section-id>`) and a verified canonical URL and exact section anchor (`https://m3.material.io/<tab_path>#<pageContentBlockCanonId>`) cross-checked against `https://m3.material.io/sitemap.xml` and Carbon CMS page payloads.
   - Multi-domain test methods wrap each assertion group in a granular `with self.spec_context(spec_key="...")` block so that any failure cites the exact component doc section and MD3 specification rule being tested.

---

## 2. Core Architectural Pillars

### 2.1 Material Design 3 Token System (`md3/components/app.css`)

The stylesheet implements a complete three-tier token hierarchy (Reference -> System -> Component) derived from official Material Design 3 tokens:

* **Reference Palettes (`--md-ref-palette-*`)**:
  - Full 13-tone tonal palettes (`0`, `10`, `20`, `30`, `40`, `50`, `60`, `70`, `80`, `90`, `95`, `99`, `100`) for `primary`, `secondary`, `tertiary`, `neutral`, `neutral-variant`, and `error`.
* **System Color Roles (`--md-sys-color-*`)**:
  - Both **Light** (`:root`) and **Dark** (`[data-theme="dark"]`) palettes covering all 45+ roles:
    - Accents: `primary`, `on-primary`, `primary-container`, `on-primary-container`, `secondary`, `on-secondary`, `secondary-container`, `on-secondary-container`, `tertiary`, `on-tertiary`, `tertiary-container`, `on-tertiary-container`, `error`, `on-error`, `error-container`, `on-error-container`.
    - Surfaces: `surface`, `on-surface`, `surface-variant`, `on-surface-variant`, `surface-dim`, `surface-bright`, `surface-tint`.
    - Surface Containers: `surface-container-lowest`, `surface-container-low`, `surface-container`, `surface-container-high`, `surface-container-highest`.
    - Outlines & Utility: `outline`, `outline-variant`, `shadow`, `scrim`.
    - Fixed Accents: `primary-fixed`, `primary-fixed-dim`, `on-primary-fixed`, `on-primary-fixed-variant` (and corresponding `secondary-fixed*`, `tertiary-fixed*`).
    - Inverse Roles: `inverse-surface`, `inverse-on-surface`, `inverse-primary`.
* **WCAG 2.1 AA Contrast Guarantee**:
  - Foreground text and icon tokens paired with container backgrounds satisfy at least 4.5:1 contrast ratio in both light and dark themes (including primary, secondary, tertiary, error, surface, and inverse pairs).
* **Typography Typescales (`--md-sys-typescale-*` and `.md-typescale-*`)**:
  - All 15 MD3 typography styles: Display (L/M/S), Headline (L/M/S), Title (L/M/S), Body (L/M/S), Label (L/M/S).
  - Documentation headings map onto semantic scales: `h1` (Headline Large 32px/40px), `h2` (Headline Medium 28px/36px), `h3` (Headline Small 24px/32px), `h4` (Title Large 22px/28px), `h5` (Title Medium 16px/24px), `h6` (Title Small 14px/20px).
  - Data tables apply `font-variant-numeric: tabular-nums` so numeric columns align vertically.
* **Shape Scale (`--md-sys-shape-corner-*`)**:
  - Complete 10-step MD3 shape scale: `none` (`0px`), `extra-small` (`4px`), `small` (`8px`), `medium` (`12px`), `large` (`16px`), `large-increased` (`20px`), `extra-large` (`28px`), `extra-large-increased` (`32px`), `extra-extra-large` (`48px`), `full` (`9999px`).
  - Interactive buttons (`.md3-btn`) and icon buttons (`.md3-icon-btn`) morph their corner shape from full pill (`9999px`) to `small` (`8px`) on `:active` press per the MD3 Expressive Button spec (`--md-comp-button-xsmall-pressed-container-shape`).
* **Elevation & Shadows (`--md-sys-elevation-level*`)**:
  - 6 discrete elevation levels (`level0` through `level5`) using paired key and ambient box-shadows.
* **Motion Physics (`--md-sys-motion-*`)**:
  - Easing curves: `standard` (`cubic-bezier(0.2, 0.0, 0, 1.0)`), `standard-decelerate` (`cubic-bezier(0, 0, 0, 1)`), `standard-accelerate` (`cubic-bezier(0.3, 0, 1, 1)`), `emphasized` (`cubic-bezier(0.2, 0.0, 0, 1.0)`), `emphasized-decelerate` (`cubic-bezier(0.05, 0.7, 0.1, 1.0)`), `emphasized-accelerate` (`cubic-bezier(0.3, 0.0, 0.8, 0.15)`).
  - Durations: `short1` (`50ms`) through `long2` (`500ms`).
* **State Layers & Focus Indicator (`--md-sys-state-*`)**:
  - Hover: `0.08` (8%)
  - Focus: `0.10` (10%) with `3px` focus ring thickness (`--md-sys-state-focus-indicator-thickness`), `2px` outer offset (`--md-sys-state-focus-indicator-outer-offset`), and `-3px` inner offset (`--md-sys-state-focus-indicator-inner-offset`).
  - Pressed: `0.10` (10%)
  - Dragged: `0.16` (16%)
  - Disabled: `0.38` (38% content opacity via `--md-sys-state-disabled-state-layer-opacity`).
* **Spatial Grid Measurements (`--md-sys-measurement-space*`)**:
  - All 18 official MD3 system measurement tokens (`space0: 0px` through `space900: 72px`) aligned with the 4dp/8dp baseline grid.

---

### 2.2 Information Density Philosophy

In developer documentation, oversized buttons and excessive whitespace hinder readability and navigation velocity. This theme implements MD3's compact density guidelines (`--md-density-scale: -2`):

| UI Component | Standard MD3 Mobile | MD3 Compact Documentation (This Theme) | Token / Rule |
| :--- | :--- | :--- | :--- |
| **Buttons** | 48px - 56px height | **32px height** (`xsmall`) / **40px** (`small`) | `--md-comp-button-xsmall-container-height` |
| **Navigation Items** | 56px height | **32px height** pill | `--md-comp-navigation-drawer-active-indicator-height` |
| **Search Bar** | 56px height | **36px height** | `--md-comp-search-bar-container-height` |
| **Icon Buttons** | 48px x 48px | **32px x 32px** (20px icon) | `--md-comp-icon-button-xsmall-container-height` |
| **Chips** | 40px - 48px | **32px height** | `--md-comp-assist-chip-container-height` |
| **Top App Bar** | 64px - 112px | **56px height** (Small App Bar) | `--md-comp-top-app-bar-small-container-height` |
| **Table Cells** | 16px - 20px padding | **8px vertical padding** | `--md-comp-data-table-cell-vertical-space` |

---

### 2.3 Responsive Window Size Classes & Layout (`md3/layout.html`, `md3/components/app.css`)

The layout container adapts dynamically based on official MD3 window size class breakpoints:

* **Large & Extra-Large Window Size Classes (`>=1200px`)**:
  - Full 3-pane documentation layout:
    - Pane 1: Persistent Left Navigation Drawer (`<md3-sidebar>`, `260px` width).
    - Pane 2: Center Main Content (`<main id="main">`, `max-width: 820px`).
    - Pane 3: Sticky Right On-Page Table of Contents (`<md3-toc>`, `220px` width).
* **Expanded Window Size Class (`840px – 1199px`)**:
  - Right on-page TOC collapses (`@media (max-width: 1199px)`) to preserve comfortable reading width for the center article pane while keeping the left navigation drawer persistent.
* **Compact (`<600px`) & Medium (`600px – 839px`) Window Size Classes (`<840px`)**:
  - Left navigation sidebar converts into an off-canvas modal sliding drawer (`@media (max-width: 839px)`, `transform: translateX(-100%)`, `box-shadow: var(--md-sys-elevation-level1)` when open).
  - Scrim backdrop (`#md3-backdrop`) dims background content with `0.32` opacity (`--md-comp-navigation-drawer-scrim-opacity`).
  - Hamburger toggle button (`#drawer-toggle`) manages drawer state with `aria-expanded` and restores focus to the trigger when closed.

---

### 2.4 Web Components Runtime (`md3/components/app.js`)

All interactive functionality is implemented as native Web Components with zero external JavaScript dependencies:

1. **`<md3-app>`**: Root custom element orchestrating theme initialization and code copy button upgrades.
2. **`<md3-top-app-bar>`**: Sticky top app bar that uses `--md-comp-top-app-bar-small-container-color` (`surface`) and Level 0 elevation at rest, and transitions to `--md-comp-top-app-bar-small-on-scroll-container-color` (`surface-container`) with Level 2 elevation (`var(--md-sys-elevation-level2)`) when scrolled (`window.scrollY > 4`).
3. **`<md3-sidebar>`**: Responsive navigation drawer supporting persistent desktop display (`>=840px`), modal drawer behavior (`<840px`), `Escape`/scrim dismissal, and focus restoration to `#drawer-toggle`.
4. **`<md3-toc>`**: On-page table of contents with `IntersectionObserver` scrollspy and smooth back-to-top scrolling.
5. **`<md3-search>`**: Client-side modal `<dialog>` (`min-width: 280px`, `max-width: 560px`, `28px` extra-large corner radius, `0.32` scrim backdrop) with instant live filtering, `⌘K` and `/` keyboard shortcuts, `Escape` dismissal, and focus restoration.
6. **`<md3-copy-button>`**: 1-click clipboard copy button injected into Sphinx code blocks with accessible `aria-label`, `title` tooltip, and visual copy confirmation.
7. **`<md3-theme-toggle>`**: Accessible icon button (`aria-label`, `title`, `aria-pressed`) switching light/dark themes with `localStorage` persistence and Pygments stylesheet synchronization.

---

### 2.5 Sphinx Technical Elements & MD3 Web Guidelines

* **Inline Links vs. Buttons**: Per MD3 Web Link guidelines, inline hyperlinks inside `.md3-article` are underlined (`text-decoration: underline; text-underline-offset: 2px`) so links are distinguishable without relying on color alone, whereas buttons (`.md3-btn`) and `.headerlink` pilcrows are not underlined.
* **Button & Card Variants**: Supports filled (`.md3-btn--filled`), tonal (`.md3-btn--tonal`), elevated (`.md3-btn--elevated`), outlined (`.md3-btn--outlined`), and text (`.md3-btn--text`) buttons, as well as outlined (`.md3-card`), elevated (`.md3-card--elevated`), and filled (`.md3-card--filled`) cards.
* **Dividers**: `hr.docutils` and `.md3-divider` use `--md-comp-divider-thickness` (`1px`) and `--md-comp-divider-color` (`outline-variant`).
* **Admonitions**: Callouts (`note`, `tip`, `warning`, `danger`) use MD3 surface container colors, `12px` medium corner shape tokens, and semantic left accent borders (`primary`, `tertiary`, `error`).
* **Pygments Syntax Highlighting**: Dual stylesheets (`pygments.css` and `pygments_dark.css`) loaded simultaneously and synchronized via media query manipulation upon theme toggle.
* **Data Tables**: `table.docutils` styled with MD3 `outline-variant` borders, `surface-container-low` header backgrounds, compact `8px` vertical cell padding, zebra striping, and `tabular-nums` alignment.
* **Pagination Cards**: Outlined interactive cards (`.md3-pagination__card`) with hover elevation and directional navigation.
* **Breadcrumbs**: Hierarchical `<nav aria-label="Breadcrumb">` trail with primary link styling and accessible separators.

---

### 2.6 Progressive Enhancement & Light DOM Rendering (`md3/layout.html`, `md3/components/app.css`, `md3/components/app.js`)

Following the architectural patterns in `~/tw`, all documentation content and navigation structures are rendered into the Light DOM at build time by Jinja templates (`md3/layout.html`), and JavaScript is used strictly for progressive enhancements:

* **Light DOM Jinja Rendering**: Global navigation (`toctree`), page table of contents (`toc`), breadcrumbs, theme selector form controls, and article content are rendered directly into the Light DOM so all content is immediately accessible when JavaScript is disabled.
* **Mobile "On this page" TOC Access**: On Compact, Medium, and Expanded viewports (`<1200px`) where the right-hand TOC column is collapsed, a compact `#toc-mobile-btn` (`popovertarget="md3-toc-mobile-menu"`) in `.md3-content-nav-bar` opens the `#md3-toc-mobile-menu` popover without JavaScript (via mouse, touch, or keyboard `Enter`/`Space`/`Escape`). When JavaScript is enabled, clicking a section link inside `#md3-toc-mobile-menu` automatically dismisses the popover.
* **No-JS Mobile Navigation Drawer**: `#drawer-toggle` (`popovertarget="md3-sidebar"`) and `#sidebar-close` (`popovertarget="md3-sidebar" popovertargetaction="hide"`) are native `<button>` controls operating `<md3-sidebar id="md3-sidebar" popover>`. When JavaScript is disabled (`.no-js`), `:root.no-js md3-sidebar:popover-open` and `:root.no-js:has(md3-sidebar:popover-open) .md3-backdrop` slide the drawer on-screen and display the full-viewport scrim backdrop (`inset: 0`), supporting mouse clicks, backdrop light-dismiss, and keyboard (`Enter`/`Space`/`Escape`).
* **No-JS Theme Switching**: `<md3-theme-toggle>` wraps a native `<button id="theme-menu-btn" popovertarget="md3-theme-menu">` and `<nav id="md3-theme-menu" popover>` with `<input type="radio" name="theme" value="light|dark">` controls. Without JavaScript, `:root.no-js:has(#md3-theme-menu input[name="theme"][value="dark"]:checked)` and `:root.no-js:has(#md3-theme-menu input[name="theme"][value="light"]:checked)` switch all MD3 color tokens.
* **Semantic Back-to-Top Link**: `#back-to-top` is rendered as `<a href="#body">` so it scrolls back to the top of the page without JavaScript.

---

## 3. Specification Conformance & Deeplinking Architecture

To ensure strict compliance with Material Design 3, every conformance test connects to the official specification on `https://m3.material.io/`.

### 3.1 Spec Catalog (`tests/md3_spec.py`)

A centralized catalog (`MD3_SPECS`, 67 verified entries) maps every tested aspect of the design system to its canonical URL and exact section block UUID (`#<pageContentBlockCanonId>`) on `https://m3.material.io/`:

```python
MD3_SPECS = {
    "COLOR_ROLES_OVERVIEW": {
        "url": "https://m3.material.io/styles/color/roles#e9fc5b00-8355-4641-b35f-58b0bac639f3",
        "section": "Styles > Color > Roles > What are color roles?",
        "requirement": "Color roles map UI elements to semantic color tokens across light and dark themes.",
    },
    "COMPONENTS_TOP_APP_BAR_SCROLL": {
        "url": "https://m3.material.io/components/app-bars/specs#9975d8e5-f69e-48bd-865e-af3c8eeba1d3",
        "section": "Components > App bars > Specs > Color > Scroll states",
        "requirement": "At rest, the top app bar uses surface container color and Level 0 elevation; on scroll (.scrolled), it transitions to surface-container color and Level 2 elevation.",
    },
    ...
}
```

Every URL path is verified against `https://m3.material.io/sitemap.xml`, and every `#<uuid>` fragment is verified against the `pageContentBlockCanonId` entries in the Carbon CMS page JSON for that exact route. Calling `format_md3_failure()` or `self.spec_context()` with an unknown `spec_key` immediately raises a `KeyError`.

### 3.2 Failure Deeplink Format

When an assertion fails inside `@md3_conformance(spec_key="...")` or `with self.spec_context(spec_key="..."):`, the test runner prints a structured failure banner:

```
================================================================================
MATERIAL DESIGN 3 (MD3) SPECIFICATION CONFORMANCE FAILURE
--------------------------------------------------------------------------------
  Spec Section:  Components > App bars > Specs > Color > Scroll states
  Spec Deeplink: https://m3.material.io/components/app-bars/specs#9975d8e5-f69e-48bd-865e-af3c8eeba1d3
  Requirement:   At rest, the top app bar uses surface container color and Level 0 elevation; on scroll (.scrolled), it transitions to surface-container color and Level 2 elevation.
================================================================================
```

This guarantees that reviewing engineers and autonomous agents can click directly into the exact MD3 documentation section to see what requirement was violated.

---

## 4. Test Suite Overview

All tests are located in `tests/` and run hermetically through Bazel:

| Target | Description | Conformance Scope |
| :--- | :--- | :--- |
| `//tests:test_md3_tokens` | Static CSS & Playwright computed styles | Reference palettes, light/dark color roles, WCAG contrast, shapes, elevation, typescales, motion, spacing, component tokens |
| `//tests:test_md3_density` | Rendered component dimensions in Playwright | 32px buttons, 32px nav items, 36px search, 32px chips/icon-buttons, 56px app bar, 8px table padding, pressed shape morph |
| `//tests:test_md3_layout` | Viewport responsiveness in Playwright | Large 3-pane (`1280px`), Expanded 2-pane (`1024px`), Medium/Compact modal drawer (`700px`/`480px`), focus restoration, line width |
| `//tests:test_md3_components` | Custom element runtime interaction | Component registration, top app bar scroll elevation/color transition, theme toggle, code copy, search dialog specs (`280–560px`), TOC scrollspy |
| `//tests:test_md3_sphinx_elements` | Sphinx docutils & Pygments rendering | Admonition containers, light/dark Pygments CSS, `tabular-nums` tables, cards, dividers, underlined inline links, pagination, breadcrumbs |
| `//tests:test_md3_accessibility` | Keyboard nav & ARIA semantics | High-contrast focus rings (`3px`/`2px`/`-3px`), state layers, 38% disabled opacity, ARIA landmark roles, icon button tooltips |
| `//tests:test_md3_progressive_enhancement` | No-JS & progressive enhancement verification | Mobile TOC popover, no-JS mobile nav drawer (mouse & keyboard), no-JS theme switching (`:has()`), no-JS back-to-top, Light DOM rendering |
| `//tests:test_md3_navigation` | Large-site navigation scalability | `<md3-nav-tabs>` active hierarchy & keyboard navigation, 1-level progressive disclosure, live filtering, in-place JS graph traversal |
| `//tests:test_md3_universal_header` | Universal header & subsite postprocessing | Doxygen & Rustdoc sentinel injection, cross-subsite theme sync, universal breadcrumbs, subsite mobile drawer, skip link, Pagefind subsite indexing |
| `//tests:test_md3_deeplinks` | Meta-verification of spec deeplinks | Validates all 78 catalog URLs & UUID fragments, `KeyError` on invalid keys, and per-assertion `spec_context` attribution |
| `//tests:test_app` | Sphinx build verification | Verifies theme builds under both `md3` and `material3` configurations |
| `//tests:test_html` | Base HTML structure | Verifies DOCTYPE, meta tags, and document title |
| `//tests:test_runtime` | Web Component lifecycle | Verifies basic runtime bootstrapping |

---

## 5. Repository Structure

```
.
├── .bazelrc                   # Bazel flags (Python toolchains, explicit init_py)
├── BUILD.bazel                # Root targets (:wheel, :serve, :ls, :requirements)
├── MODULE.bazel               # Bzlmod dependencies (rules_python, rules_playwright, sphinxdocs)
├── PROJECT.md                 # This specification & architecture guide
├── README.md                  # User-facing theme documentation & quick start
├── docs/                      # Sample documentation project using md3
│   ├── BUILD.bazel            # Sphinx docs build targets
│   ├── conf.py                # Sphinx configuration (project = "Material Design 3")
│   ├── index.rst              # Documentation home page
│   ├── tokens.rst             # Design tokens reference page
│   └── components.rst         # Component specimens page
├── md3/                       # Theme implementation & asset distribution
│   ├── BUILD.bazel            # py_library, py_package, and py_wheel targets
│   ├── __init__.py            # Sphinx extension setup, subsite postprocessor, and Pagefind indexer
│   ├── theme.toml             # Sphinx theme definition
│   ├── layout.html            # Main Jinja2 layout (3-column scaffold + Web Components)
│   ├── page.html              # Article page template
│   ├── search.html            # Dedicated search fallback template
│   ├── genindex.html          # General index template
│   └── components/
│       ├── app.css            # MD3 Design Token System & high-density styling
│       └── app.js             # Native Web Components runtime
└── tests/                     # Conformance test suite
    ├── BUILD.bazel            # Bazel py_test targets and test_suite
    ├── harness.py             # SphinxTestBase test harness with in-process HTTP server
    ├── md3_spec.py            # MD3 spec catalog (78 verified deeplinks), failure banners, and decorators
    ├── test_app.py            # Theme loading & extension tests
    ├── test_html.py           # Base HTML tests
    ├── test_runtime.py        # Base runtime tests
    ├── test_md3_tokens.py     # Token & computed style conformance tests
    ├── test_md3_density.py    # Compact information density & shape morph tests
    ├── test_md3_layout.py     # Window size class & responsive drawer tests
    ├── test_md3_components.py # Interactive Web Component & scroll state tests
    ├── test_md3_navigation.py # Top-level tabs & 1-level progressive disclosure tests
    ├── test_md3_progressive_enhancement.py # No-JS & progressive enhancement tests
    ├── test_md3_sphinx_elements.py # Admonitions, tables, links, cards, dividers, Pygments tests
    ├── test_md3_accessibility.py   # Focus rings, state layers, disabled states, tooltips, ARIA tests
    ├── test_md3_universal_header.py # Universal header & Doxygen/Rustdoc postprocessing tests
    └── test_md3_deeplinks.py  # Conformance deeplink & context attribution validation tests
```

---

## 6. How to Build, Test, and Verify

Always use the `./bazelisk` wrapper at the repository root:

### Run All Conformance Tests
```bash
./bazelisk test //tests --nocache_test_results
```

### Run a Specific Conformance Test Target
```bash
./bazelisk test //tests:test_md3_tokens --test_output=all
./bazelisk test //tests:test_md3_density --test_output=all
./bazelisk test //tests:test_md3_layout --test_output=all
```

### Build Documentation
```bash
./bazelisk build //docs
# View output at bazel-bin/docs/docs/_build/html/index.html
```

### Serve Documentation Locally
```bash
./bazelisk run :serve
```

### Build Python Wheel Package
```bash
./bazelisk build :wheel
# Inspect generated wheel:
unzip -l bazel-bin/md3/md3-0.1.0-py3-none-any.whl
```

### Build Everything Across the Workspace
```bash
./bazelisk build //...
```

---

## 7. Reviewer Checklist for Future Changes

When extending or modifying the theme, verify the following:

- [ ] **Information Density**: Buttons must remain compact (height <= 36px, target 32px), nav items <= 36px (target 32px), search bar <= 40px (target 36px), table vertical padding <= 12px (target 8px).
- [ ] **Token System**: All colors, shapes, spacings, and elevations must reference `--md-sys-*`, `--md-comp-*`, or `--md-ref-palette-*` tokens; do not hardcode ad-hoc hex colors. Both Light and Dark theme definitions must be maintained.
- [ ] **WCAG AA Contrast**: Ensure any foreground/background color pair satisfies at least 4.5:1 contrast.
- [ ] **Web Components**: Interactive features must be built as Custom Elements in `app.js` and declared in `md3/layout.html`.
- [ ] **Conformance Deeplinks**: Any new conformance assertion must use `@md3_conformance(spec_key="...")` or `with self.spec_context(spec_key="..."):` pointing to a verified `https://m3.material.io/<tab_path>#<pageContentBlockCanonId>` URL in `tests/md3_spec.py`.
- [ ] **Hermetic Verification**: All tests in `//tests` must pass with `./bazelisk test //tests --nocache_test_results`.
