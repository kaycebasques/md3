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


async def _run_pagefind(outdir: str):
    import re
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
                ".headerlink",
                ".md3-skip-link",
                "md3-top-app-bar",
                "md3-nav-tabs",
                "md3-sidebar",
                "md3-toc",
                "md3-search",
                "md3-theme-toggle",
                "md3-copy-button",
                ".md3-breadcrumbs",
                ".md3-pagination",
                ".md3-footer",
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
    """Generates the Pagefind full-site search index after HTML build finishes."""
    if exception is not None or getattr(app.builder, "format", None) != "html":
        return
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
    app.add_html_theme("paz", theme_dir)
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
