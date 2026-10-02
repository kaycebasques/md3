# Material Design 3 (MD3) Sphinx Theme

An elegant, high-density, complete Sphinx documentation theme compliant with Google's **Material Design 3** design system.

## Highlights

* **3-Column Architecture & Large-Site Navigation**: Stripe / MDN / Mintlify style documentation layout designed to scale to multi-thousand-page documentation sites:
  * **Top-Level Navigation Tabs (`<md3-nav-tabs>`)**: Primary section tabs (`40px` compact height, `3px` active indicator pill, roving arrow-key navigation) below the top app bar for instant switching across top-level site sections.
  * **Progressive Disclosure Left Sidebar (`<md3-sidebar>`)**: Displays **one hierarchy level at a time** with ancestor drill-up back-links, child chevron indicators, MD3 pill active indicators, and a live section filter (`#sidebar-filter-input`) for sections with 8+ items.
  * **Center Content**: Readable documentation container with breadcrumbs, typography scales, admonitions, and pagination cards.
  * **Right On-Page TOC**: Interactive table of contents with scrollspy active heading tracking and smooth scrolling.
* **Component Documentation & Conformance Deeplinking**:
  * Every component and token family has its own dedicated documentation page under `docs/components/` explaining how it conforms to the Material Design 3 specification and linking directly to the relevant section on `https://m3.material.io/`.
  * When an MD3 conformance test fails, its assertion output deeplinks directly to both the component documentation section (`components/<slug>.html#<section-id>`) and the official `m3.material.io` specification anchor.
* **Information Density**: Implements MD3 compact density (scale `-2`):
  * Compact button heights (32px / 28px) avoiding bulky/gigantic buttons.
  * Dense navigation items (32px height).
  * Compact search bar (36px height) and icon buttons (32px).
  * Optimized whitespace and compact data tables.
* **Complete MD3 Design Tokens**:
  * **Color Roles**: Full baseline palette (primary, secondary, tertiary, surface containers, error) for both **Light** and **Dark** themes.
  * **Typography**: All 15 MD3 typescales (Display, Headline, Title, Body, Label in large, medium, small).
  * **Shapes**: MD3 corner radii from 0px to 9999px full pills.
  * **Elevation**: 6-level elevation system with ambient and key shadows.
  * **Motion**: MD3 standard and emphasized easing curves and transition durations.
* **Web Components & Runtime**:
  * `<md3-app>` / `<paz-app>`: Root application container.
  * `<md3-top-app-bar>`: Sticky small top app bar with scroll elevation states.
  * `<md3-nav-tabs>`: Primary section navigation tabs with keyboard arrow-key navigation.
  * `<md3-sidebar>`: Progressive disclosure navigation drawer with live section filtering.
  * `<md3-theme-toggle>`: Light / Dark mode toggle with preference persistence in `localStorage`.
  * `<md3-search>`: Fast modal search dialog with `⌘K` / `/` keyboard shortcuts.
  * `<md3-copy-button>`: 1-click code block copying with visual feedback.
  * `<md3-toc>`: Scrollspy table of contents with back-to-top action.
  * Mobile responsive sliding drawer with scrim backdrop.
* **Progressive Enhancement & No-JS Architecture**:
  * **Zero-JS Core Functionality**: All critical documentation reading and navigation features function completely without JavaScript (with both mouse/touch and keyboard):
    * Navigation drawer opening and closing on mobile/tablet viewports via native HTML `<button popovertarget="md3-sidebar">` controls.
    * Mobile access to the "On this page" table of contents via native HTML Popover API (`popover`, `popovertarget`).
    * Light and dark theme switching via a native HTML popover menu, form radio controls, and CSS `:has()`.
    * Back-to-top navigation via a semantic `<a href="#body">` link.
  * **Light DOM Rendering**: All layouts, navigation hierarchies, tables of contents, breadcrumbs, and content are rendered directly into the Light DOM using Jinja templates rather than client-side JavaScript templates.
  * **JavaScript as Enhancement Only**: JavaScript is strictly reserved for non-essential progressive enhancements (such as `⌘K` search dialog shortcuts, scrollspy heading tracking, focus management, code copy buttons, live sidebar filtering, and automatic popover dismissal on link selection).

## Quick Start

In your Sphinx project's `conf.py`:

```python
extensions = ["md3"]
html_theme = "md3"

# Optional theme options
html_theme_options = {
    "site_title": "My Project Docs",
    "nav_title": "Documentation",
    "repo_url": "https://github.com/my-org/my-project",
    "show_toc": True,
}
```

## Bazel Commands

### Build Everything
```bash
./bazelisk build //...
```

### Run Tests
```bash
./bazelisk test //tests
```

### Build Documentation
```bash
./bazelisk build //docs
# View build output at bazel-bin/docs/docs/_build/html/index.html
```

### Build Wheel Package
```bash
./bazelisk build :wheel
# Generates wheel at bazel-bin/paz/md3-0.1.0-py3-none-any.whl
```
