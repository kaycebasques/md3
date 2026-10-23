* we are creating a sphinx theme for large, professional docs sites
* the theme will conform to material design 3 (md3)
* we only use vanilla css/html/js features that are supported in all browsers
* javascript should be used only as a last-resort progressive enhancement
* run all tests: `./bazelisk test //...`
* build the docs: `./bazelisk build //docs`
* docs output: `bazel-bin/docs/docs/_build/html/`
* the theme must produce fast, usable, and accessible docs sites by default
* maximize information density while still conforming to md3
* place official md3 components in `md3/components/md3/` and app components in `md3/components/app/`
* inside custom elements, style semantic html and aria attributes directly rather than adding bem classes or extra wrapper elements
* only load a component's css and js when that component is enabled
* validate `html_theme_options` types strictly (e.g. require `True` or `False` for booleans and raise `sphinx.errors.ConfigError` on invalid values)
* all ui strings in templates and python must be translatable via sphinx gettext (`_`), and keep `pt_BR` catalogs (`md3/locales/` and `docs/locales/`) up to date
* keep each test method self-contained with its own inline `files` dict (no shared `setUp` fixtures) and avoid repeating the component name in `Test*` method names
* include links to our docs and/or `https://m3.material.io/` in `test_md3` assertion failure messages; do not write "dead docs" that reiterate md3 css measurements
* agents should feel free to add content to this file as needed
