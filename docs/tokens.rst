======
Tokens
======

Material Design 3 uses a three-tier design token architecture (**Reference**, **System**, and **Component** tokens) from Google's Material 3 v35.0 specification.

Reference Palette Tokens
========================

Reference tokens (``--md-ref-palette-*``) define the tonal palettes across key hues:

* **Primary** (``--md-ref-palette-primary0`` .. ``primary100``): Google Blue tonal scale (``primary40: #0b57d0``, ``primary80: #a8c7fa``, ``primary90: #d3e3fd``).
* **Secondary** (``--md-ref-palette-secondary0`` .. ``secondary100``): Tonal secondary scale (``secondary40: #00639b``, ``secondary80: #7fcfff``, ``secondary90: #c2e7ff``).
* **Tertiary** (``--md-ref-palette-tertiary0`` .. ``tertiary100``): Tonal green accent scale (``tertiary40: #146c2e``, ``tertiary80: #6dd58c``, ``tertiary90: #c4eed0``).
* **Error** (``--md-ref-palette-error0`` .. ``error100``): Semantic alert tones (``error40: #b3261e``, ``error80: #f2b8b5``, ``error90: #f9dedc``).
* **Neutral & Neutral Variant** (``--md-ref-palette-neutral*`` / ``neutral-variant*``): Surfaces, containers, and outlines.

System Color Tokens
===================

The following semantic color roles (``--md-sys-color-*``) are supported in both light and dark modes:

.. list-table:: MD3 System Color Tokens
   :widths: 38 31 31
   :header-rows: 1

   * - Token
     - Light Value
     - Dark Value
   * - ``--md-sys-color-primary``
     - ``#0b57d0``
     - ``#a8c7fa``
   * - ``--md-sys-color-on-primary``
     - ``#ffffff``
     - ``#062e6f``
   * - ``--md-sys-color-primary-container``
     - ``#d3e3fd``
     - ``#0842a0``
   * - ``--md-sys-color-on-primary-container``
     - ``#041e49``
     - ``#d3e3fd``
   * - ``--md-sys-color-secondary-container``
     - ``#c2e7ff``
     - ``#004a77``
   * - ``--md-sys-color-on-secondary-container``
     - ``#001d35``
     - ``#c2e7ff``
   * - ``--md-sys-color-surface``
     - ``#ffffff``
     - ``#131314``
   * - ``--md-sys-color-on-surface``
     - ``#1f1f1f``
     - ``#e3e3e3``
   * - ``--md-sys-color-surface-container``
     - ``#f0f4f9``
     - ``#1e1f20``
   * - ``--md-sys-color-outline``
     - ``#747775``
     - ``#8e918f``
   * - ``--md-sys-color-outline-variant``
     - ``#c4c7c5``
     - ``#444746``

Component Tokens (Small & XSmall High-Density Specs)
====================================================

To achieve high information density without oversized touch targets, the theme binds directly to Material 3's official ``xsmall`` and ``small`` component tokens (``--md-comp-*``):

* **Button XSmall**: ``--md-comp-button-xsmall-container-height: 32px``, ``--md-comp-button-xsmall-leading-space: 12px``, ``--md-comp-button-xsmall-trailing-space: 12px``, ``--md-comp-button-xsmall-icon-size: 20px``.
* **Icon Button XSmall**: ``--md-comp-icon-button-xsmall-container-height: 32px``, ``--md-comp-icon-button-xsmall-icon-size: 20px``.
* **Assist & Filter Chips**: ``--md-comp-assist-chip-container-height: 32px``, ``--md-comp-filter-chip-container-height: 32px``.
* **Navigation Drawer**: ``--md-comp-navigation-drawer-container-width: 260px``, ``--md-comp-navigation-drawer-active-indicator-height: 32px``.
* **Small Top App Bar**: ``--md-comp-top-app-bar-small-container-height: 56px``.
* **Search Bar**: ``--md-comp-search-bar-container-height: 36px``.

Shape Tokens
============

* ``--md-sys-shape-corner-none``: ``0px``
* ``--md-sys-shape-corner-extra-small``: ``4px``
* ``--md-sys-shape-corner-small``: ``8px``
* ``--md-sys-shape-corner-medium``: ``12px``
* ``--md-sys-shape-corner-large``: ``16px``
* ``--md-sys-shape-corner-large-increased``: ``20px``
* ``--md-sys-shape-corner-extra-large``: ``28px``
* ``--md-sys-shape-corner-extra-large-increased``: ``32px``
* ``--md-sys-shape-corner-extra-extra-large``: ``48px``
* ``--md-sys-shape-corner-full``: ``9999px``

Elevation Tokens
================

* ``--md-sys-elevation-level0``: ``none`` (``0px``)
* ``--md-sys-elevation-level1``: Ambient + key shadow (``1px``)
* ``--md-sys-elevation-level2``: Ambient + key shadow (``3px``)
* ``--md-sys-elevation-level3``: Ambient + key shadow (``6px``)
* ``--md-sys-elevation-level4``: Ambient + key shadow (``8px``)
* ``--md-sys-elevation-level5``: Ambient + key shadow (``12px``)
