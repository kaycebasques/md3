project = "md3"
author = "Kayce Basques"
copyright = f"2026, {author}"

# Normal users who `pip install md3` only need `html_theme = "md3"` because the
# wheel's `sphinx.html_themes` entry point tells Sphinx to load the `md3` module
# automatically. In our local Bazel build, `//docs:sphinx` depends on the raw
# `//md3` `py_library` (not an installed wheel, so there is no entry_points.txt
# on `sys.path`), which means we must explicitly load `md3` via `extensions` so
# `md3.setup(app)` runs and registers the theme.
extensions = ["md3"]
html_theme = "md3"
