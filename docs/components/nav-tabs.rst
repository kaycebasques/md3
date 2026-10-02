=========================
Navigation Tabs
=========================

The ``<md3-nav-tabs>`` component implements a Material Design 3 **Primary
Navigation Tab Bar** positioned directly below ``<md3-top-app-bar>``. Together
with the progressive disclosure sidebar, top-level tabs allow readers on large
documentation sites to switch instantly between major site sections while keeping
the left navigation drawer focused on the active section.

.. _primary-navigation-tabs:

Primary Navigation Tabs
-----------------------

``<md3-nav-tabs>`` is populated automatically from the root document's top-level
``toctree`` entries (``md3_nav_tabs`` in ``paz/__init__.py``) and styled with
MD3 primary navigation tab tokens:

* **Container Height**: ``--md-comp-primary-navigation-tab-container-height: 36px``
  (compact ``-2`` density adaptation of the ``48px`` default primary tab bar).
* **Container Color**: ``--md-comp-primary-navigation-tab-container-color``
  (``var(--md-sys-color-surface)``) with a ``1px solid
  var(--md-sys-color-outline-variant)`` bottom divider.
* **Inactive Tab Label**: ``--md-comp-primary-navigation-tab-with-label-text-inactive-label-text-color``
  (``var(--md-sys-color-on-surface-variant)``) using ``title-small`` typography
  (``0.875rem`` / ``14px``, weight ``500``).
* **Active Tab State**: ``.md3-nav-tabs__link.active`` sets
  ``--md-comp-primary-navigation-tab-with-label-text-active-label-text-color``
  (``var(--md-sys-color-primary)``) and renders a ``3px`` pill-shaped bottom
  active indicator (``--md-comp-primary-navigation-tab-active-indicator-height: 3px``,
  ``border-radius: 3px 3px 0 0``) in ``--md-sys-color-primary``.
* **Horizontal Overflow**: On narrow viewports or sites with many top-level
  sections, ``.md3-nav-tabs__nav`` scrolls horizontally without visible
  scrollbars and centers the active tab automatically on load.

**MD3 Specification Reference:**
`Components > Tabs > Specs > Primary tabs <https://m3.material.io/components/tabs/specs#8602158e-a13b-432e-8133-b9cb34d61678>`_

.. _tab-keyboard-navigation:

Tab Keyboard Navigation
-----------------------

``<md3-nav-tabs>`` wraps its links in ``<nav class="md3-nav-tabs__nav"
aria-label="Section navigation">`` and enhances keyboard accessibility in
``Md3NavTabs``:

* Pressing ``ArrowRight`` or ``ArrowLeft`` while focused on a tab moves focus to
  the next or previous top-level tab (wrapping around at the ends).
* Pressing ``Home`` or ``End`` jumps focus to the first or last tab.
* The active section tab includes ``aria-current="page"`` when on the section's
  landing page.

**MD3 Specification Reference:**
`Components > Tabs > Accessibility > Keyboard navigation <https://m3.material.io/components/tabs/accessibility#a1ebaebd-1bb4-4401-9962-8b30a563e49e>`_
