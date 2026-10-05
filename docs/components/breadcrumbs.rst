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

.. _universal-subsite-breadcrumbs:

Universal Subsite Breadcrumbs
-----------------------------

In addition to computing the full ``md3_breadcrumb_parents`` ancestor chain from
the Sphinx ``toctree`` graph, ``postprocess_universal_header`` generates
``.md3-subsite-breadcrumbs`` inside ``#md3-universal-header`` for external Doxygen
and Rustdoc subsite pages:

* **URL-Hierarchy Sphinx Ancestors**: Walks the subsite file's parent directory
  prefixes (e.g., ``api`` for ``api/cc/group__pw__bytes.html``) to match any
  ancestor Sphinx documents (such as ``api/index`` -> ``Reference``) and their
  ``toctree`` parents, automatically inserting ``Home / Reference / ...`` and
  activating the corresponding top-level tab in ``<md3-nav-tabs>``.
* **Subsite & Doxygen Group Trail**: Appends ``C++ API`` (plus any parent module
  groups from Doxygen ``.ingroups``) and ``<Page Title>`` for Doxygen pages, or
  ``Rust API / <Crate or Item Title>`` for Rustdoc pages.

**MD3 Specification Reference:**
`Foundations > Accessible design > Structure > Hierarchy > Navigation <https://m3.material.io/foundations/designing/structure#b892ce17-68d6-4873-91f1-3c481359effd>`_

