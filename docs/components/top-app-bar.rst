=========================
Top App Bar
=========================

The ``<md3-top-app-bar>`` component implements a sticky Material Design 3 Small
Top App Bar at the top of the viewport, housing the navigation drawer toggle on
compact/medium screens, the site brand title, the quick-search trigger bar, and
trailing utility actions (source repository link and theme switcher).

.. _small-top-app-bar:

Small Top App Bar
-----------------

Under the theme's compact density scale (``-2``), ``<md3-top-app-bar>`` sets
``--md-comp-top-app-bar-small-container-height: 56px`` and renders with a fixed
``56px`` height, ``position: sticky; top: 0``, and a ``1px solid
var(--md-sys-color-outline-variant)`` bottom hairline border.

* **Container Color**: ``--md-comp-top-app-bar-small-container-color``
  (mapped to ``--md-sys-color-surface`` at rest).
* **Headline Typography**: ``--md-sys-typescale-title-medium-font`` (``1rem`` /
  ``16px``, weight ``500``).
* **Leading Icon**: ``#drawer-toggle`` compact icon button visible on viewports
  ``< 840px``.
* **Trailing Actions**: ``.md3-top-app-bar__actions`` flex container with
  ``4px`` gap for ``<md3-theme-toggle>`` and optional repository icon buttons.

**MD3 Specification Reference:**
`Components > App bars > Specs > Measurements > Small app bar <https://m3.material.io/components/app-bars/specs#fac99130-8bb8-498c-8cb8-16ea056cc3e1>`_

.. _scroll-states:

Scroll States
-------------

``<md3-top-app-bar>`` listens passively to ``window`` scroll events. When
``window.scrollY > 4``, the component toggles the ``.scrolled`` class and sets
``data-scrolled="true"``, transitioning its background from
``--md-sys-color-surface`` to ``--md-comp-top-app-bar-small-on-scroll-container-color``
(``--md-sys-color-surface-container``) with ``--md-sys-elevation-level2`` shadow
to visually separate the sticky header from scrolling article content.

**MD3 Specification Reference:**
`Components > App bars > Specs > Color > Scroll states <https://m3.material.io/components/app-bars/specs#9975d8e5-f69e-48bd-865e-af3c8eeba1d3>`_
