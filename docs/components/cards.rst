================================
Cards, Shape, Elevation & Motion
================================

The ``.md3-card`` component family provides Material Design 3 Elevated, Filled,
and Outlined surface containers, pagination cards, and the underlying MD3 shape,
elevation, and motion token systems.

.. _card-variants:

Card Variants
-------------

``paz`` implements all three official Material Design 3 card variants inside a
responsive ``.md3-card-grid`` layout:

1. **Outlined Card (``.md3-card--outlined``)**: ``--md-sys-color-surface``
   background, ``1px solid var(--md-sys-color-outline-variant)`` border, and
   ``--md-sys-elevation-level0`` resting shadow.
2. **Filled Card (``.md3-card--filled``)**: ``--md-sys-color-surface-container-highest``
   background, transparent border, and ``--md-sys-elevation-level0`` resting
   shadow.
3. **Elevated Card (``.md3-card--elevated``)**: ``--md-sys-color-surface-container-low``
   background, transparent border, and ``--md-sys-elevation-level1`` resting
   shadow that lifts to ``--md-sys-elevation-level2`` on hover.

**MD3 Specification Reference:**
`Components > Cards > Specs > Measurements <https://m3.material.io/components/cards/specs#038b4a49-3a7f-4fce-be8c-89c1155b4c82>`_

.. _pagination-cards:

Pagination Cards
----------------

At the bottom of each documentation page, ``.md3-pagination`` renders Previous
and Next page links (``.md3-pagination__link--prev`` and
``.md3-pagination__link--next``) as interactive outlined MD3 cards with
``--md-sys-shape-corner-medium`` (``12px``) corners, directional overline
labels, and primary hover borders.

**MD3 Specification Reference:**
`Components > Cards > Specs > Outlined card color <https://m3.material.io/components/cards/specs#9776d7d8-c583-4824-bb77-39cef535548d>`_

.. _corner-radius-scale:

Corner Radius Scale
-------------------

The MD3 shape scale defines corner radius tokens (``--md-sys-shape-corner-*``)
used consistently across cards, dialogs, chips, and buttons:

* ``--md-sys-shape-corner-none``: ``0px``
* ``--md-sys-shape-corner-extra-small``: ``4px``
* ``--md-sys-shape-corner-small``: ``8px``
* ``--md-sys-shape-corner-medium``: ``12px``
* ``--md-sys-shape-corner-large``: ``16px``
* ``--md-sys-shape-corner-large-increased``: ``20px``
* ``--md-sys-shape-corner-extra-large``: ``28px``
* ``--md-sys-shape-corner-extra-large-increased``: ``32px``
* ``--md-sys-shape-corner-extra-extra-large``: ``48px``
* ``--md-sys-shape-corner-full``: ``9999px``

**MD3 Specification Reference:**
`Styles > Shape > Corner radius scale > Corner radius scale <https://m3.material.io/styles/shape/corner-radius-scale#7c4b83c5-25e3-4337-889d-4f24a2b93e6d>`_

.. _semantic-shape-tokens:

Semantic Shape Tokens
---------------------

Components bind to semantic ``--md-sys-shape-corner-*`` tokens according to
their container scale: cards, square buttons, tables, and admonitions use
``medium`` (``12px``), modal navigation drawers use ``large`` (``16px``) on
their trailing edge, search dialogs use ``extra-large`` (``28px``), and round
buttons, badges, and active navigation indicators use ``full`` (``9999px``).

**MD3 Specification Reference:**
`Styles > Shape > Corner radius scale > Shape tokens <https://m3.material.io/styles/shape/corner-radius-scale#9a2814ed-bd01-43c8-a1bc-29d486ee7f35>`_

.. _elevation-levels:

Elevation Levels
----------------

Material Design 3 defines 6 discrete elevation levels (``level0`` through
``level5``) combining tonal surface container colors with ambient and key
box-shadows.

**MD3 Specification Reference:**
`Styles > Elevation > Overview > All surfaces and components have elevation values <https://m3.material.io/styles/elevation/overview#6585e78e-773c-46d2-b7e6-2eea780f7eb5>`_

.. _elevation-tokens:

Elevation Tokens
----------------

All 6 ``--md-sys-elevation-level*`` tokens are declared on ``:root``:

* ``--md-sys-elevation-level0``: ``none``
* ``--md-sys-elevation-level1``: ``0px 1px 2px 0px rgba(0, 0, 0, 0.3), 0px 1px 3px 1px rgba(0, 0, 0, 0.15)``
* ``--md-sys-elevation-level2``: ``0px 1px 2px 0px rgba(0, 0, 0, 0.3), 0px 2px 6px 2px rgba(0, 0, 0, 0.15)``
* ``--md-sys-elevation-level3``: ``0px 4px 8px 3px rgba(0, 0, 0, 0.15), 0px 1px 3px 0px rgba(0, 0, 0, 0.3)``
* ``--md-sys-elevation-level4``: ``0px 6px 10px 4px rgba(0, 0, 0, 0.15), 0px 2px 3px 0px rgba(0, 0, 0, 0.3)``
* ``--md-sys-elevation-level5``: ``0px 8px 12px 6px rgba(0, 0, 0, 0.15), 0px 4px 4px 0px rgba(0, 0, 0, 0.3)``

**MD3 Specification Reference:**
`Styles > Elevation > Tokens > Tokens <https://m3.material.io/styles/elevation/tokens#cdec0b55-abbe-46f8-a3aa-07f0ea3b76da>`_

.. _component-resting-elevation:

Component Resting Elevation
---------------------------

Components use their prescribed MD3 resting elevation:

* Outlined & Filled Cards: ``level0``
* Elevated Cards & Elevated Buttons: ``level1`` (hovering to ``level2``)
* Scrolled Top App Bar & Popover Menus: ``level2``
* Modal Search Dialog & Modal Drawer: ``level3``

**MD3 Specification Reference:**
`Styles > Elevation > Tokens > Component elevation <https://m3.material.io/styles/elevation/tokens#df721a00-888e-4c5e-bfe1-5d905f167aaa>`_

.. _scrim-overlays:

Scrim Overlays
--------------

Modal surfaces (the mobile navigation drawer ``#md3-backdrop`` and the search
dialog ``::backdrop``) apply a scrim overlay using ``--md-sys-color-scrim`` at
``32%`` opacity to attenuate background content and direct focus to the modal
container.

**MD3 Specification Reference:**
`Styles > Elevation > Applying elevation > Scrims <https://m3.material.io/styles/elevation/applying-elevation#92b9fb39-f0c4-4829-8e4d-97ac512976aa>`_

.. _motion-easing-and-duration:

Motion Easing and Duration
--------------------------

Transitions across cards, drawers, and interactive states use the MD3 motion
easing curves paired with duration tokens (``short1: 50ms`` through
``extra-long4: 1000ms``).

**MD3 Specification Reference:**
`Styles > Motion > Easing and duration > Applying easing and duration > Suggested easing and duration pairs <https://m3.material.io/styles/motion/easing-and-duration/applying-easing-and-duration#6409707e-1253-449c-b588-d27fe53bd025>`_

.. _motion-tokens:

Motion Tokens
-------------

Easing and duration tokens are defined on ``:root``:

* ``--md-sys-motion-easing-standard``: ``cubic-bezier(0.2, 0, 0, 1)``
* ``--md-sys-motion-easing-emphasized-decelerate``: ``cubic-bezier(0.05, 0.7, 0.1, 1.0)``
* ``--md-sys-motion-easing-emphasized-accelerate``: ``cubic-bezier(0.3, 0.0, 0.8, 0.15)``
* ``--md-sys-motion-spring-fast-spatial``: ``cubic-bezier(0.42, 1.67, 0.21, 0.90)``

**MD3 Specification Reference:**
`Styles > Motion > Easing and duration > Tokens & specs > Tokens <https://m3.material.io/styles/motion/easing-and-duration/tokens-specs#2c0659e2-a2c8-4d7b-8964-5b8dce012f7c>`_
