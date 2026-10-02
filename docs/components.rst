==========
Components
==========

Every web component, UI primitive, and design token system in ``paz`` has a
dedicated documentation page detailing how it conforms to the Material Design 3
(MD3) specification, including direct deeplinks to the relevant sections of
`m3.material.io <https://m3.material.io>`_. When an MD3 conformance test fails,
its assertion output deeplinks directly to the corresponding conformance section
within these component docs.

Custom Web Components
=====================

The theme defines and registers custom elements in ``paz/components/app.js``:

* :doc:`components/app` (``<paz-app>`` / ``<md3-app>``): Root application
  scaffold, responsive window size breakpoints, ``-2`` compact density scale,
  and accessible landmark hierarchy.
* :doc:`components/top-app-bar` (``<md3-top-app-bar>``): Sticky small top app
  bar (``56px``) with navigation drawer toggle, search trigger, and scroll
  elevation state tracking.
* :doc:`components/nav-tabs` (``<md3-nav-tabs>``): Primary section navigation
  tabs (``40px``) with horizontal overflow centering and roving arrow-key
  navigation.
* :doc:`components/sidebar` (``<md3-sidebar>``): Responsive navigation drawer
  (``256px`` persistent column on desktop, modal drawer with scrim on mobile)
  featuring **one-level-at-a-time progressive disclosure**, ancestor back-links,
  and live section filtering.
* :doc:`components/toc` (``<md3-toc>``): Right-hand "On this page" table of
  contents with ``IntersectionObserver`` scrollspy and back-to-top action.
* :doc:`components/search` (``<md3-search>``): Compact ``36px`` search bar pill
  and modal ``<dialog>`` quick-search with focus restoration.
* :doc:`components/theme-toggle` (``<md3-theme-toggle>``): Compact ``36px`` icon
  button switching between light and dark color schemes and synchronizing
  Pygments syntax highlighting stylesheets.
* :doc:`components/copy-button` (``<md3-copy-button>``): Compact code block
  clipboard copy button with keyboard and visual feedback.

UI Primitives & Foundations
===========================

* :doc:`components/buttons` (``.md3-btn``): Filled, Tonal, Outlined, Elevated,
  and Text buttons at ``32px`` compact height with pressed shape morphing.
* :doc:`components/icon-buttons` (``.md3-icon-btn``): Compact ``36px`` circular
  icon buttons with native tooltips and ARIA labeling.
* :doc:`components/chips` (``.md3-chip``): Compact ``28px`` Assist and Filter
  chips.
* :doc:`components/cards` (``.md3-card``): Outlined, Filled, and Elevated cards,
  pagination cards, corner radius scale, elevation levels, and motion tokens.
* :doc:`components/admonitions` (``div.admonition``): Semantic callout
  containers for Sphinx notes, tips, and warnings.
* :doc:`components/tables` (``table.docutils``): Compact data tables with
  ``tabular-nums`` numeral alignment.
* :doc:`components/dividers` (``hr``): ``1px`` ``outline-variant`` structural
  and article dividers.
* :doc:`components/breadcrumbs` (``.md3-breadcrumbs``): Hierarchical wayfinding
  breadcrumb trail.
* :doc:`components/typography`: Complete 15-role MD3 typescale, semantic
  heading/body mappings, inline hyperlinks, and Roboto / Roboto Mono typefaces.
* :doc:`components/color`: Three-tier token architecture (``--md-ref-*``,
  ``--md-sys-*``, ``--md-comp-*``), 26 semantic color roles, tonal palettes, and
  WCAG contrast pairing.
* :doc:`components/progressive-enhancement`: How the site works when JavaScript
  is disabled (``:root.no-js``) and the progressive enhancements enabled when
  JavaScript is available (in-place navigation graph traversal, full-site
  Pagefind search, roving tabs, and scrollspy).

.. toctree::
   :maxdepth: 1
   :caption: Component Reference

   components/app
   components/top-app-bar
   components/nav-tabs
   components/sidebar
   components/toc
   components/search
   components/theme-toggle
   components/copy-button
   components/buttons
   components/icon-buttons
   components/chips
   components/cards
   components/admonitions
   components/tables
   components/dividers
   components/breadcrumbs
   components/typography
   components/color
   components/progressive-enhancement
