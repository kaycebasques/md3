=========================
Buttons
=========================

The ``.md3-btn`` component family implements Material Design 3 Filled, Tonal,
Outlined, Elevated, and Text buttons at the ``-2`` compact density scale with
interactive shape morphing and state layers.

.. _compact-button-sizing:

Compact Button Sizing
---------------------

Under the ``-2`` compact density scale, buttons use
``--md-comp-button-xsmall-container-height: 32px`` and
``--md-comp-filled-button-container-height: 32px``:

* **Height**: ``32px`` with ``0 12px`` horizontal padding and ``8px`` icon-label
  gap.
* **Resting Shape**: ``--md-comp-filled-button-container-shape``
  (``var(--md-sys-shape-corner-full)`` / ``9999px`` pill) or ``12px`` square
  variant.
* **Typography**: ``--md-sys-typescale-label-large-font`` (``0.875rem`` /
  ``14px``, weight ``500``).

**MD3 Specification Reference:**
`Components > Buttons > Specs > Measurements & Corner sizes <https://m3.material.io/components/buttons/specs#73044a63-dc51-4401-bd4d-318920738ab3>`_

.. _button-color-variants:

Button Color Variants
---------------------

``md3`` provides five standard MD3 button emphasis variants:

1. **Filled (``.md3-btn--filled``)**: High emphasis; background
   ``--md-sys-color-primary`` and text ``--md-sys-color-on-primary``.
2. **Tonal (``.md3-btn--tonal``)**: Medium emphasis; background
   ``--md-sys-color-secondary-container`` and text
   ``--md-sys-color-on-secondary-container``.
3. **Outlined (``.md3-btn--outlined``)**: Medium emphasis with border;
   transparent background, ``1px solid var(--md-sys-color-outline)`` border,
   and ``--md-sys-color-primary`` text.
4. **Elevated (``.md3-btn--elevated``)**: Surface separation; background
   ``--md-sys-color-surface-container-low``, text ``--md-sys-color-primary``,
   and ``--md-sys-elevation-level1`` resting shadow.
5. **Text (``.md3-btn--text``)**: Low emphasis; transparent background and
   ``--md-sys-color-primary`` text with ``0 12px`` padding.

**MD3 Specification Reference:**
`Components > Buttons > Guidelines > Color styles <https://m3.material.io/components/buttons/guidelines#4e89da4d-a8fa-4e20-bb8d-b8a93eff3e3e>`_

.. _pressed-shape-morph:

Pressed Shape Morph
-------------------

When pressed (``:active``), ``.md3-btn`` morphs its corner radius from the
resting pill shape (``--md-sys-shape-corner-full``, ``9999px``) to
``--md-comp-filled-button-pressed-container-shape``
(``var(--md-sys-shape-corner-small)``, ``8px``) using the MD3 fast spatial
spring curve ``--md-sys-motion-spring-fast-spatial``
(``cubic-bezier(0.42, 1.67, 0.21, 0.90)``).

**MD3 Specification Reference:**
`Styles > Shape > Shape morph > Using shape morph <https://m3.material.io/styles/shape/shape-morph#7a4c6627-3452-4619-b4d1-93058c0b7685>`_

.. _state-layer-tokens:

State Layer Tokens
------------------

Interactive state overlays use the MD3 state-layer opacity tokens:

* ``--md-sys-state-hover-state-layer-opacity``: ``0.08`` (``8%``)
* ``--md-sys-state-focus-state-layer-opacity``: ``0.10`` (``10%``)
* ``--md-sys-state-pressed-state-layer-opacity``: ``0.10`` (``10%``)
* ``--md-sys-state-dragged-state-layer-opacity``: ``0.16`` (``16%``)

**MD3 Specification Reference:**
`Foundations > Interaction > States > State layers > State layer tokens & values <https://m3.material.io/foundations/interaction/states/state-layers#bf9b84b2-690c-44b2-8429-8c42dc012d43>`_

.. _interaction-states:

Interaction States
------------------

Buttons and interactive surfaces apply state layers via ``::after`` overlays or
``color-mix()`` blending the component's content color (``on-primary``,
``on-secondary-container``, or ``primary``) at the active state opacity over the
container surface.

**MD3 Specification Reference:**
`Foundations > Interaction > States > Applying states > Focused <https://m3.material.io/foundations/interaction/states/applying-states#bc6d6853-48ef-490e-8076-448e89e69f0f>`_

.. _keyboard-focus-ring:

Keyboard Focus Ring
-------------------

All interactive elements display an unmistakable keyboard focus indicator on
``:focus-visible`` using ``outline: 3px solid var(--md-sys-color-secondary)``
and ``outline-offset: 2px``, ensuring high-contrast visibility against both
light and dark surfaces.

**MD3 Specification Reference:**
`Foundations > Interaction > States > Applying states > Keyboard focus indicator <https://m3.material.io/foundations/interaction/states/applying-states#9edb181a-ed5e-4961-b3d0-cae33125a4a9>`_
