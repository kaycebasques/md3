Testing
=======

Quickstart
----------

Run all tests across the repository:

.. code-block:: console

   ./bazelisk test //tests/...

Run a single test target:

.. code-block:: console

   ./bazelisk test //tests:layout_test

Overview
--------

All tests live in ``tests/`` and are declared as standard ``py_test`` targets
in ``tests/BUILD.bazel`` with explicit dependencies on only what each test
needs.

``tests/harness.py`` provides three standalone context managers:

* ``build_docs``: builds an isolated Sphinx site in a temporary directory and
  yields the output directory path.
* ``DocsServer``: serves a built documentation directory over a local
  ``ThreadingHTTPServer``.
* ``run_playwright``: launches hermetic Chrome for Testing via Playwright and
  yields a browser page.

MD3 Compliance
--------------

``tests/tokens_test.py`` verifies the :doc:`/md3` token hierarchy, ensures no
unused tokens accumulate in ``ref.css`` or ``sys.css``, checks that component
stylesheets do not define ``:root`` blocks, custom properties (``--*``), or raw
color literals, and validates all ``DOCS*_URL`` links and anchors referenced in
``tests/*_test.py``.

Every component test suite in ``tests/`` includes a ``test_md3`` method that verifies:

* Custom element registration and bounding box geometry.
* Computed styles against ``SYS_COLORS``, ``SYS_TYPESCALE``, and ``SYS_STATE`` in ``tests/harness.py`` across resting, ``:hover``, ``:active``, and ``:focus-visible`` states.
* Failure messages linking to both our documentation and ``https://m3.material.io/``. Standard MD3 measurements are not repeated in prose documentation; components that apply `MD3 density scaling <https://m3.material.io/foundations/layout/grids-spacing/density>`_ document their scale in a ``Density`` section on the component's documentation page, and any intentional deviation from MD3 specs must be documented in a ``Deviations`` section and linked from that assertion in ``test_md3``.
