=========================
Table of Contents (TOC)
=========================

The ``<md3-toc>`` component renders the secondary right-hand supporting pane
("On this page") on Large viewports (``>= 1200px``) and pairs with the compact
mobile/tablet popover menu on narrower viewports.

.. _scrollspy-navigation:

Scrollspy Navigation
--------------------

``<md3-toc>`` uses an ``IntersectionObserver`` with
``rootMargin: '-70px 0px -70% 0px'`` to observe ``<h2>`` and ``<h3>`` section
headings inside ``.md3-article`` as the reader scrolls:

* **Active Indicator**: The currently visible section's link in ``#md3-toc-nav``
  receives the ``.active`` class, styling its left border with a ``2px solid
  var(--md-sys-color-primary)`` accent indicator, ``--md-sys-color-primary``
  text color, and ``color-mix(in srgb, var(--md-sys-color-primary) 8%, transparent)``
  background tint.
* **Automatic Heading Discovery**: When a page does not supply a multi-item
  Sphinx local TOC, ``Md3Toc.initScrollspy()`` automatically builds the in-page
  navigation list from the article's ``h2`` and ``h3`` headings.
* **Back to Top Action**: Includes the ``#back-to-top`` action button that
  smoothly scrolls the viewport back to the top of the document.

**MD3 Specification Reference:**
`Foundations > Layout > Scaffold > Panes > Panes <https://m3.material.io/foundations/layout/scaffold/panes#91f7daf8-1aab-4603-8865-013b6b5f5257>`_
