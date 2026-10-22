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
