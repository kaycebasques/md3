"""Material Design 3 (MD3) Specification Catalog and Conformance Test Utilities.

This module provides canonical deep links into both:
1. Our own component documentation pages (``components/<slug>.html#<section-id>``),
   which explain how each component conforms to the MD3 specification.
2. The official Material Design 3 documentation (https://m3.material.io/), with
   exact specification section names and requirement descriptions. Every URL in
   ``MD3_SPECS`` uses a verified ``sitemap.xml`` route and a real Carbon CMS
   ``#<pageContentBlockCanonId>`` section anchor on that page.
"""

from __future__ import annotations

import contextlib
import functools
from typing import Any, Callable, Dict, Optional

# ==============================================================================
# Canonical MD3 Specification Catalog (with component doc & m3.material.io links)
# ==============================================================================
MD3_SPECS: Dict[str, Dict[str, str]] = {
    # --------------------------------------------------------------------------
    # Design Tokens Architecture
    # --------------------------------------------------------------------------
    "DESIGN_TOKENS_OVERVIEW": {
        "url": "https://m3.material.io/foundations/design-tokens/overview#0aa7c44c-d528-4217-9aed-80d978815723",
        "section": "Foundations > Design Tokens > Overview > What’s a design token?",
        "doc_url": "components/color.html#design-tokens-overview",
        "doc_section": "Components > Color System & Tokens > Design Tokens Overview",
        "requirement": (
            "Design tokens are the smallest building blocks of the design system, "
            "organized into reference, system, and component token tiers."
        ),
    },
    "DESIGN_TOKENS_CLASSES": {
        "url": "https://m3.material.io/foundations/design-tokens/overview#c2c235dd-05db-4248-be47-48dfd8a21669",
        "section": "Foundations > Design Tokens > Overview > Classes of tokens",
        "doc_url": "components/color.html#token-classes",
        "doc_section": "Components > Color System & Tokens > Token Classes",
        "requirement": (
            "Reference tokens (--md-ref-*), system tokens (--md-sys-*), and component tokens "
            "(--md-comp-*) form a three-tier hierarchy where component tokens point to system tokens."
        ),
    },

    # --------------------------------------------------------------------------
    # Color System & Roles
    # --------------------------------------------------------------------------
    "COLOR_ROLES_OVERVIEW": {
        "url": "https://m3.material.io/styles/color/roles#e9fc5b00-8355-4641-b35f-58b0bac639f3",
        "section": "Styles > Color > Roles > What are color roles?",
        "doc_url": "components/color.html#color-roles-overview",
        "doc_section": "Components > Color System & Tokens > Color Roles Overview",
        "requirement": (
            "Color roles map UI elements to semantic color tokens across light and "
            "dark themes, establishing visual hierarchy and consistent brand identity."
        ),
    },
    "COLOR_PALETTE_TONES": {
        "url": "https://m3.material.io/styles/color/system/how-the-system-works#3ce9da92-a118-4692-8b2c-c5c52a413fa6",
        "section": "Styles > Color > System > How the system works > 4. The algorithm creates tonal palettes",
        "doc_url": "components/color.html#tonal-palettes",
        "doc_section": "Components > Color System & Tokens > Tonal Palettes",
        "requirement": (
            "Material 3 generates 13 reference tones (0, 10, 20, 30, 40, 50, 60, "
            "70, 80, 90, 95, 99, 100) for primary, secondary, tertiary, neutral, "
            "neutral-variant, and error tonal palettes."
        ),
    },
    "COLOR_PRIMARY": {
        "url": "https://m3.material.io/styles/color/roles#41f55188-5c63-4107-ac41-822ebca8ae1b",
        "section": "Styles > Color > Roles > Accent color roles > Primary",
        "doc_url": "components/color.html#primary-color-roles",
        "doc_section": "Components > Color System & Tokens > Primary Color Roles",
        "requirement": (
            "Primary color roles (primary, on-primary, primary-container, on-primary-container) "
            "are used for key UI components, filled buttons, active states, and prominent elements."
        ),
    },
    "COLOR_SECONDARY": {
        "url": "https://m3.material.io/styles/color/roles#290bcc49-b728-414c-8cc5-04336c1c799c",
        "section": "Styles > Color > Roles > Accent color roles > Secondary",
        "doc_url": "components/color.html#secondary-color-roles",
        "doc_section": "Components > Color System & Tokens > Secondary Color Roles",
        "requirement": (
            "Secondary color roles (secondary, on-secondary, secondary-container, "
            "on-secondary-container) are used for less prominent components, navigation pills, "
            "and filter chips."
        ),
    },
    "COLOR_TERTIARY": {
        "url": "https://m3.material.io/styles/color/roles#727a0bf8-c95f-4f83-bc43-290d20f24e8e",
        "section": "Styles > Color > Roles > Accent color roles > Tertiary",
        "doc_url": "components/color.html#tertiary-color-roles",
        "doc_section": "Components > Color System & Tokens > Tertiary Color Roles",
        "requirement": (
            "Tertiary color roles (tertiary, on-tertiary, tertiary-container, "
            "on-tertiary-container) provide contrasting accents to balance primary and secondary "
            "colors, used for tip callouts and editorial highlights."
        ),
    },
    "COLOR_ERROR": {
        "url": "https://m3.material.io/styles/color/roles#47a25970-8a80-43be-8307-c12e0f7a2b43",
        "section": "Styles > Color > Roles > Error",
        "doc_url": "components/color.html#error-color-roles",
        "doc_section": "Components > Color System & Tokens > Error Color Roles",
        "requirement": (
            "Error color roles (error, on-error, error-container, on-error-container) "
            "indicate errors, alerts, danger callouts, and destructive actions."
        ),
    },
    "COLOR_SURFACE": {
        "url": "https://m3.material.io/styles/color/roles#89f972b1-e372-494c-aabc-69aea34ed591",
        "section": "Styles > Color > Roles > Surface roles",
        "doc_url": "components/color.html#surface-roles",
        "doc_section": "Components > Color System & Tokens > Surface Roles",
        "requirement": (
            "Surface roles (surface, on-surface, surface-variant, on-surface-variant) "
            "provide base background coloring behind content and text typography."
        ),
    },
    "COLOR_SURFACE_CONTAINERS": {
        "url": "https://m3.material.io/styles/color/roles#1950f337-a1cb-4ebf-9d84-e0643d99c578",
        "section": "Styles > Color > Roles > Surface container roles",
        "doc_url": "components/color.html#surface-container-roles",
        "doc_section": "Components > Color System & Tokens > Surface Container Roles",
        "requirement": (
            "Five surface container roles (lowest, low, container, high, highest) create visual "
            "hierarchy, nested containers, and depth separation without elevation shadows."
        ),
    },
    "COLOR_OUTLINE": {
        "url": "https://m3.material.io/styles/color/roles#e7d72e44-72e2-4ce9-a18d-df07b1433d18",
        "section": "Styles > Color > Roles > Outline",
        "doc_url": "components/color.html#outline-roles",
        "doc_section": "Components > Color System & Tokens > Outline Roles",
        "requirement": (
            "Outline (3:1 contrast) and outline-variant roles define component boundaries "
            "for outlined buttons, outlined cards, search inputs, and subtle dividers."
        ),
    },
    "COLOR_INVERSE": {
        "url": "https://m3.material.io/styles/color/roles#7fc6b47e-db22-4e98-8359-7649a099e4a1",
        "section": "Styles > Color > Roles > Inverse roles",
        "doc_url": "components/color.html#inverse-roles",
        "doc_section": "Components > Color System & Tokens > Inverse Roles",
        "requirement": (
            "Inverse surface, inverse on-surface, and inverse primary provide reverse contrast "
            "for floating snackbars, tooltips, and high-emphasis contrast elements."
        ),
    },
    "COLOR_FIXED_ACCENTS": {
        "url": "https://m3.material.io/styles/color/roles#26b6a882-064d-4668-b096-c51142477850",
        "section": "Styles > Color > Roles > Fixed accent roles",
        "doc_url": "components/color.html#fixed-accent-roles",
        "doc_section": "Components > Color System & Tokens > Fixed Accent Roles",
        "requirement": (
            "Fixed accent roles (primary-fixed, secondary-fixed, tertiary-fixed, and dim/on-fixed "
            "variants) maintain identical tone and contrast across light and dark modes."
        ),
    },
    "COLOR_BRIGHT_DIM": {
        "url": "https://m3.material.io/styles/color/roles#63d6db08-59e2-4341-ac33-9509eefd9b4f",
        "section": "Styles > Color > Roles > Surface dim & surface bright",
        "doc_url": "components/color.html#surface-bright-and-dim",
        "doc_section": "Components > Color System & Tokens > Surface Bright and Dim",
        "requirement": (
            "Surface bright and surface dim roles supply dynamic contrast boundaries across "
            "light and dark themes."
        ),
    },
    "COLOR_CONTRAST_WCAG": {
        "url": "https://m3.material.io/foundations/designing/color-contrast#b248ecd2-9abd-4877-8f5e-ebfbb87e2048",
        "section": "Foundations > Accessible design > Color & contrast > Contrast ratios",
        "doc_url": "components/color.html#wcag-contrast-ratios",
        "doc_section": "Components > Color System & Tokens > WCAG Contrast Ratios",
        "requirement": (
            "Material Design 3 requires body text and on-color foreground tokens to achieve "
            "at least 4.5:1 contrast against their corresponding container/surface (WCAG 2.1 AA), "
            "and large text/boundaries at least 3.0:1."
        ),
    },
    "COLOR_ACCESSIBLE_PAIRING": {
        "url": "https://m3.material.io/styles/color/system/how-the-system-works#e1e92a3b-8702-46b6-8132-58321aa600bd",
        "section": "Styles > Color > System > How the system works > Pairing accessible tones",
        "doc_url": "components/color.html#accessible-tone-pairing",
        "doc_section": "Components > Color System & Tokens > Accessible Tone Pairing",
        "requirement": (
            "Foreground text roles must be algorithmically paired with background surfaces to "
            "guarantee legible contrast in both light and dark themes."
        ),
    },
    "COLOR_THEME_SWITCHING": {
        "url": "https://m3.material.io/styles/color/system/how-the-system-works#99158cf0-6590-469c-a113-2c5625f40724",
        "section": "Styles > Color > System > How the system works > 5. The algorithm assigns tones to color roles",
        "doc_url": "components/theme-toggle.html#dynamic-theme-remapping",
        "doc_section": "Components > Theme Toggle > Dynamic Theme Remapping",
        "requirement": (
            "Theme switching dynamically remaps system color tokens between light and dark "
            "palettes while maintaining semantic role relationships."
        ),
    },

    # --------------------------------------------------------------------------
    # Typography
    # --------------------------------------------------------------------------
    "TYPOGRAPHY_TYPESCALE_TOKENS": {
        "url": "https://m3.material.io/styles/typography/type-scale-tokens#84c60429-0cca-4792-b3d2-2305e22429ba",
        "section": "Styles > Typography > Type scale tokens > Baseline type style tokens",
        "doc_url": "components/typography.html#typescale-tokens",
        "doc_section": "Components > Typography > Typescale Tokens",
        "requirement": (
            "The 15 typescale tokens (Display, Headline, Title, Body, Label in large, "
            "medium, small) define exact font-size, line-height, font-weight, and tracking values."
        ),
    },
    "TYPOGRAPHY_APPLYING_TYPE": {
        "url": "https://m3.material.io/styles/typography/applying-type#ab657e7c-cb93-45ff-92c6-686959dc19ae",
        "section": "Styles > Typography > Applying type > Roles",
        "doc_url": "components/typography.html#applying-type-roles",
        "doc_section": "Components > Typography > Applying Type Roles",
        "requirement": (
            "Documentation headings h1 through h6 map onto Headline and Title typescales; "
            "body text maps to Body Large (16px) or Body Medium (14px)."
        ),
    },
    "TYPOGRAPHY_HYPERLINKS": {
        "url": "https://m3.material.io/styles/typography/applying-type#24856f70-f759-45df-a06c-92018f286083",
        "section": "Styles > Typography > Applying type > Color & contrast > Hyperlinked text",
        "doc_url": "components/typography.html#inline-hyperlinks",
        "doc_section": "Components > Typography > Inline Hyperlinks",
        "requirement": (
            "Hyperlinked text appearing on top of a surface color must use the primary color "
            "role and must also be underlined so links are distinguishable without color alone."
        ),
    },
    "TYPOGRAPHY_TABULAR_NUMERALS": {
        "url": "https://m3.material.io/styles/typography/applying-type#f0f79df7-3174-4012-871e-93ce9a89d08b",
        "section": "Styles > Typography > Applying type > Typesetting > Tabular numerals",
        "doc_url": "components/tables.html#tabular-numerals",
        "doc_section": "Components > Data Tables > Tabular Numerals",
        "requirement": (
            "Data tables must use tabular figures (font-variant-numeric: tabular-nums) rather "
            "than proportional digits so numerical columns align vertically."
        ),
    },
    "TYPOGRAPHY_FONTS": {
        "url": "https://m3.material.io/styles/typography/fonts#dbd29949-f164-4065-bb36-49a765fbfe3d",
        "section": "Styles > Typography > Fonts > Default typefaces",
        "doc_url": "components/typography.html#default-typefaces",
        "doc_section": "Components > Typography > Default Typefaces",
        "requirement": (
            "Typography specifies brand and plain sans-serif typefaces (--md-ref-typeface-brand, "
            "--md-ref-typeface-plain) and monospaced typeface (--md-ref-typeface-code) for code."
        ),
    },

    # --------------------------------------------------------------------------
    # Shapes
    # --------------------------------------------------------------------------
    "SHAPE_CORNER_RADIUS_SCALE": {
        "url": "https://m3.material.io/styles/shape/corner-radius-scale#7c4b83c5-25e3-4337-889d-4f24a2b93e6d",
        "section": "Styles > Shape > Corner radius scale > Corner radius scale",
        "doc_url": "components/cards.html#corner-radius-scale",
        "doc_section": "Components > Cards, Shape, Elevation & Motion > Corner Radius Scale",
        "requirement": (
            "The 10-value shape corner radius scale defines None (0px), Extra Small (4px), "
            "Small (8px), Medium (12px), Large (16px), Large Increased (20px), Extra Large (28px), "
            "Extra Large Increased (32px), Extra Extra Large (48px), and Full (9999px)."
        ),
    },
    "SHAPE_TOKENS": {
        "url": "https://m3.material.io/styles/shape/corner-radius-scale#9a2814ed-bd01-43c8-a1bc-29d486ee7f35",
        "section": "Styles > Shape > Corner radius scale > Shape tokens",
        "doc_url": "components/cards.html#semantic-shape-tokens",
        "doc_section": "Components > Cards, Shape, Elevation & Motion > Semantic Shape Tokens",
        "requirement": (
            "Components map to semantic shape tokens: round buttons use full pill (9999px), "
            "square buttons and cards use medium (12px), chips use small (8px), dialogs use extra-large (28px)."
        ),
    },
    "SHAPE_MORPH_INTERACTION": {
        "url": "https://m3.material.io/styles/shape/shape-morph#7a4c6627-3452-4619-b4d1-93058c0b7685",
        "section": "Styles > Shape > Shape morph > Using shape morph",
        "doc_url": "components/buttons.html#pressed-shape-morph",
        "doc_section": "Components > Buttons > Pressed Shape Morph",
        "requirement": (
            "Interactive buttons and icon buttons morph their corner radius to small (8px) "
            "in the pressed (:active) state to provide expressive tactile feedback."
        ),
    },

    # --------------------------------------------------------------------------
    # Elevation & Shadows
    # --------------------------------------------------------------------------
    "ELEVATION_LEVELS": {
        "url": "https://m3.material.io/styles/elevation/overview#6585e78e-773c-46d2-b7e6-2eea780f7eb5",
        "section": "Styles > Elevation > Overview > All surfaces and components have elevation values",
        "doc_url": "components/cards.html#elevation-levels",
        "doc_section": "Components > Cards, Shape, Elevation & Motion > Elevation Levels",
        "requirement": (
            "Elevation represents depth along the z-axis using 6 discrete levels: Level 0 (0dp), "
            "Level 1 (1dp), Level 2 (3dp), Level 3 (6dp), Level 4 (8dp), and Level 5 (12dp)."
        ),
    },
    "ELEVATION_TOKENS": {
        "url": "https://m3.material.io/styles/elevation/tokens#cdec0b55-abbe-46f8-a3aa-07f0ea3b76da",
        "section": "Styles > Elevation > Tokens > Tokens",
        "doc_url": "components/cards.html#elevation-tokens",
        "doc_section": "Components > Cards, Shape, Elevation & Motion > Elevation Tokens",
        "requirement": (
            "Elevation tokens (--md-sys-elevation-level0 through level5) define exact dp heights "
            "and dual ambient/key shadow layers."
        ),
    },
    "ELEVATION_COMPONENT_RESTING": {
        "url": "https://m3.material.io/styles/elevation/tokens#df721a00-888e-4c5e-bfe1-5d905f167aaa",
        "section": "Styles > Elevation > Tokens > Component elevation",
        "doc_url": "components/cards.html#component-resting-elevation",
        "doc_section": "Components > Cards, Shape, Elevation & Motion > Component Resting Elevation",
        "requirement": (
            "Default component elevations follow the MD3 table: Top app bar resting Level 0 "
            "and scrolled Level 2; Elevated card & button Level 1; Dialogs & Modal search Level 3."
        ),
    },
    "ELEVATION_SCRIM": {
        "url": "https://m3.material.io/styles/elevation/applying-elevation#92b9fb39-f0c4-4829-8e4d-97ac512976aa",
        "section": "Styles > Elevation > Applying elevation > Scrims",
        "doc_url": "components/cards.html#scrim-overlays",
        "doc_section": "Components > Cards, Shape, Elevation & Motion > Scrim Overlays",
        "requirement": (
            "Modal dialogs and modal navigation drawers use a scrim overlay with --md-sys-color-scrim "
            "at 32% opacity (0.32) to obscure background content."
        ),
    },

    # --------------------------------------------------------------------------
    # Motion
    # --------------------------------------------------------------------------
    "MOTION_EASING_DURATION": {
        "url": "https://m3.material.io/styles/motion/easing-and-duration/applying-easing-and-duration#6409707e-1253-449c-b588-d27fe53bd025",
        "section": "Styles > Motion > Easing and duration > Applying easing and duration > Suggested easing and duration pairs",
        "doc_url": "components/cards.html#motion-easing-and-duration",
        "doc_section": "Components > Cards, Shape, Elevation & Motion > Motion Easing and Duration",
        "requirement": (
            "Transitions use MD3 standard and emphasized easing curves paired with duration "
            "tokens (short1: 50ms through extra-long4: 1000ms)."
        ),
    },
    "MOTION_SPECS": {
        "url": "https://m3.material.io/styles/motion/easing-and-duration/tokens-specs#2c0659e2-a2c8-4d7b-8964-5b8dce012f7c",
        "section": "Styles > Motion > Easing and duration > Tokens & specs > Tokens",
        "doc_url": "components/cards.html#motion-tokens",
        "doc_section": "Components > Cards, Shape, Elevation & Motion > Motion Tokens",
        "requirement": (
            "Standard easing (cubic-bezier(0.2, 0, 0, 1)) governs utility transitions; "
            "emphasized easing (decelerate cubic-bezier(0.05, 0.7, 0.1, 1), accelerate "
            "cubic-bezier(0.3, 0, 0.8, 0.15)) governs modal dialogs and drawers."
        ),
    },

    # --------------------------------------------------------------------------
    # Spacing Tokens
    # --------------------------------------------------------------------------
    "SPACING_SYSTEM_TOKENS": {
        "url": "https://m3.material.io/styles/spacing/tokens#a744956e-be8e-4b97-8a30-b2170e6944a8",
        "section": "Styles > Spacing > Tokens > System spacing tokens",
        "doc_url": "components/app.html#spacing-system-tokens",
        "doc_section": "Components > App Scaffold & Layout > Spacing System Tokens",
        "requirement": (
            "The 18 official MD3 system measurement spacing tokens (--md-sys-measurement-space0 "
            "through space900) define the 4dp/8dp spatial grid and nested units (0px to 72px)."
        ),
    },

    # --------------------------------------------------------------------------
    # States & State Layers
    # --------------------------------------------------------------------------
    "STATE_LAYERS": {
        "url": "https://m3.material.io/foundations/interaction/states/state-layers#bf9b84b2-690c-44b2-8429-8c42dc012d43",
        "section": "Foundations > Interaction > States > State layers > State layer tokens & values",
        "doc_url": "components/buttons.html#state-layer-tokens",
        "doc_section": "Components > Buttons > State Layer Tokens",
        "requirement": (
            "State layers apply a semi-transparent overlay to communicate interaction states: "
            "hover (8%), focus (10%), pressed (10%), dragged (16%), and disabled content (38%)."
        ),
    },
    "STATE_APPLYING": {
        "url": "https://m3.material.io/foundations/interaction/states/applying-states#bc6d6853-48ef-490e-8076-448e89e69f0f",
        "section": "Foundations > Interaction > States > Applying states > Focused",
        "doc_url": "components/buttons.html#interaction-states",
        "doc_section": "Components > Buttons > Interaction States",
        "requirement": (
            "Interactive components must provide visible state transitions on hover, focus, "
            "press, and disabled states to confirm user input."
        ),
    },

    # --------------------------------------------------------------------------
    # Information Density & Compact Sizing
    # --------------------------------------------------------------------------
    "DENSITY_BUTTONS": {
        "url": "https://m3.material.io/components/buttons/specs#73044a63-dc51-4401-bd4d-318920738ab3",
        "section": "Components > Buttons > Specs > Measurements & Corner sizes",
        "doc_url": "components/buttons.html#compact-button-sizing",
        "doc_section": "Components > Buttons > Compact Button Sizing",
        "requirement": (
            "High-density documentation layouts utilize MD3 Extra Small (32px container height) "
            "buttons with 12px horizontal padding, 8px icon-label gap, and full pill or 12px square corners."
        ),
    },
    "DENSITY_NAV_DRAWER": {
        "url": "https://m3.material.io/components/navigation-drawer/specs#73da5c32-aecf-4c88-849b-77310fbc3b77",
        "section": "Components > Navigation Drawer > Specs > Measurements",
        "doc_url": "components/sidebar.html#compact-navigation-items",
        "doc_section": "Components > Navigation Drawer (Sidebar) > Compact Navigation Items",
        "requirement": (
            "Compact navigation items use a 32px height active indicator pill (full corner shape) "
            "to maintain high vertical information density in documentation sidebars."
        ),
    },
    "DENSITY_SEARCH": {
        "url": "https://m3.material.io/components/search/specs#6910a69a-1c33-42d1-83c5-3da9982e59e3",
        "section": "Components > Search > Specs > Measurements > Search bar",
        "doc_url": "components/search.html#compact-search-bar",
        "doc_section": "Components > Search Bar & Dialog > Compact Search Bar",
        "requirement": (
            "Compact search bar container has 36px height with full pill corner radius (9999px) "
            "and surface-container-high background for dense top app bar headers."
        ),
    },
    "DENSITY_CHIPS": {
        "url": "https://m3.material.io/components/chips/specs#9faeb601-c522-4a5a-a263-f1b1ac7504d6",
        "section": "Components > Chips > Specs > Assist chip measurements",
        "doc_url": "components/chips.html#assist-and-filter-chips",
        "doc_section": "Components > Chips > Assist and Filter Chips",
        "requirement": (
            "Assist and Filter chips have a 32px container height, 8px (corner-small) radius, "
            "18px icon size, and Label Large typography."
        ),
    },
    "DENSITY_ICON_BUTTONS": {
        "url": "https://m3.material.io/components/icon-buttons/specs#c2d79537-2f48-4fa3-8241-27a5a46a6ecb",
        "section": "Components > Icon Buttons > Specs > Measurements",
        "doc_url": "components/icon-buttons.html#compact-icon-buttons",
        "doc_section": "Components > Icon Buttons > Compact Icon Buttons",
        "requirement": (
            "Extra Small (XSmall) icon buttons use a 32px container height/width with a 20px icon "
            "and full circular corner radius."
        ),
    },
    "DENSITY_TABLES": {
        "url": "https://m3.material.io/foundations/layout/grids-spacing/density#7bd57971-f3eb-4050-a57e-be5698d048bc",
        "section": "Foundations > Layout > Grids & spacing > Density > Information density",
        "doc_url": "components/tables.html#compact-table-density",
        "doc_section": "Components > Data Tables > Compact Table Density",
        "requirement": (
            "High-density data tables reduce vertical cell padding to 8px to display more rows "
            "per viewport on desktop screens."
        ),
    },
    "DENSITY_SCALE": {
        "url": "https://m3.material.io/foundations/layout/grids-spacing/density#7b845d8f-aaf6-4503-ad00-760f9f988388",
        "section": "Foundations > Layout > Grids & spacing > Density > Component scaling",
        "doc_url": "components/app.html#compact-density-scale",
        "doc_section": "Components > App Scaffold & Layout > Compact Density Scale",
        "requirement": (
            "The theme implements compact density scale (--md-density-scale: -2) to "
            "consistently compress component heights across desktop documentation UI elements."
        ),
    },

    # --------------------------------------------------------------------------
    # Layout, Scaffold, Panes & Window Size Classes (Breakpoints)
    # --------------------------------------------------------------------------
    "LAYOUT_SCAFFOLD": {
        "url": "https://m3.material.io/foundations/layout/scaffold/panes#deed6085-479f-4a94-b266-c7b079d19500",
        "section": "Foundations > Layout > Scaffold > Panes > Three-pane layouts",
        "doc_url": "components/app.html#three-pane-scaffold",
        "doc_section": "Components > App Scaffold & Layout > Three Pane Scaffold",
        "requirement": (
            "Desktop documentation layout on Large/Extra-Large screens (>=1200px) organizes content "
            "into 3 panes: Left Navigation Drawer (260px), Center Main Content (max 820px), and "
            "Right On-Page Table of Contents (240px)."
        ),
    },
    "LAYOUT_TWO_PANE_EXPANDED": {
        "url": "https://m3.material.io/foundations/layout/breakpoints/expanded#9f3c44f0-b91e-4618-b93a-6fb34239d246",
        "section": "Foundations > Layout > Breakpoints > Expanded > Panes",
        "doc_url": "components/app.html#two-pane-expanded-layout",
        "doc_section": "Components > App Scaffold & Layout > Two Pane Expanded Layout",
        "requirement": (
            "In the Expanded window size class (840px–1199px), layout displays 2 panes "
            "(persistent navigation drawer + main content) and hides the 3rd supporting TOC pane."
        ),
    },
    "LAYOUT_BREAKPOINTS": {
        "url": "https://m3.material.io/foundations/layout/breakpoints/overview#395b70d6-973e-4d07-a40b-3be8d4e150d5",
        "section": "Foundations > Layout > Breakpoints > Overview > Breakpoints overview",
        "doc_url": "components/app.html#window-size-breakpoints",
        "doc_section": "Components > App Scaffold & Layout > Window Size Breakpoints",
        "requirement": (
            "Layout adapts across official MD3 window size classes: Compact (<600px) & Medium "
            "(600px–839px) single pane with modal drawer, Expanded (840px–1199px) 2-pane, and "
            "Large/Extra-Large (>=1200px) 3-pane."
        ),
    },
    "LAYOUT_MODAL_DRAWER": {
        "url": "https://m3.material.io/components/navigation-drawer/specs#368147de-9661-4a28-9fc1-ce2f8c9eac40",
        "section": "Components > Navigation Drawer > Specs > Modal navigation drawer",
        "doc_url": "components/sidebar.html#modal-navigation-drawer",
        "doc_section": "Components > Navigation Drawer (Sidebar) > Modal Navigation Drawer",
        "requirement": (
            "On Compact and Medium viewports (<840px), navigation collapses into a sliding modal "
            "drawer with a 16px trailing corner radius, Level 3 elevation, and a 32% scrim backdrop."
        ),
    },
    "LAYOUT_DRAWER_DISMISS": {
        "url": "https://m3.material.io/components/navigation-drawer/guidelines#046936be-3330-492b-94d3-5a8cb41b17e9",
        "section": "Components > Navigation Drawer > Guidelines > Behavior > Visibility",
        "doc_url": "components/sidebar.html#drawer-dismissal",
        "doc_section": "Components > Navigation Drawer (Sidebar) > Drawer Dismissal",
        "requirement": (
            "Modal navigation drawer must be dismissible by clicking the scrim backdrop or "
            "pressing Escape, and must return focus to the drawer toggle button upon closing."
        ),
    },

    # --------------------------------------------------------------------------
    # Components & Web Components Runtime
    # --------------------------------------------------------------------------
    "COMPONENTS_CUSTOM_ELEMENTS": {
        "url": "https://m3.material.io/foundations/overview/principles#25cda2a6-e748-4efc-be27-8be7b1966fc5",
        "section": "Foundations > Accessible design > Overview > Principles",
        "doc_url": "components/app.html#custom-elements-registry",
        "doc_section": "Components > App Scaffold & Layout > Custom Elements Registry",
        "requirement": (
            "Theme components must be implemented as standards-compliant Web Components "
            "(Custom Elements) defined in the browser customElements registry."
        ),
    },
    "COMPONENTS_TOP_APP_BAR": {
        "url": "https://m3.material.io/components/app-bars/specs#fac99130-8bb8-498c-8cb8-16ea056cc3e1",
        "section": "Components > App bars > Specs > Measurements > Small app bar",
        "doc_url": "components/top-app-bar.html#small-top-app-bar",
        "doc_section": "Components > Top App Bar > Small Top App Bar",
        "requirement": (
            "Small top app bar has a 56px container height, displaying leading navigation icon, "
            "headline brand title, quick search bar, and trailing utility icon buttons."
        ),
    },
    "COMPONENTS_TOP_APP_BAR_SCROLL": {
        "url": "https://m3.material.io/components/app-bars/specs#9975d8e5-f69e-48bd-865e-af3c8eeba1d3",
        "section": "Components > App bars > Specs > Color > Scroll states",
        "doc_url": "components/top-app-bar.html#scroll-states",
        "doc_section": "Components > Top App Bar > Scroll States",
        "requirement": (
            "At rest, the top app bar uses surface container color and Level 0 elevation; "
            "on scroll (.scrolled), it transitions to surface-container color and Level 2 elevation."
        ),
    },
    "COMPONENTS_NAV_PROGRESSIVE_DISCLOSURE": {
        "url": "https://m3.material.io/components/navigation-drawer/guidelines#761e9679-2e72-4a85-894d-55bc3666b567",
        "section": "Components > Navigation Drawer > Guidelines > Usage",
        "doc_url": "components/sidebar.html#progressive-disclosure",
        "doc_section": "Components > Navigation Drawer (Sidebar) > Progressive Disclosure",
        "requirement": (
            "Navigation drawer uses progressive disclosure to show one hierarchy level at a time "
            "with ancestor drill-up links, child chevron indicators, and instant filtering on large sections."
        ),
    },
    "COMPONENTS_NAV_TABS": {
        "url": "https://m3.material.io/components/tabs/specs#8602158e-a13b-432e-8133-b9cb34d61678",
        "section": "Components > Tabs > Specs > Primary tabs",
        "doc_url": "components/nav-tabs.html#primary-navigation-tabs",
        "doc_section": "Components > Navigation Tabs > Primary Navigation Tabs",
        "requirement": (
            "Primary navigation tabs (<md3-nav-tabs>) display top-level site sections below the header "
            "with a 3px primary active indicator pill and compact 40px height."
        ),
    },
    "COMPONENTS_NAV_TABS_KEYBOARD": {
        "url": "https://m3.material.io/components/tabs/accessibility#a1ebaebd-1bb4-4401-9962-8b30a563e49e",
        "section": "Components > Tabs > Accessibility > Keyboard navigation",
        "doc_url": "components/nav-tabs.html#tab-keyboard-navigation",
        "doc_section": "Components > Navigation Tabs > Tab Keyboard Navigation",
        "requirement": (
            "Primary navigation tabs support ArrowRight, ArrowLeft, Home, and End keyboard traversal "
            "across top-level section links."
        ),
    },
    "COMPONENTS_BUTTON_VARIANTS": {
        "url": "https://m3.material.io/components/buttons/guidelines#4e89da4d-a8fa-4e20-bb8d-b8a93eff3e3e",
        "section": "Components > Buttons > Guidelines > Color styles",
        "doc_url": "components/buttons.html#button-color-variants",
        "doc_section": "Components > Buttons > Button Color Variants",
        "requirement": (
            "Buttons support all 5 official MD3 color variants (Filled, Tonal, Elevated, Outlined, "
            "and Text), each with distinct container, label, and outline tokens and no text underline."
        ),
    },
    "COMPONENTS_ICON_BUTTON_TOOLTIP": {
        "url": "https://m3.material.io/components/icon-buttons/accessibility#a5b945ae-d453-424b-ae70-e008a5ebfdd1",
        "section": "Components > Icon buttons > Accessibility > Labeling elements",
        "doc_url": "components/icon-buttons.html#icon-button-tooltips",
        "doc_section": "Components > Icon Buttons > Icon Button Tooltips",
        "requirement": (
            "On web, icon buttons must provide both an accessibility label (aria-label) and "
            "a tooltip (title attribute) describing the button's action."
        ),
    },
    "COMPONENTS_CARDS": {
        "url": "https://m3.material.io/components/cards/specs#038b4a49-3a7f-4fce-be8c-89c1155b4c82",
        "section": "Components > Cards > Specs > Measurements",
        "doc_url": "components/cards.html#card-variants",
        "doc_section": "Components > Cards, Shape, Elevation & Motion > Card Variants",
        "requirement": (
            "Cards support Outlined (surface + 1px outline-variant), Filled (surface-container-highest), "
            "and Elevated (surface-container-low + Level 1 elevation) variants with 12px medium corners."
        ),
    },
    "COMPONENTS_DIVIDER": {
        "url": "https://m3.material.io/components/divider/specs#3ac2a512-7e92-4d92-b729-a1e83536c2c2",
        "section": "Components > Divider > Specs > Tokens and specs",
        "doc_url": "components/dividers.html#divider-tokens-and-specs",
        "doc_section": "Components > Dividers > Divider Tokens and Specs",
        "requirement": (
            "Dividers (hr, .md3-divider) use a 1px thickness (--md-comp-divider-thickness) "
            "and the outline-variant color token (--md-comp-divider-color)."
        ),
    },
    "COMPONENTS_LISTS": {
        "url": "https://m3.material.io/components/lists/specs#eeeb78e0-265d-4e81-96ba-c2340c348a90",
        "section": "Components > Lists > Specs > One-line lists",
        "doc_url": "components/sidebar.html#navigation-list-items",
        "doc_section": "Components > Navigation Drawer (Sidebar) > Navigation List Items",
        "requirement": (
            "Navigation and content list items use --md-comp-list-list-item-* tokens for "
            "container height, leading/trailing padding, and on-surface label color."
        ),
    },
    "COMPONENTS_SEARCH_DIALOG": {
        "url": "https://m3.material.io/components/dialogs/specs#9a8c226b-19fa-4d6b-894e-e7d5ca9203e8",
        "section": "Components > Dialogs > Specs > Basic dialog measurements",
        "doc_url": "components/search.html#modal-search-dialog",
        "doc_section": "Components > Search Bar & Dialog > Modal Search Dialog",
        "requirement": (
            "Modal search dialog uses extra-large (28px) corner radius, surface-container-high "
            "background, Level 3 elevation, min-width 280px, max-width 560px, and 32% scrim backdrop."
        ),
    },
    "COMPONENTS_DIALOG_FOCUS_RETURN": {
        "url": "https://m3.material.io/components/dialogs/accessibility#77f7ff34-ea07-4036-a45a-fc94428f43f6",
        "section": "Components > Dialogs > Accessibility > Keyboard navigation",
        "doc_url": "components/search.html#dialog-focus-return",
        "doc_section": "Components > Search Bar & Dialog > Dialog Focus Return",
        "requirement": (
            "Opening a modal dialog moves focus inside the dialog; dismissing it via Escape, "
            "Close button, or backdrop click returns focus to the trigger element."
        ),
    },
    "COMPONENTS_CODE_COPY": {
        "url": "https://m3.material.io/components/buttons/specs#c305d304-a6c0-466a-a48c-8d0718a29ae2",
        "section": "Components > Buttons > Specs > Baseline tokens",
        "doc_url": "components/copy-button.html#code-copy-interaction",
        "doc_section": "Components > Code Copy Button > Code Copy Interaction",
        "requirement": (
            "Code copy button copies content to clipboard, exposes button semantics and tooltip, "
            "and provides transient visual confirmation feedback."
        ),
    },
    "COMPONENTS_TOC_SCROLLSPY": {
        "url": "https://m3.material.io/foundations/layout/scaffold/panes#91f7daf8-1aab-4603-8865-013b6b5f5257",
        "section": "Foundations > Layout > Scaffold > Panes > Panes",
        "doc_url": "components/toc.html#scrollspy-navigation",
        "doc_section": "Components > Table of Contents (TOC) > Scrollspy Navigation",
        "requirement": (
            "On-page table of contents supporting pane tracks scrolling position and highlights "
            "the active section heading link."
        ),
    },

    # --------------------------------------------------------------------------
    # Sphinx Elements & Documentation Styling
    # --------------------------------------------------------------------------
    "SPHINX_ADMONITIONS": {
        "url": "https://m3.material.io/components/cards/specs#9ad208b3-3d37-475c-a0eb-68cf845718f8",
        "section": "Components > Cards > Specs > Outlined card",
        "doc_url": "components/admonitions.html#callout-containers",
        "doc_section": "Components > Admonitions > Callout Containers",
        "requirement": (
            "Sphinx callouts (note, tip, warning, danger) use MD3 surface container colors, "
            "12px medium card corner radii, and semantic primary/tertiary/secondary/error accents."
        ),
    },
    "SPHINX_PYGMENTS": {
        "url": "https://m3.material.io/styles/color/system/how-the-system-works#6e7242c4-8bea-4f96-b47a-c91a43181d18",
        "section": "Styles > Color > System > How the system works > 5. The algorithm assigns tones to color roles",
        "doc_url": "components/theme-toggle.html#pygments-theme-sync",
        "doc_section": "Components > Theme Toggle > Pygments Theme Sync",
        "requirement": (
            "Pygments syntax highlighting stylesheets for light and dark themes must both be loaded "
            "in <head> and synchronized dynamically when the theme changes."
        ),
    },
    "SPHINX_PAGINATION": {
        "url": "https://m3.material.io/components/cards/specs#9776d7d8-c583-4824-bb77-39cef535548d",
        "section": "Components > Cards > Specs > Outlined card color",
        "doc_url": "components/cards.html#pagination-cards",
        "doc_section": "Components > Cards, Shape, Elevation & Motion > Pagination Cards",
        "requirement": (
            "Previous / next page navigation cards render as interactive MD3 outlined cards with "
            "12px corners, 1px outline-variant border, and hover Level 1 elevation."
        ),
    },
    "SPHINX_BREADCRUMBS": {
        "url": "https://m3.material.io/foundations/designing/structure#b892ce17-68d6-4873-91f1-3c481359effd",
        "section": "Foundations > Accessible design > Structure > Hierarchy > Navigation",
        "doc_url": "components/breadcrumbs.html#breadcrumb-hierarchy",
        "doc_section": "Components > Breadcrumbs > Breadcrumb Hierarchy",
        "requirement": (
            "Breadcrumbs indicate page hierarchy with an aria-label='Breadcrumb' landmark, "
            "aria-current='page' on the active item, and aria-hidden separators."
        ),
    },

    # --------------------------------------------------------------------------
    # Accessibility & Interaction
    # --------------------------------------------------------------------------
    "ACCESSIBILITY_FOCUS_RING": {
        "url": "https://m3.material.io/foundations/interaction/states/applying-states#9edb181a-ed5e-4961-b3d0-cae33125a4a9",
        "section": "Foundations > Interaction > States > Applying states > Keyboard focus indicator",
        "doc_url": "components/buttons.html#keyboard-focus-ring",
        "doc_section": "Components > Buttons > Keyboard Focus Ring",
        "requirement": (
            "Interactive controls must display a high-contrast focus indicator "
            "(outline: 3px solid var(--md-sys-color-secondary), outline-offset: 2px) on :focus-visible."
        ),
    },
    "ACCESSIBILITY_ARIA_SEMANTICS": {
        "url": "https://m3.material.io/foundations/designing/elements#db9a0efd-8045-4c5f-8a4d-c80f9fb08c68",
        "section": "Foundations > Accessible design > Elements > Labeling elements",
        "doc_url": "components/icon-buttons.html#aria-labeling-semantics",
        "doc_section": "Components > Icon Buttons > ARIA Labeling Semantics",
        "requirement": (
            "All interactive controls must feature appropriate ARIA attributes (aria-label, "
            "aria-expanded, aria-pressed, aria-current, role) and never include the element role in labels."
        ),
    },
    "ACCESSIBILITY_WEB_LANDMARKS": {
        "url": "https://m3.material.io/foundations/designing/structure#dafa42e2-b056-42b9-ab75-9c9ea9f293b7",
        "section": "Foundations > Accessible design > Structure > Web landmarks and headings",
        "doc_url": "components/app.html#web-landmarks",
        "doc_section": "Components > App Scaffold & Layout > Web Landmarks",
        "requirement": (
            "Web pages must define banner, navigation, main, complementary, and contentinfo "
            "landmarks with distinct accessibility labels when multiple landmarks share a role."
        ),
    },
    "ACCESSIBILITY_FOCUS_FLOW": {
        "url": "https://m3.material.io/foundations/designing/flow#74d866b2-f8e4-4dbb-a352-8019b2a384b1",
        "section": "Foundations > Accessible design > Flow > Focus order & key traversal",
        "doc_url": "components/app.html#focus-flow",
        "doc_section": "Components > App Scaffold & Layout > Focus Flow",
        "requirement": (
            "Keyboard traversal must follow logical reading order and return focus to the "
            "activating control when a modal context (dialog or drawer) closes."
        ),
    },
    "COMPONENTS_THEME_TOGGLE": {
        "url": "https://m3.material.io/styles/color/system/how-the-system-works#6e7242c4-8bea-4f96-b47a-c91a43181d18",
        "section": "Styles > Color > System > How the system works > 5. The algorithm assigns tones to color roles",
        "doc_url": "components/theme-toggle.html#theme-toggle-behavior",
        "doc_section": "Components > Theme Toggle > Theme Toggle Behavior",
        "requirement": (
            "Theme toggle component (<md3-theme-toggle>) switches document.documentElement.dataset.theme "
            "between light and dark, updates aria-pressed, and persists preference in localStorage."
        ),
    },
    "COMPONENTS_PAGEFIND_SEARCH": {
        "url": "https://m3.material.io/components/search/specs#dc1fa291-5ef3-4fd4-a2b6-e9d91b5f39ff",
        "section": "Components > Search > Specs > Search view",
        "doc_url": "components/search.html#pagefind-full-site-search",
        "doc_section": "Components > Search Bar & Dialog > Pagefind Full-Site Search",
        "requirement": (
            "Full-site search indexes documentation pages with Pagefind at build time and renders "
            "MD3 result cards with highlighted excerpts and deep-linked section sub-results."
        ),
    },
    "PROGRESSIVE_ENHANCEMENT_LIGHT_DOM": {
        "url": "https://m3.material.io/foundations/overview/principles#25cda2a6-e748-4efc-be27-8be7b1966fc5",
        "section": "Foundations > Accessible design > Overview > Principles",
        "doc_url": "components/progressive-enhancement.html#light-dom-architecture",
        "doc_section": "Components > No-JavaScript & Progressive Enhancement > Light DOM Architecture",
        "requirement": (
            "All navigation, content, and interactive controls render in the Light DOM at build time "
            "and remain accessible under :root.no-js when JavaScript is disabled."
        ),
    },
    "PROGRESSIVE_ENHANCEMENT_NO_JS": {
        "url": "https://m3.material.io/foundations/designing/structure#dafa42e2-b056-42b9-ab75-9c9ea9f293b7",
        "section": "Foundations > Accessible design > Structure > Web landmarks and headings",
        "doc_url": "components/progressive-enhancement.html#no-js-navigation-and-controls",
        "doc_section": "Components > No-JavaScript & Progressive Enhancement > No-JS Navigation and Controls",
        "requirement": (
            "When JavaScript is disabled, progressive disclosure navigation links, HTML Popover "
            "drawers/menus, and CSS :has() theme switching operate without client scripts."
        ),
    },
    "PROGRESSIVE_ENHANCEMENT_JS": {
        "url": "https://m3.material.io/components/navigation-drawer/guidelines#761e9679-2e72-4a85-894d-55bc3666b567",
        "section": "Components > Navigation Drawer > Guidelines > Usage",
        "doc_url": "components/progressive-enhancement.html#javascript-progressive-enhancements",
        "doc_section": "Components > No-JavaScript & Progressive Enhancement > JavaScript Progressive Enhancements",
        "requirement": (
            "When JavaScript is enabled, <md3-sidebar> supports in-place navigation graph traversal "
            "across ancestor and child levels without reloading the page."
        ),
    },
}


# ==============================================================================
# Failure Formatting & Assertion Utilities
# ==============================================================================

def format_md3_failure(
    detail: str,
    url: str,
    section: str,
    requirement: str,
    doc_url: Optional[str] = None,
    doc_section: Optional[str] = None,
) -> str:
    """Formats an assertion failure with component doc deeplinks and MD3 specification details."""
    border = "=" * 80
    sub_border = "-" * 80
    doc_lines = ""
    if doc_url:
        if doc_section:
            doc_lines += f"  Doc Section:   {doc_section}\n"
        doc_lines += f"  Component Doc: {doc_url}\n"
    return (
        f"{detail}\n\n"
        f"{border}\n"
        f"MATERIAL DESIGN 3 (MD3) SPECIFICATION CONFORMANCE FAILURE\n"
        f"{sub_border}\n"
        f"{doc_lines}"
        f"  Spec Section:  {section}\n"
        f"  Spec Deeplink: {url}\n"
        f"  Requirement:   {requirement}\n"
        f"{border}\n"
    )


def md3_conformance(
    spec_key: Optional[str] = None,
    url: Optional[str] = None,
    section: Optional[str] = None,
    requirement: Optional[str] = None,
    doc_url: Optional[str] = None,
    doc_section: Optional[str] = None,
) -> Callable:
    """Decorator for test methods that enriches any AssertionError with component doc & MD3 spec deeplinks."""
    resolved_url = url
    resolved_section = section
    resolved_req = requirement
    resolved_doc_url = doc_url
    resolved_doc_section = doc_section

    if spec_key is not None:
        if spec_key not in MD3_SPECS:
            raise KeyError(f"Unknown MD3_SPECS key: {spec_key!r}")
        entry = MD3_SPECS[spec_key]
        resolved_url = resolved_url or entry["url"]
        resolved_section = resolved_section or entry["section"]
        resolved_req = resolved_req or entry["requirement"]
        resolved_doc_url = resolved_doc_url or entry.get("doc_url")
        resolved_doc_section = resolved_doc_section or entry.get("doc_section")

    def decorator(fn: Callable) -> Callable:
        @functools.wraps(fn)
        def wrapped(*args, **kwargs):
            try:
                return fn(*args, **kwargs)
            except AssertionError as exc:
                orig_msg = str(exc)
                if "MATERIAL DESIGN 3 (MD3) SPECIFICATION CONFORMANCE FAILURE" in orig_msg:
                    raise
                if resolved_url:
                    enriched = format_md3_failure(
                        detail=orig_msg,
                        url=resolved_url,
                        section=resolved_section or "MD3 Specification",
                        requirement=resolved_req or "Must conform to Material Design 3 guidelines.",
                        doc_url=resolved_doc_url,
                        doc_section=resolved_doc_section,
                    )
                    raise AssertionError(enriched) from None
                raise
        return wrapped
    return decorator


class Md3ConformanceMixin:
    """Mixin for unittest.TestCase providing MD3 spec-aware assertions and context managers."""

    @contextlib.contextmanager
    def spec_context(
        self,
        spec_key: Optional[str] = None,
        url: Optional[str] = None,
        section: Optional[str] = None,
        requirement: Optional[str] = None,
        doc_url: Optional[str] = None,
        doc_section: Optional[str] = None,
    ):
        """Context manager to associate a specific code block with component doc & MD3 spec deeplinks."""
        resolved_url = url
        resolved_section = section
        resolved_req = requirement
        resolved_doc_url = doc_url
        resolved_doc_section = doc_section

        if spec_key is not None:
            if spec_key not in MD3_SPECS:
                raise KeyError(f"Unknown MD3_SPECS key: {spec_key!r}")
            entry = MD3_SPECS[spec_key]
            resolved_url = resolved_url or entry["url"]
            resolved_section = resolved_section or entry["section"]
            resolved_req = resolved_req or entry["requirement"]
            resolved_doc_url = resolved_doc_url or entry.get("doc_url")
            resolved_doc_section = resolved_doc_section or entry.get("doc_section")

        try:
            yield
        except AssertionError as exc:
            orig = str(exc)
            if "MATERIAL DESIGN 3 (MD3) SPECIFICATION CONFORMANCE FAILURE" in orig:
                raise
            if resolved_url:
                enriched = format_md3_failure(
                    detail=orig,
                    url=resolved_url,
                    section=resolved_section or "MD3 Specification",
                    requirement=resolved_req or "Must conform to Material Design 3 guidelines.",
                    doc_url=resolved_doc_url,
                    doc_section=resolved_doc_section,
                )
                raise AssertionError(enriched) from None
            raise

    def assert_md3_equal(
        self,
        actual: Any,
        expected: Any,
        spec_key: Optional[str] = None,
        msg: Optional[str] = None,
        url: Optional[str] = None,
        section: Optional[str] = None,
        requirement: Optional[str] = None,
        doc_url: Optional[str] = None,
        doc_section: Optional[str] = None,
    ):
        """Asserts equality with associated component doc & MD3 specification deeplinks."""
        with self.spec_context(
            spec_key=spec_key,
            url=url,
            section=section,
            requirement=requirement,
            doc_url=doc_url,
            doc_section=doc_section,
        ):
            self.assertEqual(actual, expected, msg=msg)

    def assert_md3_almost_equal(
        self,
        actual: Any,
        expected: Any,
        spec_key: Optional[str] = None,
        delta: Optional[float] = None,
        msg: Optional[str] = None,
        url: Optional[str] = None,
        section: Optional[str] = None,
        requirement: Optional[str] = None,
        doc_url: Optional[str] = None,
        doc_section: Optional[str] = None,
    ):
        """Asserts almost-equal with associated component doc & MD3 specification deeplinks."""
        with self.spec_context(
            spec_key=spec_key,
            url=url,
            section=section,
            requirement=requirement,
            doc_url=doc_url,
            doc_section=doc_section,
        ):
            self.assertAlmostEqual(actual, expected, delta=delta, msg=msg)

    def assert_md3_in(
        self,
        member: Any,
        container: Any,
        spec_key: Optional[str] = None,
        msg: Optional[str] = None,
        url: Optional[str] = None,
        section: Optional[str] = None,
        requirement: Optional[str] = None,
        doc_url: Optional[str] = None,
        doc_section: Optional[str] = None,
    ):
        """Asserts inclusion with associated component doc & MD3 specification deeplinks."""
        with self.spec_context(
            spec_key=spec_key,
            url=url,
            section=section,
            requirement=requirement,
            doc_url=doc_url,
            doc_section=doc_section,
        ):
            self.assertIn(member, container, msg=msg)

    def assert_md3_true(
        self,
        expr: Any,
        spec_key: Optional[str] = None,
        msg: Optional[str] = None,
        url: Optional[str] = None,
        section: Optional[str] = None,
        requirement: Optional[str] = None,
        doc_url: Optional[str] = None,
        doc_section: Optional[str] = None,
    ):
        """Asserts boolean truth with associated component doc & MD3 specification deeplinks."""
        with self.spec_context(
            spec_key=spec_key,
            url=url,
            section=section,
            requirement=requirement,
            doc_url=doc_url,
            doc_section=doc_section,
        ):
            self.assertTrue(expr, msg=msg)

    def assert_md3_greater_equal(
        self,
        a: Any,
        b: Any,
        spec_key: Optional[str] = None,
        msg: Optional[str] = None,
        url: Optional[str] = None,
        section: Optional[str] = None,
        requirement: Optional[str] = None,
        doc_url: Optional[str] = None,
        doc_section: Optional[str] = None,
    ):
        """Asserts greater-or-equal with associated component doc & MD3 specification deeplinks."""
        with self.spec_context(
            spec_key=spec_key,
            url=url,
            section=section,
            requirement=requirement,
            doc_url=doc_url,
            doc_section=doc_section,
        ):
            self.assertGreaterEqual(a, b, msg=msg)

    def assert_md3_less_equal(
        self,
        a: Any,
        b: Any,
        spec_key: Optional[str] = None,
        msg: Optional[str] = None,
        url: Optional[str] = None,
        section: Optional[str] = None,
        requirement: Optional[str] = None,
        doc_url: Optional[str] = None,
        doc_section: Optional[str] = None,
    ):
        """Asserts less-or-equal with associated component doc & MD3 specification deeplinks."""
        with self.spec_context(
            spec_key=spec_key,
            url=url,
            section=section,
            requirement=requirement,
            doc_url=doc_url,
            doc_section=doc_section,
        ):
            self.assertLessEqual(a, b, msg=msg)
