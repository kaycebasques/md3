=================================
Material Design 3 Sphinx Theme
=================================

.. toctree::
   :maxdepth: 2
   :caption: Guides

   components
   tokens

Overview
========

Welcome to the **Material Design 3 (MD3) Sphinx Theme**. This theme implements Google's
Material Design 3 design system for Sphinx documentation, prioritizing **high information density**,
responsive **3-column layout**, and full design token compliance.

Key Features
------------

* **High Information Density**: Uses MD3 compact density options (scale -2) with compact buttons (32px), dense navigation lists, and optimized whitespace to maximize content visible on screen.
* **3-Column Architecture**: Designed like modern documentation sites (Stripe, MDN, Mintlify):
  * **Left Navigation**: Collapsible, hierarchical sidebar navigation with active indicator pills.
  * **Center Content**: Structured documentation with breadcrumbs, admonitions, and code blocks.
  * **Right On-Page TOC**: Interactive table of contents with scrollspy active heading tracking.
* **Complete MD3 Tokens**: Full palette roles (primary, secondary, tertiary, surface containers, error), 15-scale typography tokens, shape tokens, and elevation shadows.
* **Interactive Elements**: Instant search dialog (``⌘K`` / ``/``), 1-click code copying, and smooth light/dark theme toggling with preference persistence.
* **Progressive Enhancement & No-JS Fallback**: Designed from the ground up so core reading and navigation features require **no JavaScript**:
  * **Mobile Navigation Drawer**: Opens and closes on mobile screens (with mouse, touch, or keyboard) using the native HTML Popover API (``popover`` / ``popovertarget``) and CSS.
  * **Mobile "On this page" TOC**: Accessible on mobile/tablet viewports via the native HTML Popover API (``popover`` / ``popovertarget``).
  * **Theme Switching**: Switchable via a native HTML popover menu, form radio controls, and CSS ``:has()``.
  * **Back to Top Navigation**: Uses a semantic ``<a href="#body">`` anchor link that scrolls to the top without JavaScript.
  * **Light DOM Rendering**: All layouts, navigation lists, tables of contents, and breadcrumbs are rendered statically into the Light DOM by Jinja templates, ensuring immediate indexing and reading when scripts are disabled.
  * **JavaScript as Enhancement**: JavaScript is reserved strictly for progressive enhancements (keyboard shortcuts, scrollspy heading tracking, focus restoration, and automatic popover closing).

Admonitions
===========

The theme provides styled callout containers for all standard docutils admonition types:

.. note::
   This is a **Note** callout. It utilizes the primary container token for informative highlights.

.. tip::
   This is a **Tip** callout. Use it to share recommendations and best practices.

.. warning::
   This is a **Warning** callout. Be mindful of potential caveats or edge cases.

.. danger::
   This is a **Danger** callout. High-risk actions that could cause data loss or security issues.

Code Highlighting
=================

Code blocks include a compact one-click copy button:

.. code-block:: python

   def calculate_density(default_height: int, scale: int = -2) -> int:
       """Calculates component container height based on MD3 density scale."""
       assert scale in (-4, -3, -2, -1, 0), "Scale must be between -4 and 0"
       return default_height + (scale * 4)

   # Compact button height: 40 + (-2 * 4) = 32px
   assert calculate_density(40, -2) == 32

Tables
======

Compact tables keep technical documentation readable and dense:

.. list-table:: Material Design 3 Density Scales
   :widths: 20 25 30 25
   :header-rows: 1

   * - Scale
     - Button Height
     - Nav Item Height
     - Use Case
   * - ``0``
     - 40px
     - 48px
     - Standard / Mobile Touch
   * - ``-1``
     - 36px
     - 40px
     - Moderate Density
   * - ``-2``
     - 32px
     - 32px
     - High Density (Default)
   * - ``-3``
     - 28px
     - 28px
     - Compact Toolbars / Dense UI
