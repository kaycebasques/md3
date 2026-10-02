=========================
Data Tables
=========================

Sphinx ``table.docutils`` tables are styled as compact Material Design 3 data
tables with rounded container borders, tonal header rows, and tabular numeral
alignment.

.. _compact-table-density:

Compact Table Density
---------------------

Under the ``-2`` compact density scale, ``table.docutils`` cells use ``8px 16px``
padding (``padding-top: 8px; padding-bottom: 8px``) and ``body-medium``
(``14px``) typography so multi-column reference tables remain scannable without
horizontal overflow:

* **Container**: ``border-radius: var(--md-sys-shape-corner-medium)`` (``12px``)
  with ``1px solid var(--md-sys-color-outline-variant)`` outer border.
* **Header Row (``thead th``)**: ``--md-sys-color-surface-container-high``
  background with ``label-large`` (``500`` weight) column titles.
* **Row Hover**: ``tbody tr:hover`` applies a ``4%`` ``on-surface`` state layer.

**MD3 Specification Reference:**
`Foundations > Layout > Grids & spacing > Density > Information density <https://m3.material.io/foundations/layout/grids-spacing/density#7bd57971-f3eb-4050-a57e-be5698d048bc>`_

.. _tabular-numerals:

Tabular Numerals
----------------

All ``table.docutils`` elements set ``font-variant-numeric: tabular-nums`` so
numeric columns, token measurements, benchmarks, and version numbers align
vertically across rows.

**MD3 Specification Reference:**
`Styles > Typography > Applying type > Typesetting > Tabular numerals <https://m3.material.io/styles/typography/applying-type#f0f79df7-3174-4012-871e-93ce9a89d08b>`_
