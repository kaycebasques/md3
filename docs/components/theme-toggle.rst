=========================
Theme Toggle
=========================

The ``<md3-theme-toggle>`` component controls light and dark color scheme
switching, persistent user preference storage, and syntax-highlighting
synchronization.

.. _theme-toggle-behavior:

Theme Toggle Behavior
---------------------

``<md3-theme-toggle>`` renders a compact icon button (``#theme-menu-btn``) in
the top app bar that toggles between ``light`` and ``dark`` color schemes on
click (and exposes a native ``#md3-theme-menu`` popover for ``:root.no-js``
environments):

* **State Synchronization**: ``applyTheme(theme)`` updates
  ``document.documentElement.dataset.theme``, persists the selection to
  ``localStorage.getItem('theme')``, updates ``aria-pressed`` on
  ``#theme-menu-btn``, and dispatches a custom ``md3-theme-change`` event.
* **Zero FOUC Initialization**: An inline bootstrap script in ``<head>`` reads
  ``localStorage`` and ``window.matchMedia('(prefers-color-scheme: dark)')``
  before first paint so pages never flash an unstyled color scheme.

**MD3 Specification Reference:**
`Styles > Color > System > How the system works > 5. The algorithm assigns tones to color roles <https://m3.material.io/styles/color/system/how-the-system-works#6e7242c4-8bea-4f96-b47a-c91a43181d18>`_

.. _dynamic-theme-remapping:

Dynamic Theme Remapping
-----------------------

Rather than duplicating component CSS rules for light and dark modes, every
component references semantic ``--md-sys-color-*`` tokens. Switching
``:root[data-theme="dark"]`` (or ``:root:not([data-theme="light"])`` under
``@media (prefers-color-scheme: dark)``) remaps the 26 semantic color roles to
their dark-mode tonal palette values in a single declaration block.

**MD3 Specification Reference:**
`Styles > Color > System > How the system works > 5. The algorithm assigns tones to color roles <https://m3.material.io/styles/color/system/how-the-system-works#99158cf0-6590-469c-a113-2c5625f40724>`_

.. _pygments-theme-sync:

Pygments Theme Sync
-------------------

Sphinx code blocks use ``pygments_style = "friendly"`` for light mode and
``pygments_dark_style = "native"`` (loaded via ``#pygments_dark_css``) for dark
mode. Whenever the theme changes, ``syncPygmentsTheme(theme)`` toggles the
``media`` attribute on ``#pygments_dark_css`` between ``"all"`` (dark) and
``"not all"`` (light) so code syntax highlighting stays synchronized with the
active MD3 surface palette.

**MD3 Specification Reference:**
`Styles > Color > System > How the system works > 5. The algorithm assigns tones to color roles <https://m3.material.io/styles/color/system/how-the-system-works#6e7242c4-8bea-4f96-b47a-c91a43181d18>`_
