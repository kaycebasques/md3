import asyncio
from collections import deque
import concurrent.futures
import json
from pathlib import Path


def add_components_static_path(app, config):
    components_dir = str(Path(__file__).resolve().parent / "components")
    if components_dir not in config.html_static_path:
        config.html_static_path.append(components_dir)


def _get_doc_title(env, docname: str) -> str:
    title_node = env.titles.get(docname)
    if title_node is not None:
        text = title_node.astext().strip()
        if text:
            return text
    return docname.split("/")[-1].replace("_", " ").replace("-", " ").title()


def _build_site_nav_graph(env, root_doc: str):
    """Builds and caches the site toctree hierarchy for progressive disclosure."""
    cache_key = id(env.tocs)
    cached = getattr(env, "_md3_nav_graph", None)
    if cached and cached.get("key") == cache_key and cached.get("root_doc") == root_doc:
        return cached

    from sphinx import addnodes

    doc_groups = {}
    doc_children = {}
    all_known_docs = set(env.titles.keys()) | set(getattr(env, "found_docs", set()))

    for docname, toc_node in env.tocs.items():
        groups = []
        flat_children = []
        if toc_node is not None:
            for toctree in toc_node.findall(addnodes.toctree):
                caption = toctree.get("caption")
                entries = []
                for explicit_title, ref in toctree.get("entries", []):
                    if ref == "self":
                        ref = docname
                    is_internal = ref in all_known_docs
                    if explicit_title:
                        entry_title = explicit_title
                    elif is_internal:
                        entry_title = _get_doc_title(env, ref)
                    else:
                        entry_title = ref
                    item = {
                        "title": entry_title,
                        "ref": ref,
                        "is_internal": is_internal,
                    }
                    entries.append(item)
                    flat_children.append(item)
                if entries:
                    groups.append({
                        "caption": caption,
                        "items": entries,
                    })
        doc_groups[docname] = groups
        doc_children[docname] = flat_children

    parent_map = {}
    queue = deque([root_doc])
    visited = {root_doc}
    while queue:
        curr = queue.popleft()
        for item in doc_children.get(curr, []):
            if item["is_internal"]:
                child_doc = item["ref"]
                if child_doc not in visited:
                    visited.add(child_doc)
                    parent_map[child_doc] = curr
                    queue.append(child_doc)

    # Also cover any documents that were not directly reached from root_doc
    for docname, children in doc_children.items():
        for item in children:
            if item["is_internal"]:
                child_doc = item["ref"]
                if child_doc != root_doc and child_doc not in parent_map:
                    parent_map[child_doc] = docname

    nodes = {}
    for docname in sorted(all_known_docs | set(doc_groups.keys()) | {root_doc}):
        nodes[docname] = {
            "title": _get_doc_title(env, docname),
            "parent": parent_map.get(docname),
            "groups": [
                {
                    "caption": grp["caption"],
                    "items": [
                        {
                            "title": item["title"],
                            "ref": item["ref"],
                            "docname": item["ref"],
                            "is_internal": item["is_internal"],
                            "has_children": bool(
                                item["is_internal"] and doc_children.get(item["ref"])
                            ),
                        }
                        for item in grp["items"]
                    ],
                }
                for grp in doc_groups.get(docname, [])
            ],
        }

    graph_json = json.dumps(
        {"root_doc": root_doc, "nodes": nodes},
        separators=(",", ":"),
    ).replace("</", "<\\/")

    result = {
        "key": cache_key,
        "root_doc": root_doc,
        "doc_groups": doc_groups,
        "doc_children": doc_children,
        "parent_map": parent_map,
        "graph_json": graph_json,
    }
    env._md3_nav_graph = result
    return result


import html
import re


def _resolve_entry_url(context, item) -> str:
    ref = item["ref"]
    if item["is_internal"]:
        return context["pathto"](ref)
    if "://" in ref or ref.startswith("#") or ref.startswith("mailto:"):
        return ref
    return context["pathto"](ref, 1)


def setup_navigation_context(app, pagename, templatename, context, doctree):
    """Populates context with top-level header tabs and 1-level progressive disclosure sidebar data."""
    env = app.env
    root_doc = getattr(app.config, "root_doc", None) or getattr(app.config, "master_doc", "index")
    graph = _build_site_nav_graph(env, root_doc)
    doc_groups = graph["doc_groups"]
    doc_children = graph["doc_children"]
    parent_map = graph["parent_map"]

    file_suffix = context.get("file_suffix") or ".html"
    depth = pagename.count("/")
    context["md3_site_root_prefix"] = "./" if depth == 0 else "../" * depth
    context["md3_nav_graph_json"] = graph["graph_json"]
    context["md3_site_root_url"] = context["pathto"](root_doc + file_suffix, 1)

    # Build ancestor chain from root_doc to pagename: [root_doc, ..., pagename]
    chain = []
    curr = pagename
    seen_chain = set()
    while curr and curr not in seen_chain:
        seen_chain.add(curr)
        chain.append(curr)
        curr = parent_map.get(curr)
    chain.reverse()

    # Full ancestor breadcrumb parents (excluding root_doc and pagename itself)
    breadcrumb_parents = []
    if len(chain) > 2:
        for anc in chain[1:-1]:
            breadcrumb_parents.append({
                "title": _get_doc_title(env, anc),
                "link": context["pathto"](anc),
            })
    context["md3_breadcrumb_parents"] = breadcrumb_parents

    # 1. Top-level navigation tabs near the header (root_doc + direct L1 children of root_doc)
    root_children = doc_children.get(root_doc, [])
    root_title = _get_doc_title(env, root_doc)
    nav_tabs = [
        {
            "title": "Home",
            "url": context["pathto"](root_doc),
            "active": pagename == root_doc,
            "docname": root_doc,
        }
    ]
    for item in root_children:
        is_active = bool(item["is_internal"] and item["ref"] in seen_chain and pagename != root_doc)
        nav_tabs.append({
            "title": item["title"],
            "url": _resolve_entry_url(context, item),
            "active": is_active,
            "docname": item["ref"],
        })
    context["md3_nav_tabs"] = nav_tabs

    # 2. Progressive Disclosure Sidebar (shows strictly 1 level of docs at a time)
    page_has_children = bool(doc_children.get(pagename))
    parent_doc = parent_map.get(pagename)

    if page_has_children:
        # Current page is a section hub: show its own direct children (1 level)
        active_level_doc = pagename
        ancestor_docs = chain[:-1]
        section_header = (
            {
                "title": _get_doc_title(env, pagename),
                "url": context["pathto"](pagename),
                "current": True,
                "docname": pagename,
            }
            if pagename != root_doc
            else None
        )
    elif parent_doc is not None:
        # Current page is a leaf document: show siblings under parent_doc (1 level)
        active_level_doc = parent_doc
        # Ancestors above parent_doc
        parent_idx = chain.index(parent_doc) if parent_doc in chain else 0
        ancestor_docs = chain[:parent_idx]
        section_header = (
            {
                "title": _get_doc_title(env, parent_doc),
                "url": context["pathto"](parent_doc),
                "current": False,
                "docname": parent_doc,
            }
            if parent_doc != root_doc
            else {
                "title": root_title,
                "url": context["pathto"](root_doc),
                "current": False,
                "docname": root_doc,
            }
        )
    elif root_children and pagename != root_doc:
        # Orphan page (e.g., genindex or search) in a multi-page project
        active_level_doc = root_doc
        ancestor_docs = []
        section_header = {
            "title": root_title,
            "url": context["pathto"](root_doc),
            "current": False,
            "docname": root_doc,
        }
    else:
        # Single-page site with no toctree
        active_level_doc = None
        ancestor_docs = []
        section_header = None

    ancestors = [
        {
            "title": _get_doc_title(env, anc),
            "url": context["pathto"](anc),
            "docname": anc,
        }
        for anc in ancestor_docs
    ]

    rendered_groups = []
    total_items = 0
    if active_level_doc is not None:
        for grp in doc_groups.get(active_level_doc, []):
            grp_items = []
            for item in grp["items"]:
                is_current = bool(item["is_internal"] and item["ref"] == pagename)
                item_has_children = bool(item["is_internal"] and doc_children.get(item["ref"]))
                grp_items.append({
                    "title": item["title"],
                    "url": _resolve_entry_url(context, item),
                    "current": is_current,
                    "has_children": item_has_children,
                    "docname": item["ref"],
                })
                total_items += 1
            if grp_items:
                rendered_groups.append({
                    "caption": grp["caption"],
                    "items": grp_items,
                })
    else:
        rendered_groups.append({
            "caption": None,
            "items": [
                {
                    "title": context.get("title") or root_title,
                    "url": context["pathto"](pagename),
                    "current": True,
                    "has_children": False,
                    "docname": pagename,
                }
            ],
        })
        total_items = 1

    context["md3_sidebar_nav"] = {
        "ancestors": ancestors,
        "section_header": section_header,
        "groups": rendered_groups,
        "total_items": total_items,
        "active_level_doc": active_level_doc or pagename,
    }


_THEME_BOOTSTRAP_SCRIPT = """<script>
  (function() {
    document.documentElement.classList.remove('no-js');
    var stored = null;
    try {
      var mode = localStorage.getItem('mode');
      var theme = localStorage.getItem('theme');
      if (mode === 'auto' || theme === 'auto') {
        localStorage.removeItem('mode');
        localStorage.removeItem('theme');
        localStorage.setItem('rustdoc-use-system-theme', 'true');
      } else {
        stored = theme || mode;
      }
    } catch (e) {}
    var prefersDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
    var resolved = (stored === 'light' || stored === 'dark') ? stored : (prefersDark ? 'dark' : 'light');
    document.documentElement.dataset.theme = resolved;
    document.documentElement.dataset.mode = resolved;
    document.documentElement.classList.remove('light-mode', 'dark-mode');
    document.documentElement.classList.add(resolved + '-mode');
  })();
</script>"""


def _extract_subsite_page_title(text: str, subsite_type: str) -> str:
    """Extracts a clean human-readable page title from Doxygen or Rustdoc HTML."""
    if subsite_type == "doxygen":
        cleaned_header = re.sub(
            r'<div\s+class="ingroups"[^>]*>.*?</div>',
            "",
            text,
            flags=re.DOTALL | re.IGNORECASE,
        )
        cleaned_header = re.sub(
            r'<span\s+class="mlabels"[^>]*>.*?</span>',
            "",
            cleaned_header,
            flags=re.DOTALL | re.IGNORECASE,
        )
        m = re.search(
            r'<div\s+class="headertitle"[^>]*>\s*<div\s+class="title"[^>]*>(.*?)</div>',
            cleaned_header,
            re.DOTALL | re.IGNORECASE,
        )
        if m:
            raw = m.group(1)
            cleaned = html.unescape(re.sub(r"<[^>]+>", "", raw)).strip()
            if cleaned:
                return cleaned
    elif subsite_type == "rustdoc":
        m = re.search(
            r'<div\s+class="main-heading"[^>]*>.*?<h1[^>]*>(.*?)</h1>',
            text,
            re.DOTALL | re.IGNORECASE,
        )
        if m:
            raw = m.group(1)
            raw = re.sub(r"<button[^>]*>.*?</button>", "", raw, flags=re.DOTALL | re.IGNORECASE)
            cleaned = html.unescape(re.sub(r"<[^>]+>", "", raw)).replace("\xa0", " ").replace("Copy item path", "").strip()
            if cleaned:
                return cleaned

    m_title = re.search(r"<title[^>]*>(.*?)</title>", text, re.DOTALL | re.IGNORECASE)
    if m_title:
        cleaned = html.unescape(re.sub(r"<[^>]+>", "", m_title.group(1))).strip()
        if subsite_type == "rustdoc" and cleaned.endswith(" - Rust"):
            cleaned = cleaned[: -len(" - Rust")].strip()
        if cleaned:
            return cleaned
    return "C++ API" if subsite_type == "doxygen" else ("Rust API" if subsite_type == "rustdoc" else "Documentation")


def _build_universal_header_html(
    *,
    project: str,
    root_doc: str,
    root_prefix: str,
    site_root_attr: str,
    subsite_type: str,
    skip_target: str,
    logo_rel: str,
    source_url: str,
    source_label: str,
    raw_tabs: list,
    breadcrumbs_items_html: str,
    ancestor_docnames: set[str] | None = None,
) -> str:
    home_href = f"{root_prefix}{root_doc}.html"
    logo_html = ""
    if logo_rel:
        logo_src = logo_rel if ("://" in logo_rel or logo_rel.startswith("/")) else f"{root_prefix}{logo_rel.lstrip('/')}"
        logo_html = f'<img class="md3-brand__logo" src="{html.escape(logo_src)}" alt="{html.escape(project)} logo"/>'

    source_html = ""
    if source_url:
        source_html = f"""
        <a class="md3-icon-btn md3-source-link" id="md3-source-link" href="{html.escape(source_url)}" aria-label="{html.escape(source_label)}" title="{html.escape(source_label)}">
          <svg class="md3-icon" viewBox="0 0 24 24" width="20" height="20" aria-hidden="true">
            <path d="M9.4 16.6L4.8 12l4.6-4.6L8 6l-6 6 6 6 1.4-1.4zm5.2 0l4.6-4.6-4.6-4.6L16 6l6 6-6 6-1.4-1.4z"/>
          </svg>
        </a>"""

    ancestor_set = ancestor_docnames or set()
    nav_tabs_html = ""
    if len(raw_tabs) > 1:
        tab_items = []
        for tab in raw_tabs:
            ref = tab["ref"]
            if tab["is_internal"]:
                tab_url = f"{root_prefix}{ref}.html"
            elif "://" in ref or ref.startswith("#") or ref.startswith("mailto:"):
                tab_url = ref
            else:
                tab_url = f"{root_prefix}{ref.lstrip('/')}"
            is_active = (
                (ref != root_doc and ref in ancestor_set)
                or (subsite_type == "doxygen" and ("doxygen" in ref or "api/cc" in ref))
                or (subsite_type == "rustdoc" and "rustdoc" in ref)
            )
            li_active_cls = " active" if is_active else ""
            active_cls = " active" if is_active else ""
            aria_curr = ' aria-current="page"' if is_active else ""
            tab_items.append(
                f'<li class="md3-nav-tabs__item{li_active_cls}">'
                f'<a class="md3-nav-tabs__link{active_cls}" href="{html.escape(tab_url)}" data-docname="{html.escape(ref)}"{aria_curr}>'
                f'<span class="md3-nav-tabs__label">{html.escape(tab["title"])}</span>'
                f'<span class="md3-nav-tabs__indicator" aria-hidden="true"></span>'
                f"</a></li>"
            )
        nav_tabs_html = f"""
      <md3-nav-tabs class="md3-nav-tabs" data-pagefind-ignore="all">
        <nav class="md3-nav-tabs__nav" aria-label="Primary sections">
          <ul class="md3-nav-tabs__list">
            {"".join(tab_items)}
          </ul>
        </nav>
      </md3-nav-tabs>"""

    return f"""<a class="md3-skip-link" id="md3-skip-link" href="{html.escape(skip_target)}" data-pagefind-ignore="all">Skip to main content</a>
    <div class="md3-universal-header" id="md3-universal-header" data-subsite="{html.escape(subsite_type)}" data-site-root="{html.escape(site_root_attr)}" data-pagefind-ignore="all">
      <md3-top-app-bar class="md3-top-app-bar" data-pagefind-ignore="all">
        <div class="md3-top-app-bar__start">
          <button class="md3-icon-btn md3-drawer-toggle" id="drawer-toggle" aria-label="Toggle navigation drawer" title="Toggle navigation drawer" aria-expanded="false" type="button">
            <svg class="md3-icon" viewBox="0 0 24 24" width="20" height="20" aria-hidden="true">
              <path d="M3 18h18v-2H3v2zm0-5h18v-2H3v2zm0-7v2h18V6H3z"/>
            </svg>
          </button>
          <a class="md3-brand" href="{html.escape(home_href)}">
            {logo_html}
            <span class="md3-brand__title">{html.escape(project)}</span>
          </a>
        </div>
        <div class="md3-top-app-bar__center">
          <button class="md3-search-bar" id="search-bar-trigger" type="button" aria-label="Search documentation" title="Search documentation (Ctrl+K or /)">
            <svg class="md3-icon md3-search-icon" viewBox="0 0 24 24" width="18" height="18" aria-hidden="true">
              <path d="M15.5 14h-.79l-.28-.27A6.471 6.471 0 0 0 16 9.5 6.5 6.5 0 1 0 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z"/>
            </svg>
            <span class="md3-search-placeholder">Search docs...</span>
            <kbd class="md3-kbd-shortcut">Ctrl+K</kbd>
          </button>
        </div>
        <div class="md3-top-app-bar__end">
          <button class="md3-icon-btn md3-search-mobile-btn" id="search-mobile-trigger" type="button" aria-label="Search documentation" title="Search documentation">
            <svg class="md3-icon" viewBox="0 0 24 24" width="20" height="20" aria-hidden="true">
              <path d="M15.5 14h-.79l-.28-.27A6.471 6.471 0 0 0 16 9.5 6.5 6.5 0 1 0 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z"/>
            </svg>
          </button>
          <md3-theme-toggle class="md3-theme-toggle">
            <button type="button" class="md3-theme-toggle__native-btn" id="theme-menu-btn" popovertarget="md3-theme-menu" aria-label="Toggle color theme" title="Toggle color theme" aria-pressed="false">
              <svg class="md3-icon md3-theme-toggle__icon--light" viewBox="0 0 24 24" width="20" height="20" aria-hidden="true">
                <path d="M12 7c-2.76 0-5 2.24-5 5s2.24 5 5 5 5-2.24 5-5-2.24-5-5-5zM2 13h2c.55 0 1-.45 1-1s-.45-1-1-1H2c-.55 0-1 .45-1 1s.45 1 1 1zm18 0h2c.55 0 1-.45 1-1s-.45-1-1-1h-2c-.55 0-1 .45-1 1s.45 1 1 1zM11 2v2c0 .55.45 1 1 1s1-.45 1-1V2c0-.55-.45-1-1-1s-1 .45-1 1zm0 18v2c0 .55.45 1 1 1s1-.45 1-1v-2c0-.55-.45-1-1-1s-1 .45-1 1zM5.99 4.58a.996.996 0 0 0-1.41 0 .996.996 0 0 0 0 1.41l1.06 1.06c.39.39 1.03.39 1.41 0s.39-1.03 0-1.41L5.99 4.58zm12.37 12.37a.996.996 0 0 0-1.41 0 .996.996 0 0 0 0 1.41l1.06 1.06c.39.39 1.03.39 1.41 0a.996.996 0 0 0 0-1.41l-1.06-1.06zm1.06-10.96a.996.996 0 0 0 0-1.41.996.996 0 0 0-1.41 0l-1.06 1.06c-.39.39-.39 1.03 0 1.41s1.03.39 1.41 0l1.06-1.06zM7.05 18.36a.996.996 0 0 0 0-1.41.996.996 0 0 0-1.41 0l-1.06 1.06c-.39.39-.39 1.03 0 1.41s1.03.39 1.41 0l1.06-1.06z"/>
              </svg>
              <svg class="md3-icon md3-theme-toggle__icon--dark" viewBox="0 0 24 24" width="20" height="20" aria-hidden="true">
                <path d="M12 3a9 9 0 1 0 9 9c0-.46-.04-.92-.1-1.36a5.389 5.389 0 0 1-4.4 2.26 5.403 5.403 0 0 1-3.14-9.8c-.44-.06-.9-.1-1.36-.1z"/>
              </svg>
            </button>
            <div id="md3-theme-menu" class="md3-theme-menu" popover>
              <fieldset class="md3-theme-fieldset">
                <legend class="md3-theme-legend">Appearance</legend>
                <label class="md3-theme-option">
                  <input type="radio" name="theme" value="light" checked />
                  <span>Light</span>
                </label>
                <label class="md3-theme-option">
                  <input type="radio" name="theme" value="dark" />
                  <span>Dark</span>
                </label>
              </fieldset>
            </div>
          </md3-theme-toggle>{source_html}
        </div>
      </md3-top-app-bar>{nav_tabs_html}
      <nav class="md3-breadcrumbs md3-subsite-breadcrumbs" id="md3-subsite-breadcrumbs" aria-label="Breadcrumb" data-pagefind-ignore="all">
        <ol class="md3-breadcrumbs__list">
          {breadcrumbs_items_html}
        </ol>
      </nav>
    </div>
    <div class="md3-backdrop" id="md3-backdrop" aria-hidden="true" data-pagefind-ignore="all"></div>
    <md3-search class="md3-search" id="md3-search" data-pagefind-ignore="all">
      <dialog class="md3-search-dialog" id="md3-search-dialog" aria-label="Search Documentation">
        <div class="md3-search-dialog__container">
          <div class="md3-search-dialog__header">
            <svg class="md3-icon" viewBox="0 0 24 24" width="20" height="20" aria-hidden="true">
              <path d="M15.5 14h-.79l-.28-.27A6.471 6.471 0 0 0 16 9.5 6.5 6.5 0 1 0 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z"/>
            </svg>
            <input type="search" class="md3-search-input" id="md3-search-input" placeholder="Search documentation..." autocomplete="off" />
            <button class="md3-icon-btn" id="md3-search-close" type="button" aria-label="Close search" title="Close search">
              <svg class="md3-icon" viewBox="0 0 24 24" width="20" height="20" aria-hidden="true">
                <path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/>
              </svg>
            </button>
          </div>
          <div class="md3-search-dialog__body" id="md3-search-results">
            <div class="md3-search-hint">Type a query to search documentation. Press <kbd class="md3-kbd-shortcut">ESC</kbd> to exit.</div>
          </div>
        </div>
      </dialog>
    </md3-search>"""


def _resolve_subsite_url_ancestors(
    rel_path: Path,
    outdir_path: Path,
    env,
    root_doc: str,
    parent_map: dict[str, str],
    all_known_docs: set[str],
) -> tuple[list[tuple[str, str]], set[str]]:
    """Resolves URL-hierarchy ancestor Sphinx pages (e.g. api/index -> 'Reference' for api/cc/...)
    between the site root and the subsite directory.

    Returns (breadcrumbs_list_of_(title, rel_doc_html), ancestor_docnames_set).
    """
    dir_parts = rel_path.parts[:-1]
    if len(dir_parts) <= 1:
        return [], set()

    # Walk ancestor directory prefixes above the subsite's own directory (dir_parts[:-1])
    matched_docs: list[str] = []
    extra_crumbs: list[tuple[str, str]] = []
    for i in range(1, len(dir_parts)):
        prefix = "/".join(dir_parts[:i])
        cand_index = f"{prefix}/index"
        if cand_index in all_known_docs and cand_index != root_doc:
            matched_docs.append(cand_index)
        elif prefix in all_known_docs and prefix != root_doc:
            matched_docs.append(prefix)
        elif (outdir_path / prefix / "index.html").exists():
            try:
                idx_html = (outdir_path / prefix / "index.html").read_text(encoding="utf-8")
                idx_title = _extract_subsite_page_title(idx_html, "subsite")
            except OSError:
                idx_title = prefix.split("/")[-1].replace("_", " ").replace("-", " ").title()
            extra_crumbs.append((idx_title, f"{prefix}/index.html"))

    ancestor_docnames: set[str] = set()
    crumbs: list[tuple[str, str]] = []
    seen_hrefs: set[str] = set()

    for doc in matched_docs:
        # Build full toctree ancestor chain from root_doc to doc
        chain: list[str] = []
        curr: str | None = doc
        while curr and curr not in ancestor_docnames:
            chain.append(curr)
            curr = parent_map.get(curr)
        chain.reverse()
        for anc in chain:
            ancestor_docnames.add(anc)
            if anc == root_doc:
                continue
            href = f"{anc}.html"
            if href not in seen_hrefs:
                seen_hrefs.add(href)
                crumbs.append((_get_doc_title(env, anc), href))

    for title, href in extra_crumbs:
        if href not in seen_hrefs:
            seen_hrefs.add(href)
            crumbs.append((title, href))

    return crumbs, ancestor_docnames


def postprocess_universal_header(app, exception) -> None:
    """Replaces <!-- md3-sentinel --> / <!-- pw-sentinel --> in external subsites (Doxygen, Rustdoc)
    with the universal MD3 header, breadcrumbs, search dialog, and theme assets.
    """
    if exception is not None or getattr(app.builder, "format", None) != "html":
        return

    outdir_path = Path(app.outdir)
    env = app.env
    root_doc = getattr(app.config, "root_doc", None) or getattr(app.config, "master_doc", "index")
    graph = _build_site_nav_graph(env, root_doc)
    doc_children = graph["doc_children"]
    parent_map = graph["parent_map"]
    all_known_docs = set(env.titles.keys()) | set(getattr(env, "found_docs", set()))

    raw_tabs = [{"title": "Home", "ref": root_doc, "is_internal": True}]
    for item in doc_children.get(root_doc, []):
        raw_tabs.append({
            "title": item["title"],
            "ref": item["ref"],
            "is_internal": item["is_internal"],
        })

    project = getattr(app.config, "project", "Documentation") or "Documentation"
    theme_opts = getattr(app.config, "html_theme_options", {}) or {}
    html_logo = getattr(app.config, "html_logo", None)
    logo_opt = theme_opts.get("logo") or ""
    if html_logo:
        logo_str = str(html_logo)
        logo_rel = (
            logo_str
            if ("://" in logo_str or logo_str.startswith("/"))
            else f"_static/{Path(logo_str).name}"
        )
    elif logo_opt:
        logo_rel = logo_opt if ("://" in logo_opt or logo_opt.startswith("/")) else f"_static/{logo_opt.lstrip('/')}"
    else:
        logo_rel = ""

    source_url = theme_opts.get("source_url") or theme_opts.get("repo_url") or ""
    source_label = theme_opts.get("source_label") or "View source repository"
    baseurl = theme_opts.get("baseurl") or getattr(app.config, "html_baseurl", "") or ""

    if (outdir_path / "rustdoc" / "pw_bytes" / "index.html").exists():
        rustdoc_root_rel = "rustdoc/pw_bytes/index.html"
    else:
        rustdoc_root_rel = "rustdoc/index.html"

    for html_file in outdir_path.rglob("*.html"):
        try:
            text = html_file.read_text(encoding="utf-8")
        except OSError:
            continue

        if "<!-- md3-sentinel -->" not in text and "<!-- pw-sentinel -->" not in text:
            continue

        rel_path = html_file.relative_to(outdir_path)
        rel_posix = rel_path.as_posix()
        depth = len(rel_path.parts) - 1
        root_prefix = "./" if depth == 0 else "../" * depth
        site_root_attr = "." if depth == 0 else ("../" * depth).rstrip("/")

        if "rustdoc" in rel_path.parts or 'class="rustdoc' in text or "rustdoc-topbar" in text or "rustdoc-vars" in text:
            subsite_type = "rustdoc"
            skip_target = "#main-content"
        elif "doxygen" in rel_path.parts or "doxygen" in text.lower() or 'id="doc-content"' in text:
            subsite_type = "doxygen"
            skip_target = "#doc-content" if 'id="doc-content"' in text else "#main"
        else:
            subsite_type = "subsite"
            skip_target = "#main"

        page_title = _extract_subsite_page_title(text, subsite_type)
        home_href = f"{root_prefix}{root_doc}.html"

        breadcrumbs_parts = [
            f'<li class="md3-breadcrumbs__item">'
            f'<a class="md3-breadcrumbs__link md3-breadcrumbs__home" href="{html.escape(home_href)}" aria-label="Home">'
            f'<svg class="md3-icon md3-breadcrumbs__home-icon" viewBox="0 0 24 24" width="16" height="16" aria-hidden="true">'
            f'<path d="M10 20v-6h4v6h5v-8h3L12 3 2 12h3v8z"/>'
            f"</svg>"
            f'<span class="md3-breadcrumbs__home-text">Home</span>'
            f"</a></li>"
        ]

        url_ancestors, ancestor_docnames = _resolve_subsite_url_ancestors(
            rel_path=rel_path,
            outdir_path=outdir_path,
            env=env,
            root_doc=root_doc,
            parent_map=parent_map,
            all_known_docs=all_known_docs,
        )
        for anc_title, anc_rel_href in url_ancestors:
            breadcrumbs_parts.append(
                '<li class="md3-breadcrumbs__separator" aria-hidden="true">/</li>'
                f'<li class="md3-breadcrumbs__item"><a class="md3-breadcrumbs__link" href="{html.escape(root_prefix + anc_rel_href)}">{html.escape(anc_title)}</a></li>'
            )

        if subsite_type == "doxygen":
            is_subsite_root = rel_path.name == "index.html"
            if is_subsite_root:
                breadcrumbs_parts.append(
                    '<li class="md3-breadcrumbs__separator" aria-hidden="true">/</li>'
                    '<li class="md3-breadcrumbs__item"><span class="md3-breadcrumbs__current" aria-current="page">C++ API</span></li>'
                )
            else:
                breadcrumbs_parts.append(
                    '<li class="md3-breadcrumbs__separator" aria-hidden="true">/</li>'
                    '<li class="md3-breadcrumbs__item"><a class="md3-breadcrumbs__link" href="index.html">C++ API</a></li>'
                )
                # Include Doxygen parent module groups from .ingroups (if any, excluding root modules.html/index.html)
                m_ingroups = re.search(r'<div class="ingroups"[^>]*>([\s\S]*?)</div>', text)
                if m_ingroups:
                    for g_href, g_title in re.findall(
                        r'<a\s+class="el"\s+href="([^"]+)"[^>]*>([^<]+)</a>',
                        m_ingroups.group(1),
                    ):
                        clean_href = g_href.lstrip("./")
                        if clean_href not in ("modules.html", "index.html"):
                            breadcrumbs_parts.append(
                                '<li class="md3-breadcrumbs__separator" aria-hidden="true">/</li>'
                                f'<li class="md3-breadcrumbs__item"><a class="md3-breadcrumbs__link" href="{html.escape(clean_href)}">{html.escape(g_title.strip())}</a></li>'
                            )
                breadcrumbs_parts.append(
                    '<li class="md3-breadcrumbs__separator" aria-hidden="true">/</li>'
                    f'<li class="md3-breadcrumbs__item"><span class="md3-breadcrumbs__current" aria-current="page">{html.escape(page_title)}</span></li>'
                )
        elif subsite_type == "rustdoc":
            is_subsite_root = rel_posix in (rustdoc_root_rel, "rustdoc/index.html", "rustdoc/pw_bytes/index.html")
            if is_subsite_root:
                breadcrumbs_parts.append(
                    '<li class="md3-breadcrumbs__separator" aria-hidden="true">/</li>'
                    '<li class="md3-breadcrumbs__item"><span class="md3-breadcrumbs__current" aria-current="page">Rust API</span></li>'
                )
            else:
                rust_api_href = f"{root_prefix}{rustdoc_root_rel}"
                breadcrumbs_parts.append(
                    '<li class="md3-breadcrumbs__separator" aria-hidden="true">/</li>'
                    f'<li class="md3-breadcrumbs__item"><a class="md3-breadcrumbs__link" href="{html.escape(rust_api_href)}">Rust API</a></li>'
                    '<li class="md3-breadcrumbs__separator" aria-hidden="true">/</li>'
                    f'<li class="md3-breadcrumbs__item"><span class="md3-breadcrumbs__current" aria-current="page">{html.escape(page_title)}</span></li>'
                )
        else:
            breadcrumbs_parts.append(
                '<li class="md3-breadcrumbs__separator" aria-hidden="true">/</li>'
                f'<li class="md3-breadcrumbs__item"><span class="md3-breadcrumbs__current" aria-current="page">{html.escape(page_title)}</span></li>'
            )

        header_html = _build_universal_header_html(
            project=project,
            root_doc=root_doc,
            root_prefix=root_prefix,
            site_root_attr=site_root_attr,
            subsite_type=subsite_type,
            skip_target=skip_target,
            logo_rel=logo_rel,
            source_url=source_url,
            source_label=source_label,
            raw_tabs=raw_tabs,
            breadcrumbs_items_html="".join(breadcrumbs_parts),
            ancestor_docnames=ancestor_docnames,
        )

        # Ensure <html> carries data-content_root (and data-baseurl if configured)
        def _patch_html_tag(match):
            tag = match.group(0)
            if "data-content_root=" not in tag:
                tag = tag[:-1] + f' data-content_root="{html.escape(root_prefix)}">'
            if baseurl and "data-baseurl=" not in tag:
                tag = tag[:-1] + f' data-baseurl="{html.escape(baseurl)}">'
            return tag

        text = re.sub(r"<html\b[^>]*>", _patch_html_tag, text, count=1, flags=re.IGNORECASE)

        # Inject MD3 theme bootstrap, app.css, and app.js into <head>
        head_injection = (
            f"{_THEME_BOOTSTRAP_SCRIPT}\n"
            f'<link rel="stylesheet" href="{html.escape(root_prefix)}_static/app.css" type="text/css" />\n'
            f'<script src="{html.escape(root_prefix)}_static/app.js" data-pagefind-js="{html.escape(root_prefix)}search/pagefind.js" type="module"></script>\n'
        )
        if "_static/app.css" not in text and "</head>" in text:
            text = text.replace("</head>", f"{head_injection}</head>", 1)

        # Add data-pagefind-body to subsite main content container and data-pagefind-ignore to excluded chrome
        for ignored_attr in (
            'id="navrow1"',
            'id="Loading"',
            'id="Searching"',
            'id="NoMatches"',
            'id="side-nav"',
            'id="copy-path"',
            'class="anchor"',
            'class="footer"',
            'class="doc-anchor"',
            'class="hideme"',
            'class="skip-main-content"',
        ):
            if ignored_attr in text:
                text = text.replace(ignored_attr, f'{ignored_attr} data-pagefind-ignore="all"')

        if subsite_type == "doxygen":
            if 'id="doc-content"' in text and "data-pagefind-body" not in text:
                text = text.replace('id="doc-content"', 'id="doc-content" data-pagefind-body', 1)
            elif 'class="contents"' in text and "data-pagefind-body" not in text:
                text = text.replace('class="contents"', 'class="contents" data-pagefind-body', 1)
        elif subsite_type == "rustdoc":
            is_rustdoc_src = bool(re.search(r'<body\b[^>]*\bclass="[^"]*\bsrc\b', text))
            if is_rustdoc_src:
                text = re.sub(
                    r"(<body\b[^>]*)(>)",
                    r'\1 data-pagefind-ignore="all"\2',
                    text,
                    count=1,
                    flags=re.IGNORECASE,
                )
            elif 'id="main-content"' in text and "data-pagefind-body" not in text:
                text = text.replace('id="main-content"', 'id="main-content" data-pagefind-body', 1)

        text = text.replace("<!-- md3-sentinel -->", header_html).replace("<!-- pw-sentinel -->", header_html)
        try:
            html_file.write_text(text, encoding="utf-8")
        except OSError:
            pass


async def _run_pagefind(outdir: str):
    from pagefind.index import IndexConfig, PagefindIndex

    heading_re = re.compile(
        r'(<h([1-6])(?![^>]*\bid=)[^>]*>)(.*?<a\s+class="headerlink"\s+href="#([^"]+)")',
        re.DOTALL,
    )
    outdir_path = Path(outdir)
    originals = {}
    for html_file in outdir_path.rglob("*.html"):
        try:
            text = html_file.read_text(encoding="utf-8")
            patched = heading_re.sub(
                lambda m: f'{m.group(1)[:-1]} id="{m.group(4)}">{m.group(3)}',
                text,
            )
            if patched != text:
                originals[html_file] = text
                html_file.write_text(patched, encoding="utf-8")
        except OSError:
            pass

    try:
        config = IndexConfig(
            exclude_selectors=[
                # Sphinx & MD3 chrome
                ".headerlink",
                ".md3-skip-link",
                ".md3-universal-header",
                "md3-top-app-bar",
                "md3-nav-tabs",
                "md3-sidebar",
                "md3-toc",
                ".md3-toc-mobile-wrapper",
                "md3-search",
                "md3-theme-toggle",
                "md3-copy-button",
                ".md3-breadcrumbs",
                ".md3-pagination",
                ".md3-footer",
                # Doxygen chrome & non-content elements
                ".anchor",
                ".footer",
                "#navrow1",
                "#Loading",
                "#Searching",
                "#NoMatches",
                # Rustdoc chrome & source view pages
                ".doc-anchor",
                ".hideme",
                ".main-heading .sub-heading .src",
                ".skip-main-content",
                "#copy-path",
                "body.rustdoc.src",
            ],
            verbose=False,
            keep_index_url=True,
            output_path=f"{outdir}/search",
            force_language="en",
        )
        async with PagefindIndex(config=config) as index:
            await index.add_directory(outdir)
    finally:
        for html_file, orig_text in originals.items():
            try:
                html_file.write_text(orig_text, encoding="utf-8")
            except OSError:
                pass


def generate_pagefind_index(app, exception) -> None:
    """Postprocesses external subsite headers and generates the Pagefind full-site search index."""
    if exception is not None or getattr(app.builder, "format", None) != "html":
        return
    postprocess_universal_header(app, exception)
    outdir = str(app.outdir)
    try:
        asyncio.get_running_loop()
        has_running_loop = True
    except RuntimeError:
        has_running_loop = False

    if has_running_loop:
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as pool:
            pool.submit(lambda: asyncio.run(_run_pagefind(outdir))).result()
    else:
        asyncio.run(_run_pagefind(outdir))


def setup(app):
    theme_dir = Path(__file__).resolve().parent
    app.add_html_theme("md3", theme_dir)
    app.add_html_theme("material3", theme_dir)
    app.connect("config-inited", add_components_static_path)
    app.connect("html-page-context", setup_navigation_context)
    app.connect("build-finished", generate_pagefind_index)
    return {
        "version": "0.1.0",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
