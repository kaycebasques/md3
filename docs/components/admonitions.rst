=========================
Admonitions
=========================

Sphinx admonition directives (``.. note::``, ``.. tip::``, ``.. warning::``,
``.. danger::``, ``.. error::``, ``.. caution::``, ``.. important::``) are
styled as Material Design 3 tonal callout containers.

.. _callout-containers:

Callout Containers
------------------

Every ``div.admonition`` container renders with:

* **Container Shape**: ``--md-sys-shape-corner-medium`` (``12px``) with a
  ``4px solid`` semantic accent bar along the leading ``border-left`` edge.
* **Surface Container**: ``--md-sys-color-surface-container-low`` background with
  ``14px 16px`` compact padding.
* **Semantic Color Mapping**:

  * **Informational (``note``, ``seealso``)**: ``--md-sys-color-primary`` accent
    border and title icon.
  * **Constructive (``tip``, ``hint``, ``important``)**: ``--md-sys-color-tertiary``
    accent border and title icon.
  * **Destructive / Alert (``warning``, ``caution``, ``danger``, ``error``)**:
    ``--md-sys-color-error`` accent border with a subtle ``--md-sys-color-error-container``
    surface tint.

**MD3 Specification Reference:**
`Components > Cards > Specs > Outlined card <https://m3.material.io/components/cards/specs#9ad208b3-3d37-475c-a0eb-68cf845718f8>`_
