=========================
Search Bar & Dialog
=========================

The ``<md3-search>`` component provides a compact pill-shaped search bar trigger
in the top app bar paired with a native HTML ``<dialog>`` modal quick-search
experience and a dedicated ``search.html`` page powered by **Pagefind** for
full-site search across the entire documentation site.

.. _compact-search-bar:

Compact Search Bar
------------------

In ``<md3-top-app-bar>``, the ``#search-bar-trigger`` element implements a
Material Design 3 Search Bar at ``-2`` compact density:

* **Container Height**: ``--md-comp-search-bar-container-height: 36px``
  (reduced from the ``56px`` default MD3 search bar height).
* **Container Shape**: ``--md-comp-search-bar-container-shape``
  (``var(--md-sys-shape-corner-full)`` / ``9999px`` full pill radius).
* **Surface Color**: ``--md-comp-search-bar-container-color``
  (``var(--md-sys-color-surface-container-high)``) with a ``1px solid`` subtle
  outline and a trailing ``<kbd>/</kbd>`` shortcut badge.
* **Progressive Enhancement**: The search bar is a native ``<a href="search.html">``
  link inside a ``<form action="search.html" method="get">`` fallback so search
  works cleanly across both modal and full-page workflows.

**MD3 Specification Reference:**
`Components > Search > Specs > Measurements > Search bar <https://m3.material.io/components/search/specs#6910a69a-1c33-42d1-83c5-3da9982e59e3>`_

.. _modal-search-dialog:

Modal Search Dialog
-------------------

Clicking ``#search-bar-trigger`` or pressing ``/`` or ``Cmd+K`` / ``Ctrl+K``
invokes ``Md3Search.open()``, which opens ``#md3-search-dialog`` via native
``HTMLDialogElement.showModal()``:

* **Container Shape**: ``--md-sys-shape-corner-extra-large`` (``28px``) modal
  surface container (``--md-sys-color-surface-container-high``) with
  ``--md-sys-elevation-level3`` shadow, ``min-width: 280px``, and
  ``max-width: 560px``.
* **Scrim Backdrop**: ``::backdrop`` styled with ``--md-sys-color-scrim`` at
  ``32%`` opacity and ``backdrop-filter: blur(2px)``.

**MD3 Specification Reference:**
`Components > Dialogs > Specs > Basic dialog measurements <https://m3.material.io/components/dialogs/specs#9a8c226b-19fa-4d6b-894e-e7d5ca9203e8>`_

.. _pagefind-full-site-search:

Pagefind Full-Site Search
-------------------------

During the ``build-finished`` Sphinx event, ``md3`` indexes all built HTML pages
(scoped to ``[data-pagefind-body]`` and excluding navigation chrome) into
``<outdir>/search/pagefind.js`` using ``pagefind.index.PagefindIndex``. Typing
into ``#md3-search-input`` (or ``#search-input`` on ``search.html``) queries the
Pagefind WebAssembly API across every page of the site and renders MD3 result
cards (``.md3-search-result-item``) featuring:

* Document title and primary section breadcrumb link.
* Matching ``<mark>`` highlighted context excerpts styled with
  ``--md-sys-color-primary-container`` and ``--md-sys-color-on-primary-container``.
* Nested section sub-results (``.md3-search-sub-results``) deep-linking
  directly to ``#section-id`` anchors within matching pages.

**MD3 Specification Reference:**
`Components > Search > Specs > Search view <https://m3.material.io/components/search/specs#dc1fa291-5ef3-4fd4-a2b6-e9d91b5f39ff>`_

.. _dialog-focus-return:

Dialog Focus Return
-------------------

``<md3-search>`` records ``document.activeElement`` before calling
``dialog.showModal()`` and automatically focuses ``#md3-search-input``. When the
dialog is dismissed via the ``Escape`` key, the ``#md3-search-close`` button, or
a backdrop click, ``Md3Search.close()`` clears the query and restores keyboard
focus to the element that originally triggered the dialog.

**MD3 Specification Reference:**
`Components > Dialogs > Accessibility > Keyboard navigation <https://m3.material.io/components/dialogs/accessibility#77f7ff34-ea07-4036-a45a-fc94428f43f6>`_
