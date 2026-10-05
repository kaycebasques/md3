=========================
Typography
=========================

``md3`` implements the complete 15-role Material Design 3 typescale across its
three-tier design token architecture, optimized for long-form technical reading.

.. _typescale-tokens:

Typescale Tokens
----------------

All 15 MD3 typescale roles are defined as ``--md-sys-typescale-<role>-*`` CSS
custom properties (covering ``font``, ``size``, ``line-height``, ``weight``, and
``tracking``):

* **Display**: ``display-large`` (``57px``), ``display-medium`` (``45px``),
  ``display-small`` (``36px``)
* **Headline**: ``headline-large`` (``32px``), ``headline-medium`` (``28px``),
  ``headline-small`` (``24px``)
* **Title**: ``title-large`` (``22px``), ``title-medium`` (``16px``),
  ``title-small`` (``14px``)
* **Body**: ``body-large`` (``16px``), ``body-medium`` (``14px``),
  ``body-small`` (``12px``)
* **Label**: ``label-large`` (``14px``), ``label-medium`` (``12px``),
  ``label-small`` (``11px``)

**MD3 Specification Reference:**
`Styles > Typography > Type scale tokens > Baseline type style tokens <https://m3.material.io/styles/typography/type-scale-tokens#84c60429-0cca-4792-b3d2-2305e22429ba>`_

.. _applying-type-roles:

Applying Type Roles
-------------------

Semantic HTML elements inside ``.md3-article`` map directly to MD3 typescale
roles:

* ``<h1>`` -> ``headline-large`` (``2rem`` / ``32px``)
* ``<h2>`` -> ``headline-medium`` (``1.75rem`` / ``28px``)
* ``<h3>`` -> ``headline-small`` (``1.5rem`` / ``24px``)
* ``<h4>`` -> ``title-large`` (``1.375rem`` / ``22px``)
* ``<p>``, ``<li>`` -> ``body-large`` (``1rem`` / ``16px``, line-height ``1.6``)
* Navigation, chips, buttons, and table headers -> ``label-large`` /
  ``label-medium``

**MD3 Specification Reference:**
`Styles > Typography > Applying type > Roles <https://m3.material.io/styles/typography/applying-type#ab657e7c-cb93-45ff-92c6-686959dc19ae>`_

.. _inline-hyperlinks:

Inline Hyperlinks
-----------------

Inline links inside ``.md3-article`` use ``--md-sys-color-primary`` with an
underline offset (``text-underline-offset: 3px``) and a ``1px`` underline
thickness (``text-decoration-thickness: 1px``) that increases to ``2px`` on
``:hover``, ensuring links are distinguishable from surrounding body text by
more than color alone.

**MD3 Specification Reference:**
`Styles > Typography > Applying type > Color & contrast > Hyperlinked text <https://m3.material.io/styles/typography/applying-type#24856f70-f759-45df-a06c-92018f286083>`_

.. _default-typefaces:

Default Typefaces
-----------------

Reference typeface tokens define **Roboto** for brand and plain text
(``--md-ref-typeface-brand`` and ``--md-ref-typeface-plain``) and **Roboto Mono**
for code blocks, API signatures, and inline literals
(``--md-ref-typeface-code`` / ``--md-ref-typeface-mono``), loaded from Google
Fonts with graceful system font fallbacks.

**MD3 Specification Reference:**
`Styles > Typography > Fonts > Default typefaces <https://m3.material.io/styles/typography/fonts#dbd29949-f164-4065-bb36-49a765fbfe3d>`_
