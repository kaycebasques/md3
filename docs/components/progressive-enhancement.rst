====================================
Progressive Enhancement & No-JS Mode
====================================

``md3`` is architected from the ground up using **Light DOM server-side rendering**
and **progressive enhancement**. Every page is fully readable, navigable, and
themeable when JavaScript is disabled (``:root.no-js``), while enabling
JavaScript unlocks instantaneous client-side navigation graph traversal,
full-site Pagefind search, keyboard roving tab management, and scrollspy
tracking.

.. _light-dom-architecture:

Light DOM Architecture
----------------------

All structural HTML—including the top app bar, primary section tabs, progressive
disclosure navigation drawer, breadcrumbs, article content, on-page table of
contents, and pagination cards—is rendered directly into the Light DOM at build
time by Sphinx's Jinja2 templates (``md3/layout.html``):

* **No Client-Side Template Dependencies**: Custom elements (``<md3-app>``,
  ``<md3-top-app-bar>``, ``<md3-nav-tabs>``, ``<md3-sidebar>``, ``<md3-toc>``,
  ``<md3-search>``, ``<md3-theme-toggle>``) wrap semantic HTML landmarks and
  links rather than hiding content inside opaque Shadow DOM roots or requiring
  JavaScript to render navigation links.
* **No-JS Detection Class**: The ``<html>`` element starts with ``class="no-js"``.
  An inline bootstrap script in ``<head>`` removes ``.no-js`` before first paint
  when JavaScript is enabled. CSS rules scoped to ``:root.no-js`` provide native
  HTML fallbacks whenever JavaScript is unavailable.

**MD3 Specification Reference:**
`Foundations > Accessible design > Overview > Principles <https://m3.material.io/foundations/overview/principles#25cda2a6-e748-4efc-be27-8be7b1966fc5>`_

.. _no-js-navigation-and-controls:

No-JS Navigation and Controls
-----------------------------

When JavaScript is disabled in the browser, all core documentation workflows
continue to operate using native HTML5 and CSS features:

1. **Multi-Page Progressive Disclosure Navigation**:
   Every link in ``<md3-sidebar>``—including ``<- Ancestor`` drill-up back-links,
   section hub links, and leaf document links—is a standard ``<a href="...">``
   element pointing to the target HTML document. Clicking ``<- Material Design 3
   Sphinx Theme`` on ``components.html`` loads ``index.html``, which displays
   the top-level navigation hierarchy.
2. **Mobile Navigation Drawer via HTML Popover API**:
   On Compact and Medium viewports (``< 840px``), ``#drawer-toggle`` uses
   ``popovertarget="md3-sidebar"`` and ``#sidebar-close`` uses
   ``popovertarget="md3-sidebar" popovertargetaction="hide"`` to open and close
   ``<md3-sidebar id="md3-sidebar" popover>`` with a CSS ``:has(md3-sidebar:popover-open)``
   scrim backdrop—requiring zero JavaScript.
3. **Mobile Table of Contents Menu via HTML Popover API**:
   On viewports ``< 1200px``, ``#toc-mobile-btn`` opens ``#md3-toc-mobile-menu[popover]``
   natively so readers can jump to any section heading on the page without
   JavaScript.
4. **No-JS Light & Dark Theme Switching**:
   ``<md3-theme-toggle>`` pairs ``#theme-menu-btn`` (``popovertarget="md3-theme-menu"``)
   with ``#md3-theme-menu[popover]`` containing ``<input type="radio" name="theme"
   value="light|dark">`` controls. Pure CSS selectors
   (``:root.no-js:has(#md3-theme-menu input[name="theme"][value="dark"]:checked)``)
   remap all 26 MD3 semantic color tokens between light and dark modes without
   JavaScript.
5. **Search Form & Back-to-Top Fallbacks**:
   The top app bar search trigger is wrapped in a ``<form action="search.html"
   method="get">`` form with a native ``<a href="search.html">`` link, and the
   "Back to top" control is a semantic ``<a href="#body">`` anchor.
   JavaScript-only controls (such as ``#sidebar-filter-input``) are hidden cleanly
   via ``:root.no-js .md3-sidebar__filter { display: none; }``.

**MD3 Specification Reference:**
`Foundations > Accessible design > Structure > Web landmarks and headings <https://m3.material.io/foundations/designing/structure#dafa42e2-b056-42b9-ab75-9c9ea9f293b7>`_

.. _js-progressive-enhancements:

JavaScript Progressive Enhancements
-----------------------------------

When JavaScript is available, ``md3/components/app.js`` upgrades the Light DOM
elements in place with richer, instantaneous interactions:

1. **In-Place Navigation Graph Traversal (``<md3-sidebar>``)**:
   The complete site ``toctree`` graph is serialized into
   ``#md3-nav-graph-data``. Clicking any ``<- Ancestor`` back-link
   (``.md3-sidebar__back-link[data-nav-level]``) or any parent section item with
   children (``.has-children > a[data-nav-level]``) traverses up and down the
   navigation hierarchy **in-place without loading a new page**. For example,
   clicking ``<- Material Design 3 Sphinx Theme`` while reading
   ``/components.html`` immediately displays the top-level site hierarchy in the
   sidebar while remaining on ``/components.html``. Clicking the section header
   link (``.md3-sidebar__section-link``) or any leaf page item navigates to that
   document.
2. **Live Section Filtering (``#sidebar-filter-input``)**:
   On any sidebar hierarchy level containing ``8`` or more items (whether loaded
   initially or reached via in-place graph traversal), ``<md3-sidebar>`` displays
   a live filter input that filters items as you type and hides empty section
   captions.
3. **Full-Site Pagefind Search (``<md3-search>``)**:
   Clicking the search bar or pressing ``/`` or ``Cmd+K`` / ``Ctrl+K`` opens the
   MD3 modal ``<dialog>`` and queries the build-time **Pagefind** WebAssembly
   search index across the entire documentation site, rendering MD3 result cards
   with highlighted ``<mark>`` excerpts and deep-linked section sub-results.
4. **Roving Tab Keyboard Navigation (``<md3-nav-tabs>``)**:
   Adds ``ArrowRight``, ``ArrowLeft``, ``Home``, and ``End`` keyboard focus
   traversal across top-level section tabs and centers the active tab in
   horizontally scrollable tab bars.
5. **Scrollspy & Sticky Header Elevation (``<md3-toc>``, ``<md3-top-app-bar>``)**:
   Tracks the active article section via ``IntersectionObserver`` and elevates
   ``<md3-top-app-bar>`` to ``--md-sys-elevation-level2`` when scrolled.
6. **Persistent Theme & Code Copy (``<md3-theme-toggle>``, ``<md3-copy-button>``)**:
   Persists light/dark theme preferences in ``localStorage``, synchronizes
   Pygments syntax highlighting stylesheets, and injects one-click clipboard
   copy buttons into code blocks.

**MD3 Specification Reference:**
`Components > Navigation Drawer > Guidelines > Usage <https://m3.material.io/components/navigation-drawer/guidelines#761e9679-2e72-4a85-894d-55bc3666b567>`_
