=========================
App Scaffold & Layout
=========================

The ``<md3-app>`` root custom element orchestrates the
Material Design 3 application scaffold, responsive window size breakpoints,
compact density scale, and accessible landmark hierarchy.

.. _custom-elements-registry:

Custom Elements Registry
------------------------

Every interactive theme component is implemented as a standard Custom Element
and registered with ``window.customElements`` in ``md3/components/app.js``:

* ``<md3-app>`` — Root application shell, Pygments theme sync,
  and automatic code block copy-button injection.
* ``<md3-top-app-bar>`` — Sticky top app bar with scroll state management.
* ``<md3-nav-tabs>`` — Primary section navigation tabs with keyboard arrow-key
  roving navigation.
* ``<md3-sidebar>`` — Responsive navigation drawer with 1-level progressive
  disclosure and instant section filtering.
* ``<md3-toc>`` — Secondary "On this page" scrollspy navigation.
* ``<md3-search>`` — Modal quick-search dialog with keyboard shortcuts.
* ``<md3-theme-toggle>`` — Light/dark theme switcher and popover menu.
* ``<md3-copy-button>`` — Clipboard copy button for code blocks.

**MD3 Specification Reference:**
`Foundations > Accessible design > Overview > Principles <https://m3.material.io/foundations/overview/principles#25cda2a6-e748-4efc-be27-8be7b1966fc5>`_

.. _three-pane-scaffold:

Three Pane Scaffold
-------------------

On Expanded and Large viewports (``>= 1200px``), the ``.md3-scaffold`` layout
implements an adaptive three-pane CSS Grid architecture:

1. **Navigation Pane (Left)**: Fixed ``256px`` (``--md-comp-navigation-drawer-container-width``)
   persistent navigation drawer (``<md3-sidebar>``).
2. **Body Pane (Center)**: Fluid ``minmax(0, 1fr)`` main article region
   (``<main class="md3-main">``) with a ``820px`` readable measure container.
3. **Supporting Pane (Right)**: Fixed ``224px`` (``--md-sys-layout-toc-width``)
   sticky table of contents pane (``<md3-toc>``).

**MD3 Specification Reference:**
`Foundations > Layout > Scaffold > Panes > Three-pane layouts <https://m3.material.io/foundations/layout/scaffold/panes#deed6085-479f-4a94-b266-c7b079d19500>`_

.. _two-pane-expanded-layout:

Two Pane Expanded Layout
------------------------

On Medium and early Expanded viewports (``840px <= width < 1200px``), the
``.md3-scaffold`` adapts to a two-pane layout by keeping the persistent
``256px`` navigation drawer alongside the fluid main content pane while collapsing
the secondary ``<md3-toc>`` supporting pane into an inline "On this page"
popover menu in the content navigation bar.

**MD3 Specification Reference:**
`Foundations > Layout > Breakpoints > Expanded > Panes <https://m3.material.io/foundations/layout/breakpoints/expanded#9f3c44f0-b91e-4618-b93a-6fb34239d246>`_

.. _window-size-breakpoints:

Window Size Breakpoints
-----------------------

The theme's responsive media queries align with Material Design 3 Window Size
Classes:

* **Compact (``< 600px``)**: Single-pane article view; navigation drawer becomes
  a modal overlay (``position: fixed``) with scrim; search bar collapses to a
  compact icon button.
* **Medium (``600px - 839px``)**: Single-pane article view with modal navigation
  drawer and full pill search trigger in the top app bar.
* **Expanded (``840px - 1199px``)**: Two-pane layout with persistent ``256px``
  navigation drawer and fluid main content pane.
* **Large (``>= 1200px``)**: Full three-pane layout with persistent ``256px``
  navigation drawer, fluid main content pane, and ``224px`` sticky TOC pane.

**MD3 Specification Reference:**
`Foundations > Layout > Breakpoints > Overview > Breakpoints overview <https://m3.material.io/foundations/layout/breakpoints/overview#395b70d6-973e-4d07-a40b-3be8d4e150d5>`_

.. _spacing-system-tokens:

Spacing System Tokens
---------------------

All layout margins, paddings, and grid gaps derive from the Material Design 3
``4dp``/``8dp`` spatial grid scale exposed as ``--md-sys-measurement-space*``
and ``--md-sys-spacing-*`` CSS custom properties:

* ``--md-sys-spacing-1`` / ``--md-sys-measurement-space100``: ``4px``
* ``--md-sys-spacing-2`` / ``--md-sys-measurement-space200``: ``8px``
* ``--md-sys-spacing-3`` / ``--md-sys-measurement-space300``: ``12px``
* ``--md-sys-spacing-4`` / ``--md-sys-measurement-space400``: ``16px``
* ``--md-sys-spacing-6`` / ``--md-sys-measurement-space600``: ``24px``
* ``--md-sys-spacing-8`` / ``--md-sys-measurement-space800``: ``32px``

**MD3 Specification Reference:**
`Styles > Spacing > Tokens > System spacing tokens <https://m3.material.io/styles/spacing/tokens#a744956e-be8e-4b97-8a30-b2170e6944a8>`_

.. _compact-density-scale:

Compact Density Scale
---------------------

Technical documentation requires high information density so readers can scan
navigation trees, API signatures, and data tables without excessive scrolling.
``md3`` applies the MD3 **-2 (compact)** density scale across the entire theme
via ``--md-sys-density-scale: -2`` and ``--md-density-scale: -2``, reducing
interactive component heights by ``8px`` relative to default (``0``) density
while preserving accessible touch and click targets.

**MD3 Specification Reference:**
`Foundations > Layout > Grids & spacing > Density > Component scaling <https://m3.material.io/foundations/layout/grids-spacing/density#7b845d8f-aaf6-4503-ad00-760f9f988388>`_

.. _web-landmarks:

Web Landmarks
-------------

The page scaffold exposes unambiguous HTML5 and ARIA landmarks so assistive
technology users can jump directly between regions:

* ``<header class="md3-top-app-bar" role="banner">`` — Top app bar banner.
* ``<nav class="md3-nav-tabs__nav" aria-label="Section navigation">`` — Top-level
  primary navigation tabs.
* ``<md3-sidebar role="navigation" aria-label="Site navigation">`` — Primary
  section navigation drawer.
* ``<main class="md3-main" id="main" role="main">`` — Primary article content.
* ``<md3-toc role="complementary" aria-label="On this page">`` — Secondary
  in-page table of contents.
* ``<footer class="md3-footer" role="contentinfo">`` — Document footer.

**MD3 Specification Reference:**
`Foundations > Accessible design > Structure > Web landmarks and headings <https://m3.material.io/foundations/designing/structure#dafa42e2-b056-42b9-ab75-9c9ea9f293b7>`_

.. _focus-flow:

Focus Flow
----------

A ``.md3-skip-link`` ("Skip to main content") is the first focusable element in
the DOM, positioned off-screen until focused via ``:focus-visible`` where it
appears at the top-left of the viewport and moves focus directly to ``#main``.
Logical DOM order matches visual order: Top App Bar -> Section Navigation Tabs ->
Navigation Drawer -> Main Content -> Table of Contents -> Footer.

**MD3 Specification Reference:**
`Foundations > Accessible design > Flow > Focus order & key traversal <https://m3.material.io/foundations/designing/flow#74d866b2-f8e4-4dbb-a352-8019b2a384b1>`_
