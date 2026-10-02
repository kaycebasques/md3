=========================
Chips
=========================

The ``.md3-chip`` component implements Material Design 3 Assist and Filter
Chips used for metadata tags, release version badges, and category filters.

.. _assist-and-filter-chips:

Assist and Filter Chips
-----------------------

Under the ``-2`` compact density scale, ``.md3-chip`` uses
``--md-comp-assist-chip-container-height: 32px``:

* **Container Height**: ``32px`` with ``0 12px`` horizontal padding, ``18px``
  icon size, and ``8px`` icon-label gap.
* **Container Shape**: ``--md-comp-assist-chip-container-shape``
  (``var(--md-sys-shape-corner-small)`` / ``8px`` corner radius).
* **Outlined Assist Chip (``.md3-chip``)**: Transparent surface with
  ``1px solid var(--md-sys-color-outline-variant)`` border and
  ``--md-sys-color-on-surface-variant`` label text.
* **Selected Filter Chip (``.md3-chip--selected``)**: Filled with
  ``--md-sys-color-secondary-container``, ``--md-sys-color-on-secondary-container``
  text, and transparent border.

**MD3 Specification Reference:**
`Components > Chips > Specs > Assist chip measurements <https://m3.material.io/components/chips/specs#9faeb601-c522-4a5a-a263-f1b1ac7504d6>`_
