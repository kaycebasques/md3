===========================
Navigation Drawer (Sidebar)
===========================

The ``<md3-sidebar>`` component implements a Material Design 3 Navigation Drawer
with **one-level-at-a-time progressive disclosure**, scaling cleanly from small
projects to massive multi-thousand-page documentation sites.

.. _compact-navigation-items:

Compact Navigation Items
------------------------

Under the ``-2`` compact density scale, navigation drawer items use
``--md-comp-navigation-drawer-active-indicator-height: 32px`` and
``--md-comp-navigation-drawer-container-width: 256px``:

* **Item Height**: ``32px`` (reduced from the ``56px`` default MD3 drawer item
  height so large documentation sections fit comfortably without scrolling).
* **Active Indicator Shape**: ``--md-comp-navigation-drawer-active-indicator-shape``
  (``var(--md-sys-shape-corner-full)`` / ``9999px`` pill).
* **Active Indicator Color**: ``--md-comp-navigation-drawer-active-indicator-color``
  (``var(--md-sys-color-secondary-container)``) with
  ``--md-sys-color-on-secondary-container`` label text and ``aria-current="page"``.

**MD3 Specification Reference:**
`Components > Navigation Drawer > Specs > Measurements <https://m3.material.io/components/navigation-drawer/specs#73da5c32-aecf-4c88-849b-77310fbc3b77>`_

.. _progressive-disclosure:

Progressive Disclosure
----------------------

Large Sphinx documentation sites (such as monorepos with thousands of documents)
become unusable when the entire multi-level ``toctree`` is rendered into every
page's sidebar. ``md3`` solves this in ``md3/__init__.py``
(``compute_progressive_navigation``) and ``<md3-sidebar>`` using **progressive
disclosure**:

1. **Strictly One Level at a Time**: On any page, ``<md3-sidebar>`` displays
   only a single active hierarchy level:

   * If the current page has child documents in the ``toctree``, the sidebar
     displays the current page as the active section header and lists only its
     **immediate children** (1 level deep).
   * If the current page is a leaf document (no children), the sidebar displays
     its parent section as the header and lists the **immediate siblings** at
     that level.
   * On the root page, the sidebar lists only the top-level documents.

2. **Ancestor Drill-Up Links**: When navigated into a nested subsection, an
   ``.md3-sidebar__ancestors`` list above the section items provides one-click
   back-links (with a leading back arrow icon) to every ancestor section up to
   the top-level section.
3. **Child Chevron Indicators**: Items that contain their own nested child
   documents render a ``.md3-nav-item__chevron`` trailing chevron icon and the
   ``.has-children`` class so readers know which items drill down deeper.
4. **Live Section Filter**: Whenever the current level contains ``8`` or more
   items, ``<md3-sidebar>`` renders a compact ``#sidebar-filter-input`` search
   box at the top of the drawer that filters items in real time and hides empty
   category captions.

**MD3 Specification Reference:**
`Components > Navigation Drawer > Guidelines > Usage <https://m3.material.io/components/navigation-drawer/guidelines#761e9679-2e72-4a85-894d-55bc3666b567>`_

.. _modal-navigation-drawer:

Modal Navigation Drawer
-----------------------

On viewports narrower than ``840px`` (Compact and Medium window size classes),
``<md3-sidebar>`` transitions from a persistent sticky column into a **modal
navigation drawer**:

* Positioned with ``position: fixed; top: 0; left: 0; bottom: 0; z-index: 200``.
* Hidden off-canvas via ``transform: translateX(-100%)`` at rest and animated
  into view (``transform: translateX(0)``) using
  ``--md-sys-motion-easing-emphasized-decelerate`` when opened.
* Paired with ``#md3-backdrop`` (``.md3-backdrop``) which applies a
  ``--md-sys-color-scrim`` overlay at ``32%`` opacity over the main content.
* Supports native HTML ``popover="auto"`` fallback so the drawer remains operable
  even when JavaScript is disabled (``:root.no-js``).

**MD3 Specification Reference:**
`Components > Navigation Drawer > Specs > Modal navigation drawer <https://m3.material.io/components/navigation-drawer/specs#368147de-9661-4a28-9fc1-ce2f8c9eac40>`_

.. _drawer-dismissal:

Drawer Dismissal
----------------

When open as a modal drawer on mobile/tablet viewports, ``<md3-sidebar>`` can be
dismissed via three standard MD3 interactions, all of which restore keyboard
focus to the ``#drawer-toggle`` button:

1. Clicking the ``#md3-backdrop`` scrim overlay.
2. Pressing the ``Escape`` key.
3. Clicking the ``#sidebar-close`` icon button or selecting a navigation link.

**MD3 Specification Reference:**
`Components > Navigation Drawer > Guidelines > Behavior > Visibility <https://m3.material.io/components/navigation-drawer/guidelines#046936be-3330-492b-94d3-5a8cb41b17e9>`_

.. _navigation-list-items:

Navigation List Items
---------------------

Navigation items inside ``.md3-nav-list`` and the right-hand ``.md3-toc__nav``
follow MD3 list item spacing and state-layer specifications:

* Horizontal padding of ``12px`` (``--md-sys-spacing-3``) and vertical gap of
  ``2px`` between items.
* Hover state layer using ``color-mix(in srgb, var(--md-sys-color-on-surface) 8%, transparent)``.
* Truncation protection and flexbox alignment so trailing chevron icons stay
  pinned to the right edge.

**MD3 Specification Reference:**
`Components > Lists > Specs > One-line lists <https://m3.material.io/components/lists/specs#eeeb78e0-265d-4e81-96ba-c2340c348a90>`_
