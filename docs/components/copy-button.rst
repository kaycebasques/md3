=========================
Code Copy Button
=========================

The ``<md3-copy-button>`` component provides one-click clipboard copying for
Sphinx ``div.highlight`` code blocks.

.. _code-copy-interaction:

Code Copy Interaction
---------------------

During ``<md3-app>`` initialization, ``Md3App.initCodeCopy()`` upgrades every
``div.highlight`` block containing a ``<pre>`` element by appending an
``<md3-copy-button class="md3-code-copy-btn">`` element:

* **Accessibility**: Automatically sets ``role="button"``, ``tabindex="0"``,
  ``aria-label="Copy code snippet"``, and ``title="Copy code snippet"``, and
  activates on both mouse click and ``Enter`` / ``Space`` keydown events.
* **Clipboard & Feedback**: Copies the ``<pre>`` text content via
  ``navigator.clipboard.writeText()`` (with a ``document.execCommand('copy')``
  fallback), adds the ``.copied`` state class, changes the visible label from
  ``Copy`` to ``Copied!``, and resets after ``2000ms``.

**MD3 Specification Reference:**
`Components > Buttons > Specs > Baseline tokens <https://m3.material.io/components/buttons/specs#c305d304-a6c0-466a-a48c-8d0718a29ae2>`_
