=========================
Color System & Tokens
=========================

``paz`` implements the complete Material Design 3 three-tier token architecture
(``--md-ref-*``, ``--md-sys-*``, ``--md-comp-*``) and all 26 semantic color
roles across light and dark themes.

.. _design-tokens-overview:

Design Tokens Overview
----------------------

Design tokens store every visual design attribute—color tones, typography scales,
corner radii, elevation shadows, state opacities, and spatial increments—as CSS
custom properties on ``:root`` in ``paz/components/app.css``, eliminating
hardcoded magic values in component rules.

**MD3 Specification Reference:**
`Foundations > Design Tokens > Overview > What’s a design token? <https://m3.material.io/foundations/design-tokens/overview#0aa7c44c-d528-4217-9aed-80d978815723>`_

.. _token-classes:

Token Classes
-------------

The stylesheet organizes tokens into the three canonical MD3 token classes:

1. **Reference Tokens (``--md-ref-*``)**: Raw tonal palette hex values
   (``--md-ref-palette-primary40``) and font family stacks
   (``--md-ref-typeface-plain``).
2. **System Tokens (``--md-sys-*``)**: Semantic roles (``--md-sys-color-primary``,
   ``--md-sys-typescale-body-large-size``, ``--md-sys-shape-corner-medium``) that
   adapt dynamically to theme and density contexts.
3. **Component Tokens (``--md-comp-*``)**: Component-specific measurements and
   surface bindings (``--md-comp-top-app-bar-small-container-height``,
   ``--md-comp-navigation-drawer-active-indicator-height``).

**MD3 Specification Reference:**
`Foundations > Design Tokens > Overview > Classes of tokens <https://m3.material.io/foundations/design-tokens/overview#c2c235dd-05db-4248-be47-48dfd8a21669>`_

.. _color-roles-overview:

Color Roles Overview
--------------------

All 26 Material Design 3 semantic color roles are defined on ``:root`` for light
mode and remapped under ``:root[data-theme="dark"]`` for dark mode, covering
accent roles, surface containers, outlines, inverse surfaces, and fixed accents.

**MD3 Specification Reference:**
`Styles > Color > Roles > What are color roles? <https://m3.material.io/styles/color/roles#e9fc5b00-8355-4641-b35f-58b0bac639f3>`_

.. _tonal-palettes:

Tonal Palettes
--------------

Six reference tonal palettes (``primary``, ``secondary``, ``tertiary``,
``neutral``, ``neutral-variant``, and ``error``) span 13 luminance tones from
``0`` (pure black) to ``100`` (pure white), providing the foundation for
guaranteed contrast ratios in both light and dark modes.

**MD3 Specification Reference:**
`Styles > Color > System > How the system works > 4. The algorithm creates tonal palettes <https://m3.material.io/styles/color/system/how-the-system-works#3ce9da92-a118-4692-8b2c-c5c52a413fa6>`_

.. _primary-color-roles:

Primary Color Roles
-------------------

The primary accent roles (``--md-sys-color-primary``, ``--md-sys-color-on-primary``,
``--md-sys-color-primary-container``, ``--md-sys-color-on-primary-container``)
drive high-emphasis actions including filled buttons, active tab indicators,
scrollspy indicators, focus rings, and inline hyperlinks.

**MD3 Specification Reference:**
`Styles > Color > Roles > Accent color roles > Primary <https://m3.material.io/styles/color/roles#41f55188-5c63-4107-ac41-822ebca8ae1b>`_

.. _secondary-color-roles:

Secondary Color Roles
---------------------

The secondary roles (``--md-sys-color-secondary``, ``--md-sys-color-on-secondary``,
``--md-sys-color-secondary-container``, ``--md-sys-color-on-secondary-container``)
style medium-emphasis components such as the active navigation drawer pill,
tonal buttons, and selected filter chips.

**MD3 Specification Reference:**
`Styles > Color > Roles > Accent color roles > Secondary <https://m3.material.io/styles/color/roles#290bcc49-b728-414c-8cc5-04336c1c799c>`_

.. _tertiary-color-roles:

Tertiary Color Roles
--------------------

The tertiary roles (``--md-sys-color-tertiary``, ``--md-sys-color-on-tertiary``,
``--md-sys-color-tertiary-container``, ``--md-sys-color-on-tertiary-container``)
provide complementary accents for constructive admonitions (``.. tip::``,
``.. important::``) and code copy confirmation badges.

**MD3 Specification Reference:**
`Styles > Color > Roles > Accent color roles > Tertiary <https://m3.material.io/styles/color/roles#727a0bf8-c95f-4f83-bc43-290d20f24e8e>`_

.. _error-color-roles:

Error Color Roles
-----------------

The error roles (``--md-sys-color-error``, ``--md-sys-color-on-error``,
``--md-sys-color-error-container``, ``--md-sys-color-on-error-container``)
communicate destructive states, warnings, and ``.. danger::`` / ``.. error::``
admonitions.

**MD3 Specification Reference:**
`Styles > Color > Roles > Error <https://m3.material.io/styles/color/roles#47a25970-8a80-43be-8307-c12e0f7a2b43>`_

.. _surface-roles:

Surface Roles
-------------

``--md-sys-color-surface``, ``--md-sys-color-on-surface``, and
``--md-sys-color-on-surface-variant`` define the default page background, primary
article text, and secondary metadata/navigation text.

**MD3 Specification Reference:**
`Styles > Color > Roles > Surface roles <https://m3.material.io/styles/color/roles#89f972b1-e372-494c-aabc-69aea34ed591>`_

.. _surface-container-roles:

Surface Container Roles
-----------------------

Tonal elevation uses the five hierarchical surface container tokens:

* ``--md-sys-color-surface-container-lowest``
* ``--md-sys-color-surface-container-low`` (elevated cards, admonitions, code blocks)
* ``--md-sys-color-surface-container`` (scrolled top app bar, sidebar filter input)
* ``--md-sys-color-surface-container-high`` (search bar, modal search dialog, table headers)
* ``--md-sys-color-surface-container-highest`` (filled cards, inline literal code)

**MD3 Specification Reference:**
`Styles > Color > Roles > Surface container roles <https://m3.material.io/styles/color/roles#1950f337-a1cb-4ebf-9d84-e0643d99c578>`_

.. _outline-roles:

Outline Roles
-------------

``--md-sys-color-outline`` provides ``3:1+`` high-contrast boundaries for
outlined buttons and focused inputs, while ``--md-sys-color-outline-variant``
provides subtle decorative borders for dividers, cards, tables, and structural
panes.

**MD3 Specification Reference:**
`Styles > Color > Roles > Outline <https://m3.material.io/styles/color/roles#e7d72e44-72e2-4ce9-a18d-df07b1433d18>`_

.. _inverse-roles:

Inverse Roles
-------------

``--md-sys-color-inverse-surface``, ``--md-sys-color-inverse-on-surface``, and
``--md-sys-color-inverse-primary`` support high-contrast floating notifications
and tooltips that contrast starkly with the surrounding page surface.

**MD3 Specification Reference:**
`Styles > Color > Roles > Inverse roles <https://m3.material.io/styles/color/roles#7fc6b47e-db22-4e98-8359-7649a099e4a1>`_

.. _fixed-accent-roles:

Fixed Accent Roles
------------------

``--md-sys-color-primary-fixed``, ``--md-sys-color-primary-fixed-dim``,
``--md-sys-color-on-primary-fixed``, and ``--md-sys-color-on-primary-fixed-variant``
(along with secondary and tertiary equivalents) maintain identical tones across
both light and dark themes.

**MD3 Specification Reference:**
`Styles > Color > Roles > Fixed accent roles <https://m3.material.io/styles/color/roles#26b6a882-064d-4668-b096-c51142477850>`_

.. _surface-bright-and-dim:

Surface Bright and Dim
----------------------

``--md-sys-color-surface-dim`` and ``--md-sys-color-surface-bright`` provide
explicit low- and high-luminance surface extremes across both light and dark
themes.

**MD3 Specification Reference:**
`Styles > Color > Roles > Surface dim & surface bright <https://m3.material.io/styles/color/roles#63d6db08-59e2-4341-ac33-9509eefd9b4f>`_

.. _wcag-contrast-ratios:

WCAG Contrast Ratios
--------------------

All foreground/background token pairings meet or exceed WCAG 2.1 AA contrast
thresholds: ``>= 4.5:1`` for body copy and interactive labels, and ``>= 3.0:1``
for large headlines and non-text UI boundaries.

**MD3 Specification Reference:**
`Foundations > Accessible design > Color & contrast > Contrast ratios <https://m3.material.io/foundations/designing/color-contrast#b248ecd2-9abd-4877-8f5e-ebfbb87e2048>`_

.. _accessible-tone-pairing:

Accessible Tone Pairing
-----------------------

By pairing tone ``40`` accents with tone ``100`` ``on-*`` text in light mode (a
60-tone delta) and tone ``80`` accents with tone ``20`` ``on-*`` text in dark
mode (also a 60-tone delta), the tonal palette system guarantees accessible
legibility across every component state.

**MD3 Specification Reference:**
`Styles > Color > System > How the system works > Pairing accessible tones <https://m3.material.io/styles/color/system/how-the-system-works#e1e92a3b-8702-46b6-8132-58321aa600bd>`_
