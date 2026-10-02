=========================
Breadcrumbs
=========================

The ``.md3-breadcrumbs`` component at the top of ``<main class="md3-main">``
provides hierarchical wayfinding from the documentation root down to the active
page.

.. _breadcrumb-hierarchy:

Breadcrumb Hierarchy
--------------------

``.md3-breadcrumbs`` renders an accessible ``<nav aria-label="Breadcrumb">``
containing an ordered list (``<ol class="md3-breadcrumbs__list">``) of parent
documents from Sphinx's ``parents`` context variable:

* **Root Home Link**: Starts with a compact home icon link pointing to
  ``master_doc``.
* **Ancestor Links**: Each parent section link uses ``label-medium`` (``12px``,
  weight ``500``) typography in ``--md-sys-color-on-surface-variant``, transitioning
  to ``--md-sys-color-primary`` on hover, separated by ``/`` dividers
  (``aria-hidden="true"``).
* **Current Page Item**: The final item carries ``aria-current="page"`` and
  renders in ``--md-sys-color-on-surface``.

**MD3 Specification Reference:**
`Foundations > Accessible design > Structure > Hierarchy > Navigation <https://m3.material.io/foundations/designing/structure#b892ce17-68d6-4873-91f1-3c481359effd>`_
