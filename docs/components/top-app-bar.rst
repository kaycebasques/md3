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

.. _universal-subsite-header:

Universal Subsite Header
------------------------

During the ``build-finished`` Sphinx event, ``postprocess_universal_header`` in
``md3/__init__.py`` scans all HTML files in the output directory for
``<!-- md3-sentinel -->`` or ``<!-- pw-sentinel -->`` comments (used by external
Doxygen C++ API and Rustdoc Rust API subsites) and injects:

* ``_static/app.css``, ``_static/app.js``, and the zero-FOUC theme bootstrap
  script into ``<head>``, plus ``data-content_root`` and ``data-baseurl`` on
  ``<html>``.
* ``#md3-skip-link`` pointing to ``#main`` (Sphinx), ``#doc-content`` (Doxygen),
  or ``#main-content`` (Rustdoc), transferring keyboard focus on activation.
* ``#md3-universal-header`` containing ``<md3-top-app-bar>``, ``<md3-nav-tabs>``,
  and ``.md3-subsite-breadcrumbs``, plus ``<md3-search>`` and ``#md3-backdrop``.
  To integrate scalably with any third-party subsite layout without breaking
  native CSS rules:

  * ``#md3-universal-header`` uses ``position: fixed; top: 0; left: 0; right: 0``
    and ``body:has(#md3-universal-header)`` applies
    ``padding-top: var(--md3-universal-header-height, 128px)`` (`92px` without
    tabs, `128px` with ``<md3-nav-tabs>``), keeping the injected header out of
    ``body.rustdoc``'s horizontal ``display: flex; flex-direction: row;
    flex-wrap: nowrap`` flow so ``nav.sidebar`` and ``main`` remain side-by-side.
  * Global ``box-sizing: border-box`` and code/typography resets in ``app.css``
    are scoped strictly to ``md3-app`` and injected MD3 chrome so Doxygen's
    ``navtree.js`` ``createIndent`` expand/collapse arrows (``.arrow { width:
    16px; padding-left: ... }``) retain ``box-sizing: content-box`` and never
    overlap ``.label a`` links.
  * Doxygen ``#side-nav`` (`width: 250px`) and ``#doc-content``
    (`margin-left: 256px`) use non-``!important`` horizontal dimensions so
    Doxygen's ``resize.js`` splitter can dynamically update inline styles.
* Mobile drawer synchronization on viewports ``< 840px`` (toggling
  ``nav.sidebar.shown`` / ``html.src-sidebar-expanded`` on Rustdoc and
  ``body.md3-doxygen-nav-open`` on Doxygen) and local/staging URL rewriting
  (``rewriteUrls()``).

**MD3 Specification Reference:**
`Components > App bars > Specs > Measurements > Small app bar <https://m3.material.io/components/app-bars/specs#fac99130-8bb8-498c-8cb8-16ea056cc3e1>`_

