# md3

`md3` (also registered under the `material3` Sphinx theme name) is a Material Design 3 (MD3) Sphinx HTML theme, published to PyPI as a wheel.

## Goals & Architectural Approach

1. **From-Scratch Material Design 3 Conformance (`inherit = "none"`)**:
   * The theme does not inherit from any built-in Sphinx theme, not even `basic` (`inherit = "none"` in `md3/theme.toml`).
   * All styling in `md3/components/app.css` is built on a 3-tier Material Design 3 token architecture: Reference palettes (`--md-ref-palette-*`), System tokens (`--md-sys-color-*`, `--md-sys-typescale-*`, `--md-sys-shape-corner-*`, `--md-sys-elevation-*`, `--md-sys-motion-*`, `--md-sys-state-*`, `--md-sys-measurement-*`), and Component tokens (`--md-comp-*`), supporting both Light and Dark themes with WCAG 2.1 AA contrast (`>= 4.5:1`).

2. **High Information Density (`--md-density-scale: -2`)**:
   * Designed specifically for technical documentation (informed by Pigweed's integration in `~/wt/theme` and `~/tw`) using MD3's official compact / extra-small (`xsmall`) component specifications so desktop viewports aren't bloated by mobile-sized touch targets:
     * `56px` small top app bar (`<md3-top-app-bar>`), `36px` search bar trigger, and `36px` top-level navigation tabs (`<md3-nav-tabs>`).
     * `32px` buttons, icon buttons, chips, and navigation drawer items (`260px` sidebar width).
     * `8px` vertical padding and `tabular-nums` alignment in data tables.

3. **Light DOM Server-Side Rendering & Progressive Enhancement (`:root.no-js`)**:
   * All page content, navigation hierarchies, on-page table of contents, breadcrumbs, and theme controls are rendered directly into the Light DOM at build time by Jinja2 (`md3/layout.html`)—never hidden inside Shadow DOM or requiring client-side JS to render.
   * **When JavaScript is disabled (`:root.no-js`)**:
     * Every page is 100% readable, navigable, and themeable.
     * Mobile navigation drawer (`<md3-sidebar id="md3-sidebar" popover>`) and mobile "On this page" TOC (`#md3-toc-mobile-menu[popover]`) open and close natively via the HTML5 `popover` / `popovertarget` API and CSS `:has()` backdrop rules.
     * Light/Dark theme switching operates without JS via `<input type="radio" name="theme" value="light|dark">` inside `#md3-theme-menu[popover]` paired with `:root.no-js:has(#md3-theme-menu input[name="theme"][value="dark"]:checked)` CSS token overrides.
     * Sidebar navigation links (including `<- Ancestor` back-links and section links) operate as standard multi-page `<a href="...">` links.
   * **When JavaScript is enabled (`md3/components/app.js`)**:
     * Native Custom Elements (`<md3-app>`, `<md3-top-app-bar>`, `<md3-nav-tabs>`, `<md3-sidebar>`, `<md3-toc>`, `<md3-search>`, `<md3-theme-toggle>`, `<md3-copy-button>`) progressively enhance the existing Light DOM in place.
     * Documented in `docs/components/progressive-enhancement.rst` and tested in `tests/test_md3_progressive_enhancement.py` and `tests/test_md3_navigation.py`.

4. **Large-Site Navigation Scalability (Top-Level Tabs + 1-Level Progressive Disclosure + In-Place Graph Traversal)**:
   * To prevent overwhelmingly long left sidebars on large documentation sites (a key pain point identified in `~/wt/theme`):
     * **Top-Level Navigation Tabs (`<md3-nav-tabs>`)**: Renders top-level site sections in a horizontal tab bar directly below the header with active section indicator pills and roving `ArrowRight`/`ArrowLeft`/`Home`/`End` keyboard focus.
     * **1-Level Progressive Disclosure Sidebar (`<md3-sidebar>`)**: Computes the site `toctree` graph in `md3/__init__.py` (`setup_navigation_context`) and displays **strictly one hierarchy level at a time**, with `<- Ancestor` drill-up back-links, `.has-children` chevron indicators, and a live section filter input (`#sidebar-filter-input`) when a level has `>= 8` items.
     * **In-Place Graph Traversal Without Page Loads (JS Progressive Enhancement)**: `md3/__init__.py` embeds the serialized navigation graph in `<script type="application/json" id="md3-nav-graph-data">` and annotates ancestor back-links and `.has-children` items with `data-nav-level="<docname>"`. When JS is enabled, clicking an ancestor back-link (e.g., clicking `<- Material Design 3 Sphinx Theme` while on `/components.html`) or a `.has-children` section item updates `#sidebar-nav` in-place (`Md3Sidebar.navigateToLevel()`) without loading a new page. Clicking the section header link (`.md3-sidebar__section-link`) or a leaf item navigates to that document.

5. **Full-Site Search with Pagefind & Custom MD3 UI/UX**:
   * Following the pattern in `~/tw`, `md3/__init__.py` connects `generate_pagefind_index` to Sphinx's `build-finished` event using `pagefind[extended]==1.5.2` (`pagefind.index.PagefindIndex`) to index `<article class="md3-article" data-pagefind-body>` across all built HTML pages into `<outdir>/search/pagefind.js` (temporarily injecting `id` attributes onto `<h1>`–`<h6>` tags from their `.headerlink` anchors during indexing so Pagefind `sub_results` deep-link to exact `#section-id` fragments).
   * Instead of using Pagefind's default prebuilt widget, `<md3-search>` (`#md3-search-dialog`) and `md3/search.html` (`initSearchPage()`) call the underlying Pagefind WebAssembly JS API (`loadPagefind()`) and render custom MD3 search result cards (`.md3-search-result-item`) with document titles, section breadcrumbs, `<mark>` highlighted excerpts (`--md-sys-color-primary-container` / `--md-sys-color-on-primary-container`), and deep-linked section chips (`.md3-search-sub-result-link`).

6. **Universal Header & Cross-Subsite Postprocessing (Doxygen & Rustdoc)**:
   * On large multi-tool documentation sites (such as Pigweed in `~/wt/theme`), `md3/__init__.py` (`postprocess_universal_header` on Sphinx's `build-finished` event) postprocesses external Doxygen (`doxygen/**`, `api/**`) and Rustdoc (`rustdoc/**`) HTML pages containing `<!-- md3-sentinel -->` or `<!-- pw-sentinel -->`.
   * Injects `<md3-top-app-bar>`, `<md3-nav-tabs>`, `<md3-search>` (`#md3-search-dialog`), `#md3-skip-link`, and `.md3-subsite-breadcrumbs` (`Home / C++ API / <Page>` and `Home / Rust API / <Page>`), along with `_static/app.css` and `_static/app.js`.
   * **Scalable Third-Party CSS Isolation (`md3/components/app.css`)**:
     * Global `box-sizing: border-box` and typography/code resets in `app.css` are scoped strictly to `md3-app` and injected MD3 chrome (`.md3-universal-header`, `.md3-search-dialog`, `.md3-skip-link`, `.md3-backdrop`) so external subsites retain their native `box-sizing` and code block styles.
     * `#md3-universal-header` uses `position: fixed; top: 0; left: 0; right: 0; width: 100%` and `body:has(#md3-universal-header)` sets `padding-top: var(--md3-universal-header-height, 128px) !important` (`92px` default; `128px` when `<md3-nav-tabs>` is present). This removes the header from `body.rustdoc`'s `display: flex; flex-direction: row; flex-wrap: nowrap` flow so `nav.sidebar` and `main` remain side-by-side on desktop.
     * Doxygen `#nav-tree .arrow` explicitly preserves `box-sizing: content-box !important` without `display: flex` on `#nav-tree .item`, ensuring `navtree.js` (`createIndent`) inline `padding-left: (16 * level)px` + `width: 16px` indents expand/collapse arrows (`►`/`▼`) without overlapping `.label a` links. `#side-nav` (`width: 250px`) and `#doc-content` (`margin-left: 256px`) use non-`!important` horizontal dimensions so Doxygen's `resize.js` splitter works natively.
   * Synchronizes Light/Dark theme state across Sphinx, Doxygen (including `window.DarkModeToggle`), and Rustdoc (`localStorage.getItem('theme')`, `rustdoc-theme`, `rustdoc-use-system-theme`, `.light-mode` / `.dark-mode` classes, `data-theme` / `data-mode` attributes, OS `prefers-color-scheme` and `pageshow` bfcache listeners) and maps `--pw-color-*`, Doxygen, and Rustdoc CSS variables to MD3 system tokens (`--md-sys-color-*`).
   * Annotates Doxygen `#doc-content` and non-`src` Rustdoc `#main-content` with `data-pagefind-body` while excluding subsite navigation chrome and Rustdoc source pages (`body.rustdoc.src`) from Pagefind indexing.

7. **Per-Component Documentation & Dual-Target Conformance Test Deeplinks**:
   * Every component and architectural feature has a dedicated documentation page in `docs/components/*.rst` (19 pages under `docs/components/`, indexed in `docs/components.rst` and `docs/BUILD.bazel`).
   * Every conformance requirement in `tests/md3_spec.py` (`MD3_SPECS`, 78 entries) includes **both**:
     * `doc_url` & `doc_section`: A deeplink to the exact section in our component docs (`components/<slug>.html#<section-id>`) explaining how `md3` conforms to the spec.
     * `url` & `section`: A verified canonical deeplink (`https://m3.material.io/<route>#<uuid>`) to the official Material Design 3 specification.
   * Each section in `docs/components/*.rst` includes a matching outbound link to `https://m3.material.io/<route>#<uuid>`.
   * When any test decorated with `@md3_conformance(spec_key="...")` or using `with self.spec_context(spec_key="..."):` fails, the assertion error banner prints both `Component Doc: components/<slug>.html#<section-id>` and `Spec Deeplink: https://m3.material.io/<route>#<uuid>`.
   * `tests/test_md3_deeplinks.py` verifies at test time that every `MD3_SPECS` entry resolves to an actual `<section id="...">` in the built `//docs` HTML and that the section contains the exact `https://m3.material.io/` deeplink. Whenever you add a new spec key or component feature, update both `docs/components/*.rst` and `tests/md3_spec.py`.

8. **Lessons Learned & Subsite Visual Verification Guardrails**:
   * **Why an earlier iteration appeared done when it was unusable in production**:
     * During initial Universal Header development, all Playwright tests in `tests/test_md3_universal_header.py` passed, leading us to believe the integration was complete. In reality, when verified on a real multi-tool build (`~/wt/theme`), the Rustdoc subsite was completely unusable (blank white viewport below the header because `nav.sidebar` and `main` were pushed offscreen to the right) and Doxygen `#nav-tree` navigation was broken (expand/collapse arrows overlapped link labels and intercepted clicks, and the mobile drawer failed to appear due to CSS selector specificity).
     * **Root Cause 1 — Minimal synthetic HTML stubs without third-party layout CSS/JS**: The test fixtures originally used bare 5-line HTML tags with no CSS. They did not model `rustdoc.css`'s `body.rustdoc { display: flex; flex-direction: row; flex-wrap: nowrap; }` (where a `position: sticky` header injected as the first child of `body.rustdoc` becomes a `1280px+`-wide first flex column) or Doxygen `navtree.js`/`navtree.css`'s reliance on `box-sizing: content-box` for `.arrow` indentation (`width: 16px` + inline `padding-left`).
     * **Root Cause 2 — DOM/class assertions without bounding-box geometry or visual screenshot inspection**: Asserting `document.body.classList.contains('md3-doxygen-nav-open')` or `Boolean(header)` passed even when CSS specificity (`body:has(#md3-universal-header[data-subsite="doxygen"]) #side-nav { display: none !important; }`) kept the drawer invisible (`width: 0`) or pushed content offscreen (`left: 1469px`).
   * **Mandatory Verification Infrastructure & Workflow**:
     * **Realistic Subsite CSS/DOM Fixtures**: Test fixtures in `tests/test_md3_universal_header.py` must include the layout-critical CSS/DOM rules of external tools (`body.rustdoc` horizontal flex row, `body.rustdoc.src` `#sidebar-button`, Doxygen `#nav-tree` nested `<ul>` items with inline `padding-left` on `.arrow`).
     * **Bounding-Box Geometry & Interactive Assertions**: Tests must assert rendered `getBoundingClientRect()` coordinates (e.g., `nav.sidebar` at `left == 0`, `main` at `left == 200`; mobile drawer `display == 'block'` and `width >= 200`; Doxygen `.arrow` `boxSizing == 'content-box'` and `arrowRect.right <= labelRect.left`) and interactive click flows (expanding tree arrows without navigating, clicking tree links to navigate).
     * **Visual Playwright Screenshot Inspection**: Whenever modifying layout, CSS, or subsite postprocessing, always run a Playwright script against the real integrated build (`~/wt/theme/bazel-bin/docs/sphinx/docs/_build/html`), capture desktop (`1280x800`) and mobile (`375x667`) screenshots across Light/Dark themes and interactive states (expanded tree, open mobile drawer, expanded source sidebar), and visually inspect the PNGs with `view_file` before considering the task complete.

## Build system

[Sphinx](https://www.sphinx-doc.org) builds the docs and
[Bazel](https://bazel.build) orchestrates the Sphinx build, the tests, and the
wheel. The theme does not inherit from any built-in Sphinx theme, not even
`basic` (`inherit = "none"` in `md3/theme.toml`).

### Invoke Bazel

Always use the `./bazelisk` wrapper script at the root of the repository. It
downloads a pinned `bazelisk` binary into the gitignored `.bazelisk/` directory
on first use. Do not attempt to use a globally available `bazel` or `bazelisk`
because they may not exist.

### Build everything

```bash
./bazelisk build //...
```

### Debug build sources

Do not rely on the directory hierarchy of the repository. When Bazel runs the
Sphinx build, it rearranges the source files. To see exactly what Sphinx sees:

```bash
./bazelisk build :ls
ls bazel-bin/docs/_docs/_sources
```

### Inspect build output

```bash
./bazelisk build //docs
ls bazel-bin/docs/docs/_build/html
```

## Managing Python Dependencies

Top-level Python dependencies are listed in `requirements.in` and locked into
`requirements.txt` using `uv` (via `rules_python`'s `lock` rule):

```bash
./bazelisk run :requirements.update
```

The pip hub is named `deps`, so Bazel targets depend on e.g. `@deps//sphinx`.

## Serving Docs Locally

To build and serve the documentation locally:

```bash
./bazelisk run :serve
```

## Running Sphinx Directly

You can run the Sphinx binary directly for debugging or faster iteration:

```bash
./bazel-bin/docs/sphinx \
  bazel-out/k8-fastbuild/bin/docs/_docs/_sources \
  bazel-out/k8-fastbuild/bin/docs/docs/_build/html \
  --builder=html \
  --show-traceback \
  --jobs=auto \
  --doctree-dir=bazel-out/k8-fastbuild/bin/docs/docs/_build/html_doctrees \
  --fail-on-warning
```

## Continuous Integration

Two GitHub Actions workflows live in `.github/workflows/`:

*   `ci.yml` runs `./bazelisk test //tests`, `./bazelisk build :wheel`, and
    `./bazelisk build //docs` on pushes and pull requests.
*   `pages.yml` builds `//docs` on pushes to `main` and deploys
    `bazel-bin/docs/docs/_build/html` to GitHub Pages.

## Running Tests

This project uses Bazel for running tests. The `./bazelisk` wrapper automatically downloads and caches `bazelisk` in `.bazelisk/`.

Tests live in `tests/`. `tests/harness.py` builds a throwaway Sphinx project
(with the theme enabled) in a temp dir, serves it from an in-process HTTP
server, and drives it with Playwright. `tests/md3_spec.py` defines the
`MD3_SPECS` conformance catalog, the `@md3_conformance(spec_key="...")`
decorator, and `self.spec_context(spec_key="...")`. Register any new test files
in the list comprehension and `test_suite` in `tests/BUILD.bazel`:

*   `//tests:test_md3_tokens` — Static CSS & computed MD3 tokens, light/dark color roles, WCAG 2.1 AA contrast, shapes, elevation, typescales, motion, spacing.
*   `//tests:test_md3_density` — Compact `-2` density measurements (32px buttons/nav items/chips/icon-buttons, 36px search bar & nav tabs, 56px app bar, 8px table padding).
*   `//tests:test_md3_layout` — Responsive window size classes (`>=1200px` 3-pane, `840–1199px` 2-pane, `<840px` modal drawer with scrim and focus return).
*   `//tests:test_md3_components` — Custom element registration (`md3-app`, `md3-top-app-bar`, `md3-nav-tabs`, `md3-sidebar`, `md3-toc`, `md3-search`, `md3-theme-toggle`, `md3-copy-button`), scroll elevation, Pagefind full-site cross-page search, code copy, and TOC scrollspy.
*   `//tests:test_md3_navigation` — Large-site navigation scalability: `<md3-nav-tabs>` active hierarchy & keyboard arrow navigation, 1-level progressive disclosure in `<md3-sidebar>`, live section filtering, in-place JS graph traversal without page reloads, and no-JS multi-page fallback.
*   `//tests:test_md3_progressive_enhancement` — No-JS (`java_script_enabled=False`) mobile TOC popover, no-JS mobile navigation drawer, no-JS CSS `:has()` theme switching, and Light DOM rendering.
*   `//tests:test_md3_sphinx_elements` — Admonitions, Pygments dual light/dark stylesheets, data tables, cards, dividers, inline links, pagination, breadcrumbs.
*   `//tests:test_md3_accessibility` — `:focus-visible` rings, state layers, ARIA landmarks, icon button tooltips.
*   `//tests:test_md3_universal_header` — Universal header & subsite postprocessing across Sphinx, Doxygen, and Rustdoc (cross-subsite theme sync, legacy `'auto'` cleanup, `SecurityError` resilience, universal breadcrumbs, mobile drawer & search trigger, skip-to-main-content link, Pagefind subsite indexing/exclusions, and local URL rewriting).
*   `//tests:test_md3_deeplinks` — Verifies every `MD3_SPECS` entry deeplinks to a real `<section id="...">` in built `//docs` (`components/<slug>.html#<section-id>`) and that the section contains the outbound `https://m3.material.io/<route>#<uuid>` link.
*   `//tests:test_app`, `//tests:test_html`, `//tests:test_runtime` — Base Sphinx extension, HTML title, and runtime smoke tests.

### Run All Tests

To run all tests in the repository:

```bash
./bazelisk test //tests
```

### Run a Specific Test Target

To run a specific test, such as `test_runtime`:

```bash
./bazelisk test //tests:test_runtime
```

### Inspecting Test Output

When a test fails, Bazel will print a summary and point to the log file.

*   **Test Logs**: Detailed logs for each test run are stored in the `bazel-testlogs` directory. For example, the log for `test_runtime` can be found at:
    `bazel-testlogs/tests/test_runtime/test.log`
    This is a symlink to the actual log file in the Bazel execution root.

### Verbose Output and Debugging

By default, Bazel may suppress test output unless the test fails. You can control this behavior with the `--test_output` flag:

*   **Show all output (even for passing tests)**:
    ```bash
    ./bazelisk test //tests:test_runtime --test_output=all
    ```
*   **Stream output in real-time**: Useful for debugging hung tests.
    ```bash
    ./bazelisk test //tests:test_runtime --test_output=streamed
    ```
*   **Force rerun tests (bypass cache)**: Bazel caches successful test results. To force a rerun:
    ```bash
    ./bazelisk test //tests:test_runtime --nocache_test_results
    ```

---

## Packaging and Publishing to PyPI

This project is configured with `@rules_python//python:packaging.bzl`'s `py_wheel` rule to build and publish a Python wheel (`md3`) for PyPI.

### 1. Build the Wheel

To build the wheel package:

```bash
./bazelisk build :wheel
# or: ./bazelisk build //md3:wheel
```

The generated wheel will be located at:
`bazel-bin/md3/md3-[version]-py3-none-any.whl`

### 2. Inspect the Wheel

Since a `.whl` file is a standard ZIP archive, you can inspect its contents with `unzip` (or `python3 -m zipfile`):

*   **List all files in the wheel**:
    ```bash
    unzip -l bazel-bin/md3/md3-0.1.0-py3-none-any.whl
    # or: python3 -m zipfile -l bazel-bin/md3/md3-0.1.0-py3-none-any.whl
    ```
*   **Print a specific file inside the wheel to stdout (`-p`)**:
    ```bash
    unzip -p bazel-bin/md3/md3-0.1.0-py3-none-any.whl md3-0.1.0.dist-info/METADATA
    unzip -p bazel-bin/md3/md3-0.1.0-py3-none-any.whl md3-0.1.0.dist-info/entry_points.txt
    ```
*   **Extract the wheel into a temporary directory**:
    ```bash
    unzip bazel-bin/md3/md3-0.1.0-py3-none-any.whl -d /tmp/md3-wheel
    ```

### 3. Publish to PyPI

Under Bzlmod, `rules_python`'s `py_wheel` automatically generates a `//md3:wheel.publish` target (aliased at the root as `:publish`) with bundled `twine`:

```bash
TWINE_USERNAME=__token__ TWINE_PASSWORD=pypi-... \
  ./bazelisk run :publish
# or: ./bazelisk run //md3:wheel.publish
```

To publish to TestPyPI first:

```bash
TWINE_USERNAME=__token__ TWINE_PASSWORD=pypi-... \
  ./bazelisk run :publish -- --repository testpypi
```

Before publishing, ensure you update the `version` and `distribution` in the `py_wheel` target in `md3/BUILD.bazel`.
