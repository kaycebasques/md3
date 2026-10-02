=========================
Icon Buttons
=========================

The ``.md3-icon-btn`` component implements compact Material Design 3 icon
buttons used in the top app bar, navigation drawer header, and search dialog.

.. _compact-icon-buttons:

Compact Icon Buttons
--------------------

Under the ``-2`` compact density scale, ``.md3-icon-btn`` uses
``--md-comp-icon-button-xsmall-container-height: 32px``:

* **Dimensions**: ``32px x 32px`` circular hit target
  (``border-radius: var(--md-sys-shape-corner-full)``) with a ``20px`` icon.
* **Pressed Shape Morph**: Morphs to ``--md-sys-shape-corner-small`` (``8px``)
  on ``:active`` press.
* **State Layer**: Applies an ``8%`` hover and ``10%`` active state layer using
  ``--md-sys-color-on-surface-variant``.

**MD3 Specification Reference:**
`Components > Icon Buttons > Specs > Measurements <https://m3.material.io/components/icon-buttons/specs#c2d79537-2f48-4fa3-8241-27a5a46a6ecb>`_

.. _icon-button-tooltips:

Icon Button Tooltips
--------------------

Because icon buttons do not display visible text labels, every ``.md3-icon-btn``
in the theme includes a descriptive ``title`` attribute (alongside
``aria-label``) so sighted pointer users receive a native tooltip explaining the
button's action (e.g., ``"Toggle navigation drawer"``, ``"Toggle light/dark
theme"``, ``"Close search"``).

**MD3 Specification Reference:**
`Components > Icon buttons > Accessibility > Labeling elements <https://m3.material.io/components/icon-buttons/accessibility#a5b945ae-d453-424b-ae70-e008a5ebfdd1>`_

.. _aria-labeling-semantics:

ARIA Labeling Semantics
-----------------------

Every icon-only interactive control exposes an accessible name via
``aria-label`` and state attributes (such as ``aria-expanded`` on
``#drawer-toggle`` and ``aria-pressed`` on ``#theme-menu-btn``), while decorative
inline ``<svg>`` icons are hidden from the accessibility tree or paired with an
explicit parent ``aria-label``.

**MD3 Specification Reference:**
`Foundations > Accessible design > Elements > Labeling elements <https://m3.material.io/foundations/designing/elements#db9a0efd-8045-4c5f-8a4d-c80f9fb08c68>`_
