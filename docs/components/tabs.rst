Tabs
====

``<md3-tabs>`` renders the root document's top-level ``toctree`` entries as
`Material Design 3 primary navigation tabs <https://m3.material.io/components/tabs/specs>`_.

Configuration
-------------

Top-level navigation tabs are enabled by default. To disable them in ``conf.py``:

.. code-block:: python

   html_theme_options = {
       "tabs": False,
   }

Accessibility
-------------

* Links are rendered inside ``<nav aria-label="Section navigation">`` with
  ``aria-current="page"`` on the active section.
* ``ArrowRight``, ``ArrowLeft``, ``Home``, and ``End`` move focus across tabs
  (`MD3 tabs keyboard navigation <https://m3.material.io/components/tabs/accessibility#a1ebaebd-1bb4-4401-9962-8b30a563e49e>`_).
