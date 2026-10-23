from pathlib import Path

from sphinx.errors import ConfigError
from sphinx.locale import _


def configure_theme(app, config):
    tabs_enabled = config.html_theme_options.get("tabs", True)
    if not isinstance(tabs_enabled, bool):
        raise ConfigError("html_theme_options['tabs'] must be a bool")

    components_dir = str(Path(__file__).resolve().parent / "components")
    if components_dir not in config.html_static_path:
        config.html_static_path.append(components_dir)


def _in_subtree(includes: dict[str, list[str]], root: str, target: str) -> bool:
    stack = [root]
    seen = set()
    while stack:
        doc = stack.pop()
        if doc == target:
            return True
        if doc not in seen:
            seen.add(doc)
            stack.extend(includes.get(doc, ()))
    return False


def setup_navigation_context(app, pagename, templatename, context, doctree):
    if not app.config.html_theme_options.get("tabs", True):
        context["md3_tabs"] = []
        return

    env = app.env
    root_doc = app.config.root_doc
    includes = env.toctree_includes

    tabs = [
        {
            "title": _("Home"),
            "url": context["pathto"](root_doc),
            "active": pagename == root_doc,
        }
    ]
    for child in includes.get(root_doc, ()):
        title_node = env.titles.get(child)
        title = title_node.astext() if title_node else child
        tabs.append({
            "title": title,
            "url": context["pathto"](child),
            "active": pagename != root_doc and _in_subtree(includes, child, pagename),
        })
    context["md3_tabs"] = tabs


def setup(app):
    package_dir = Path(__file__).resolve().parent
    app.add_html_theme("md3", package_dir)
    app.add_message_catalog("sphinx", package_dir / "locales")
    app.connect("config-inited", configure_theme)
    app.connect("html-page-context", setup_navigation_context)
    return {
        "version": "0.0.0",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
