Material Design 3
=================

``md3`` implements `Material Design 3 <https://m3.material.io/>`_ using vanilla
HTML, CSS, and progressive-enhancement JavaScript.

Tokens
------

``md3`` uses a two-tier CSS custom property hierarchy modeled after
`Material Design 3 design tokens <https://m3.material.io/foundations/design-tokens/overview>`_.
Every ``--md-ref-*`` and ``--md-sys-*`` variable name is a 1:1 CSS custom
property mapping of an official dot-separated token name from ``m3.material.io``
(prefixing with ``--`` and replacing ``.`` with ``-``, e.g.
``md.sys.color.primary`` becomes ``--md-sys-color-primary``):

* ``md3/tokens/ref.css`` defines ``--md-ref-*`` reference tokens on ``:root``
  from `MD3 baseline color tokens <https://m3.material.io/styles/color/static/baseline>`_
  (``md.ref.palette.*``) and `MD3 type scale tokens <https://m3.material.io/styles/typography/type-scale-tokens>`_
  (``md.ref.typeface.*``).
* ``md3/tokens/sys.css`` defines ``--md-sys-*`` system tokens on ``:root``
  referencing ``var(--md-ref-*)`` across `color <https://m3.material.io/styles/color/static/baseline>`_
  (``md.sys.color.*``), `typography <https://m3.material.io/styles/typography/type-scale-tokens>`_
  (``md.sys.typescale.*``), and `interaction states <https://m3.material.io/foundations/interaction/states/state-layers>`_
  / `focus indicators <https://m3.material.io/foundations/interaction/states/applying-states>`_
  (``md.sys.state.*``).
* Component stylesheets in ``md3/components/md3/`` and ``md3/components/app/``
  consume ``var(--md-sys-*)`` tokens (plus ``var(--md3-density)`` for density
  scaling) and literal component measurements; they do not define ``:root``
  blocks, custom properties (``--*``), or raw color literals.
* Only tokens actively used by implemented components are defined in
  ``ref.css`` and ``sys.css``.

.. _density:

Density
-------

``md3`` implements the `MD3 density scale <https://m3.material.io/foundations/layout/grids-spacing/density>`_,
where each step on the scale (``0``, ``-1``, ``-2``, ``-3``) adjusts a
component's baseline height by ``4px`` via the ``--md3-density`` variable set on
``<html>``:

.. code-block:: css

   height: calc(<baseline> + var(--md3-density) * 4px);

To configure the density scale in ``conf.py`` (``-3``, ``-2``, ``-1``, or ``0``):

.. code-block:: python

   html_theme_options = {
       "density": -2,
   }

Components that apply density scaling document their formula in a ``Density``
section on their component page.

Deviations
----------

* `MD3 density guidelines <https://m3.material.io/foundations/layout/grids-spacing/density>`_
  state that high density should not be applied by default (recommending ``0``
  as the default scale). Because ``md3`` targets technical documentation sites
  where maximizing information density is a primary goal,
  ``html_theme_options["density"]`` defaults to ``-3`` instead of ``0``. Set
  ``"density": 0`` in ``html_theme_options`` to use baseline MD3 sizing.
