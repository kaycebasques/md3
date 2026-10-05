import unittest
from harness import SphinxTestBase, md3_conformance


class TestMd3UniversalHeader(SphinxTestBase):
    """Verifies Universal Header postprocessing across Sphinx, Doxygen, and Rustdoc subsites,
    including cross-subsite theme synchronization, universal breadcrumbs, mobile drawer
    toggling, skip-to-main-content focus transfer, Pagefind subsite indexing/exclusions,
    and local/staging URL rewriting.
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        conf_content = """
            project = "Pigweed"
            extensions = ["md3"]
            html_theme = "md3"
            html_baseurl = "https://pigweed.dev/"
            html_extra_path = ["extra"]
            html_theme_options = {
                "source_url": "https://cs.opensource.google/pigweed/pigweed/",
                "source_label": "Pigweed source code",
            }
        """
        index_content = """
            =======
            Pigweed
            =======

            Welcome to Pigweed documentation.

            .. raw:: html

               <p><a id="prod-rewrite-link" href="https://pigweed.dev/docs/concepts/index.html">Concepts Prod Link</a></p>

            .. toctree::
               :maxdepth: 2

               docs/concepts/index
               api/index
        """
        extra_files = {
            "docs/concepts/index.rst": """
                ========
                Concepts
                ========

                Core Pigweed concepts.

                .. toctree::
                   :maxdepth: 2

                   nested/leaf
            """,
            "docs/concepts/nested/leaf.rst": """
                =========
                Leaf Page
                =========

                Deeply nested concept page.
            """,
            "api/index.rst": """
                =========
                Reference
                =========

                API Reference overview.
            """,
            "extra/api/cc/index.html": """<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8" />
  <title>Pigweed: Main Page</title>
  <style>
    body { margin: 0; }
    #side-nav { position: relative; width: 250px; float: left; }
    #nav-tree { overflow: auto; }
    #nav-tree .item { margin: 0; padding: 1px 0; display: block; white-space: nowrap; }
    #nav-tree .arrow { display: inline-block; width: 16px; height: 22px; cursor: pointer; user-select: none; }
    #nav-tree .label { display: inline; }
    #doc-content { overflow: auto; display: block; padding: 0; }
  </style>
</head>
<body>
<!-- pw-sentinel -->
<div id="top">
  <div id="navrow1" class="tabs">excludednavrowalpha</div>
</div>
<div id="side-nav" class="ui-resizable side-nav-resizable">
  <div id="nav-tree">
    <div id="nav-tree-contents">
      <div class="item selected"><span class="arrow" style="padding-left: 0px;">▼</span><span class="label"><a href="index.html">Main Page</a></span></div>
    </div>
  </div>
</div>
<div id="doc-content">
  <div class="header">
    <div class="headertitle"><div class="title">Main Page</div></div>
  </div>
  <div class="contents">
    <p>DoxygenRootOverviewToken</p>
    <div id="Loading">excludedloadingbeta</div>
    <div id="Searching">excludedsearchingdelta</div>
    <div id="NoMatches">excludednomatchesepsilon</div>
  </div>
</div>
</body>
</html>
""",
            "extra/api/cc/group__pw__bytes.html": """<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8" />
  <title>Pigweed: pw_bytes</title>
  <style>
    body { margin: 0; }
    #side-nav { position: relative; width: 250px; float: left; }
    #nav-tree { overflow: auto; }
    #nav-tree ul { list-style: none; margin: 0; padding: 0; }
    #nav-tree .item { margin: 0; padding: 1px 0; display: block; white-space: nowrap; }
    #nav-tree .arrow { display: inline-block; width: 16px; height: 22px; cursor: pointer; user-select: none; }
    #nav-tree .label { display: inline; }
    #doc-content { overflow: auto; display: block; padding: 0; }
  </style>
</head>
<body>
<!-- md3-sentinel -->
<div id="top">
  <div id="navrow1" class="tabs">excludednavrowalpha</div>
</div>
<div id="side-nav" class="ui-resizable side-nav-resizable">
  <div id="nav-tree">
    <div id="nav-tree-contents">
      <ul id="nav-tree-root">
        <li>
          <div class="item"><a href="javascript:void(0)" class="arrow-toggle" onclick="const ul = this.closest('li').querySelector('ul'); const sp = this.querySelector('.arrow'); if (ul.style.display === 'none') { ul.style.display = 'block'; sp.textContent = '▼'; } else { ul.style.display = 'none'; sp.textContent = '►'; }"><span class="arrow" style="padding-left: 0px;">▼</span></a><span class="label"><a href="index.html">Main Page</a></span></div>
          <ul class="children_ul">
            <li>
              <div class="item selected" id="selected"><a href="javascript:void(0)" id="pw-bytes-arrow-toggle" class="arrow-toggle" onclick="const ul = this.closest('li').querySelector('ul'); const sp = this.querySelector('.arrow'); if (ul.style.display === 'none') { ul.style.display = 'block'; sp.textContent = '▼'; } else { ul.style.display = 'none'; sp.textContent = '►'; }"><span class="arrow" style="padding-left: 16px;">►</span></a><span class="label"><a id="pw-bytes-label-link" href="group__pw__bytes.html">pw_bytes</a></span></div>
              <ul id="pw-bytes-children" class="children_ul" style="display: none;">
                <li>
                  <div class="item"><span style="width: 48px; display: inline-block;">&#160;</span><span class="label"><a id="byte-builder-link" href="index.html">pw::ByteBuilder</a></span></div>
                </li>
              </ul>
            </li>
          </ul>
        </li>
      </ul>
    </div>
  </div>
</div>
<div id="doc-content">
  <div class="header">
    <div class="headertitle"><div class="title">pw_bytes<div class="ingroups"><a class="el" href="modules.html">Modules</a></div></div></div>
  </div>
  <div class="contents">
    <p>DoxygenByteBuilderUniqueToken for manipulating byte arrays in C++.</p>
    <a class="anchor" id="details">excludedanchorzeta</a>
  </div>
</div>
</body>
</html>
""",
            "extra/rustdoc/pw_bytes/index.html": """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <title>pw_bytes - Rust</title>
  <style>
    body.rustdoc { display: flex; flex-direction: row; flex-wrap: nowrap; margin: 0; }
    body.rustdoc > nav.sidebar { flex: 0 0 200px; width: 200px; overflow-y: scroll; position: sticky; height: 100vh; top: 0; left: 0; }
    body.rustdoc > main { position: relative; flex-grow: 1; padding: 10px 15px 40px 45px; min-width: 0; }
  </style>
</head>
<body class="rustdoc mod crate">
<!-- pw-sentinel -->
<a class="skip-main-content" href="#main-content">Skip to main content</a>
<rustdoc-topbar><h2>pw_bytes</h2></rustdoc-topbar>
<nav class="sidebar">
  <div class="sidebar-crate"><h2><a href="../pw_bytes/index.html">pw_bytes</a></h2></div>
  <div class="sidebar-elems"><a class="current" href="index.html">pw_bytes</a><a id="status-crate-link" href="../pw_status/index.html">pw_status</a></div>
</nav>
<div class="sidebar-resizer"></div>
<main>
  <div class="width-limiter">
    <section id="main-content" class="content">
      <div class="main-heading">
        <h1>Crate <span>pw_bytes</span>&nbsp;<button id="copy-path" title="Copy item path">Copy item path</button></h1>
      </div>
      <p>RustdocBytesCrateUniqueToken for zero-overhead byte slices in Rust.</p>
      <a class="doc-anchor" href="#main-content">§</a>
    </section>
  </div>
</main>
</body>
</html>
""",
            "extra/rustdoc/pw_status/index.html": """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <title>pw_status - Rust</title>
  <style>
    body.rustdoc { display: flex; flex-direction: row; flex-wrap: nowrap; margin: 0; }
    body.rustdoc > nav.sidebar { flex: 0 0 200px; width: 200px; overflow-y: scroll; position: sticky; height: 100vh; top: 0; left: 0; }
    body.rustdoc > main { position: relative; flex-grow: 1; padding: 10px 15px 40px 45px; min-width: 0; }
  </style>
</head>
<body class="rustdoc mod crate">
<!-- md3-sentinel -->
<rustdoc-topbar><h2>pw_status</h2></rustdoc-topbar>
<nav class="sidebar">
  <div class="sidebar-crate"><h2><a href="../pw_status/index.html">pw_status</a></h2></div>
  <div class="sidebar-elems"><a class="current" href="index.html">pw_status</a></div>
</nav>
<div class="sidebar-resizer"></div>
<main>
  <div class="width-limiter">
    <section id="main-content" class="content">
      <div class="main-heading">
        <h1>Crate <span>pw_status</span>&nbsp;<button id="copy-path" title="Copy item path">Copy item path</button></h1>
      </div>
      <p>RustdocStatusCrateUniqueToken status codes for Rust.</p>
      <div>
        <label for="theme-ayu">Ayu</label>
      </div>
    </section>
  </div>
</main>
</body>
</html>
""",
            "extra/rustdoc/src/pw_bytes/lib.rs.html": """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <title>lib.rs - source</title>
  <style>
    body.rustdoc { display: flex; flex-direction: row; flex-wrap: nowrap; margin: 0; }
    body.rustdoc.src > nav.sidebar { flex: 0 0 50px; width: 50px; position: sticky; height: 100vh; top: 0; left: 0; }
    html.src-sidebar-expanded body.rustdoc.src > nav.sidebar { flex-basis: 300px; width: 300px; }
    body.rustdoc > main { position: relative; flex-grow: 1; padding: 10px 15px 40px 45px; min-width: 0; }
    #sidebar-button { position: fixed; left: 10px; top: 10px; z-index: 10; }
  </style>
</head>
<body class="rustdoc src">
<!-- pw-sentinel -->
<nav class="sidebar"><div id="src-sidebar"></div></nav>
<div id="sidebar-button"><a href="javascript:void(0)" title="Expand sidebar" onclick="document.documentElement.classList.toggle('src-sidebar-expanded')">☰</a></div>
<main>
  <section id="main-content" class="content">
    <pre class="rust"><code>pub fn excludedsrcviewgamma() {}</code></pre>
  </section>
</main>
</body>
</html>
""",
        }
        outdir = cls.build_docs(
            conf_content,
            index_content,
            extra_files=extra_files,
            outdir_name="universal_header_out",
        )
        cls.url = cls.start_server(outdir)

    @md3_conformance(spec_key="COMPONENTS_UNIVERSAL_HEADER")
    def test_universal_header_injected_into_doxygen_and_rustdoc_subsites(self):
        """Verifies that postprocess_universal_header replaces sentinels in Doxygen and Rustdoc pages."""
        with self.run_playwright(viewport={"width": 1280, "height": 800}) as page:
            for rel_url, expected_subsite in [
                ("api/cc/group__pw__bytes.html", "doxygen"),
                ("rustdoc/pw_status/index.html", "rustdoc"),
            ]:
                page.goto(f"{self.url}/{rel_url}")
                info = page.evaluate(
                    """() => {
                        const header = document.getElementById('md3-universal-header');
                        const appBar = document.querySelector('md3-top-app-bar');
                        const navTabs = document.querySelector('md3-nav-tabs');
                        const themeToggle = document.querySelector('md3-theme-toggle');
                        const searchTrigger = document.getElementById('search-bar-trigger');
                        const sourceLink = document.getElementById('md3-source-link');
                        const skipLink = document.getElementById('md3-skip-link');
                        return {
                            hasHeader: Boolean(header),
                            subsiteAttr: header ? header.getAttribute('data-subsite') : null,
                            contentRoot: document.documentElement.getAttribute('data-content_root'),
                            baseUrl: document.documentElement.getAttribute('data-baseurl'),
                            hasAppBar: Boolean(appBar),
                            appBarHeight: appBar ? appBar.getBoundingClientRect().height : 0,
                            hasNavTabs: Boolean(navTabs),
                            hasThemeToggle: Boolean(themeToggle),
                            hasSearchTrigger: Boolean(searchTrigger),
                            sourceHref: sourceLink ? sourceLink.getAttribute('href') : null,
                            skipHref: skipLink ? skipLink.getAttribute('href') : null,
                        };
                    }"""
                )
                self.assertTrue(info["hasHeader"], f"Missing #md3-universal-header on {rel_url}")
                self.assertEqual(info["subsiteAttr"], expected_subsite)
                self.assertEqual(info["contentRoot"], "../../")
                self.assertEqual(info["baseUrl"], "https://pigweed.dev/")
                self.assertTrue(info["hasAppBar"])
                self.assertEqual(info["appBarHeight"], 56)
                self.assertTrue(info["hasNavTabs"])
                self.assertTrue(info["hasThemeToggle"])
                self.assertTrue(info["hasSearchTrigger"])
                self.assertEqual(info["sourceHref"], "https://cs.opensource.google/pigweed/pigweed/")
                self.assertEqual(
                    info["skipHref"],
                    "#doc-content" if expected_subsite == "doxygen" else "#main-content",
                )

    @md3_conformance(spec_key="COMPONENTS_UNIVERSAL_BREADCRUMBS")
    def test_universal_breadcrumbs_across_sphinx_doxygen_and_rustdoc(self):
        """Verifies hierarchical breadcrumbs across nested Sphinx pages, Doxygen, and Rustdoc."""
        with self.run_playwright(viewport={"width": 1280, "height": 800}) as page:
            # 1. Deeply nested Sphinx page: Pigweed -> Concepts -> Leaf Page
            page.goto(f"{self.url}/docs/concepts/nested/leaf.html")
            sphinx_bc = page.evaluate(
                """() => {
                    const items = Array.from(document.querySelectorAll('.md3-breadcrumbs__item'));
                    return items.map((el) => ({
                        text: el.textContent.trim(),
                        href: el.querySelector('a')?.getAttribute('href') || null,
                        isCurrent: el.getAttribute('aria-current') === 'page' || Boolean(el.querySelector('[aria-current="page"]')),
                    }));
                }"""
            )
            self.assertEqual(len(sphinx_bc), 3)
            self.assertEqual(sphinx_bc[0]["text"], "Pigweed")
            self.assertEqual(sphinx_bc[1]["text"], "Concepts")
            self.assertEqual(sphinx_bc[2]["text"], "Leaf Page")
            self.assertTrue(sphinx_bc[2]["isCurrent"])

            # 2. Doxygen root page: Home -> Reference -> C++ API
            page.goto(f"{self.url}/api/cc/index.html")
            dox_root_bc = page.evaluate(
                """() => Array.from(document.querySelectorAll('#md3-subsite-breadcrumbs .md3-breadcrumbs__item')).map((el) => ({
                    text: el.textContent.trim(),
                    href: el.querySelector('a')?.getAttribute('href') || null,
                    isCurrent: Boolean(el.querySelector('[aria-current="page"]')),
                }))"""
            )
            self.assertEqual(len(dox_root_bc), 3)
            self.assertEqual(dox_root_bc[0]["text"], "Home")
            self.assertEqual(dox_root_bc[1]["text"], "Reference")
            self.assertTrue(dox_root_bc[1]["href"].endswith("api/index.html"))
            self.assertEqual(dox_root_bc[2]["text"], "C++ API")
            self.assertTrue(dox_root_bc[2]["isCurrent"])
            self.assertEqual(
                page.evaluate("document.querySelector('md3-nav-tabs .md3-nav-tabs__link.active')?.textContent?.trim()"),
                "Reference",
            )

            # 3. Doxygen subpage: Home -> Reference -> C++ API -> pw_bytes
            page.goto(f"{self.url}/api/cc/group__pw__bytes.html")
            dox_sub_bc = page.evaluate(
                """() => Array.from(document.querySelectorAll('#md3-subsite-breadcrumbs .md3-breadcrumbs__item')).map((el) => ({
                    text: el.textContent.trim(),
                    href: el.querySelector('a')?.getAttribute('href') || null,
                    isCurrent: Boolean(el.querySelector('[aria-current="page"]')),
                }))"""
            )
            self.assertEqual(len(dox_sub_bc), 4)
            self.assertEqual(dox_sub_bc[0]["text"], "Home")
            self.assertEqual(dox_sub_bc[1]["text"], "Reference")
            self.assertTrue(dox_sub_bc[1]["href"].endswith("api/index.html"))
            self.assertEqual(dox_sub_bc[2]["text"], "C++ API")
            self.assertEqual(dox_sub_bc[2]["href"], "index.html")
            self.assertEqual(dox_sub_bc[3]["text"], "pw_bytes")
            self.assertTrue(dox_sub_bc[3]["isCurrent"])
            self.assertEqual(
                page.evaluate("document.querySelector('md3-nav-tabs .md3-nav-tabs__link.active')?.textContent?.trim()"),
                "Reference",
            )

            # 4. Rustdoc root page: Home -> Rust API
            page.goto(f"{self.url}/rustdoc/pw_bytes/index.html")
            rust_root_bc = page.evaluate(
                """() => Array.from(document.querySelectorAll('#md3-subsite-breadcrumbs .md3-breadcrumbs__item')).map((el) => ({
                    text: el.textContent.trim(),
                    href: el.querySelector('a')?.getAttribute('href') || null,
                    isCurrent: Boolean(el.querySelector('[aria-current="page"]')),
                }))"""
            )
            self.assertEqual(len(rust_root_bc), 2)
            self.assertEqual(rust_root_bc[0]["text"], "Home")
            self.assertEqual(rust_root_bc[1]["text"], "Rust API")
            self.assertTrue(rust_root_bc[1]["isCurrent"])

            # 5. Rustdoc crate page: Home -> Rust API -> Crate pw_status
            page.goto(f"{self.url}/rustdoc/pw_status/index.html")
            rust_sub_bc = page.evaluate(
                """() => Array.from(document.querySelectorAll('#md3-subsite-breadcrumbs .md3-breadcrumbs__item')).map((el) => ({
                    text: el.textContent.trim(),
                    href: el.querySelector('a')?.getAttribute('href') || null,
                    isCurrent: Boolean(el.querySelector('[aria-current="page"]')),
                }))"""
            )
            self.assertEqual(len(rust_sub_bc), 3)
            self.assertEqual(rust_sub_bc[0]["text"], "Home")
            self.assertEqual(rust_sub_bc[1]["text"], "Rust API")
            self.assertTrue(rust_sub_bc[1]["href"].endswith("rustdoc/pw_bytes/index.html"))
            self.assertEqual(rust_sub_bc[2]["text"], "Crate pw_status")
            self.assertTrue(rust_sub_bc[2]["isCurrent"])

    @md3_conformance(spec_key="COMPONENTS_CROSS_SUBSITE_THEME_SYNC")
    def test_cross_subsite_theme_synchronization_and_storage_resilience(self):
        """Verifies theme persistence across Sphinx, Doxygen, and Rustdoc, legacy auto cleanup, and SecurityError safety."""
        with self.run_playwright(viewport={"width": 1280, "height": 800}, color_scheme="light") as page:
            page.goto(f"{self.url}/index.html")

            # Click theme toggle on Sphinx page to switch to dark mode
            page.locator("md3-theme-toggle #theme-menu-btn").click()
            state_sphinx = page.evaluate(
                """() => ({
                    themeAttr: document.documentElement.dataset.theme,
                    modeAttr: document.documentElement.dataset.mode,
                    hasDarkClass: document.documentElement.classList.contains('dark-mode'),
                    storedTheme: localStorage.getItem('theme'),
                    storedMode: localStorage.getItem('mode'),
                    rustdocTheme: localStorage.getItem('rustdoc-theme'),
                    rustdocSystem: localStorage.getItem('rustdoc-use-system-theme'),
                    pwBg: getComputedStyle(document.documentElement).getPropertyValue('--pw-color-bg').trim(),
                })"""
            )
            self.assertEqual(state_sphinx["themeAttr"], "dark")
            self.assertEqual(state_sphinx["modeAttr"], "dark")
            self.assertTrue(state_sphinx["hasDarkClass"])
            self.assertEqual(state_sphinx["storedTheme"], "dark")
            self.assertEqual(state_sphinx["storedMode"], "dark")
            self.assertEqual(state_sphinx["rustdocTheme"], "dark")
            self.assertEqual(state_sphinx["rustdocSystem"], "false")
            self.assertEqual(state_sphinx["pwBg"], "#131314")

            # Navigate to Doxygen subsite and verify dark mode persists automatically
            page.goto(f"{self.url}/api/cc/group__pw__bytes.html")
            state_doxygen = page.evaluate(
                """() => ({
                    themeAttr: document.documentElement.dataset.theme,
                    hasDarkClass: document.documentElement.classList.contains('dark-mode'),
                    bodyBg: getComputedStyle(document.body).backgroundColor,
                    oldNavRowDisplay: getComputedStyle(document.getElementById('navrow1')).display,
                })"""
            )
            self.assertEqual(state_doxygen["themeAttr"], "dark")
            self.assertTrue(state_doxygen["hasDarkClass"])
            self.assertEqual(state_doxygen["bodyBg"], "rgb(19, 19, 20)")
            self.assertEqual(state_doxygen["oldNavRowDisplay"], "none")

            # Navigate to Rustdoc subsite and verify dark mode and hidden ayu theme label
            page.goto(f"{self.url}/rustdoc/pw_status/index.html")
            state_rustdoc = page.evaluate(
                """() => ({
                    themeAttr: document.documentElement.dataset.theme,
                    hasDarkClass: document.documentElement.classList.contains('dark-mode'),
                    ayuDisplay: getComputedStyle(document.querySelector('label[for="theme-ayu"]')).display,
                    topbarDisplay: getComputedStyle(document.querySelector('rustdoc-topbar')).display,
                })"""
            )
            self.assertEqual(state_rustdoc["themeAttr"], "dark")
            self.assertTrue(state_rustdoc["hasDarkClass"])
            self.assertEqual(state_rustdoc["ayuDisplay"], "none")
            self.assertEqual(state_rustdoc["topbarDisplay"], "none")

            # Legacy 'auto' value in localStorage should be cleaned up on reload
            page.evaluate("localStorage.setItem('mode', 'auto'); localStorage.setItem('theme', 'auto');")
            page.reload()
            auto_cleaned = page.evaluate(
                """() => ({
                    mode: localStorage.getItem('mode'),
                    theme: localStorage.getItem('theme'),
                    rustdocSystem: localStorage.getItem('rustdoc-use-system-theme'),
                    resolvedTheme: document.documentElement.dataset.theme,
                })"""
            )
            self.assertIsNone(auto_cleaned["mode"])
            self.assertIsNone(auto_cleaned["theme"])
            self.assertEqual(auto_cleaned["rustdocSystem"], "true")
            self.assertEqual(auto_cleaned["resolvedTheme"], "light")

            # Verify SecurityError resilience when localStorage throws
            errors = []
            page.on("pageerror", lambda err: errors.append(str(err)))
            page.add_init_script(
                """
                Object.defineProperty(window, 'localStorage', {
                    get() { throw new DOMException('Blocked', 'SecurityError'); }
                });
                """
            )
            page.goto(f"{self.url}/index.html")
            page.locator("md3-theme-toggle #theme-menu-btn").click()
            self.assertEqual(page.evaluate("document.documentElement.dataset.theme"), "dark")
            self.assertEqual(errors, [])

    @md3_conformance(spec_key="COMPONENTS_UNIVERSAL_HEADER")
    def test_mobile_drawer_search_and_skip_link_across_subsites(self):
        """Verifies skip-to-main-content focus transfer and mobile drawer/search triggers on subsites."""
        with self.run_playwright(viewport={"width": 375, "height": 667}) as page:
            # 1. Skip link on Doxygen transfers focus to #doc-content
            page.goto(f"{self.url}/api/cc/group__pw__bytes.html")
            page.keyboard.press("Tab")
            self.assertEqual(page.evaluate("document.activeElement?.id"), "md3-skip-link")
            page.keyboard.press("Enter")
            self.assertEqual(page.evaluate("document.activeElement?.id"), "doc-content")

            # 2. Mobile drawer toggle on Doxygen opens/closes #side-nav with visible geometry
            page.locator("#drawer-toggle").click()
            dox_drawer = page.evaluate(
                """() => {
                    const sn = document.getElementById('side-nav');
                    const r = sn.getBoundingClientRect();
                    return {
                        hasClass: document.body.classList.contains('md3-doxygen-nav-open'),
                        display: getComputedStyle(sn).display,
                        left: Math.round(r.left),
                        top: Math.round(r.top),
                        width: Math.round(r.width),
                        height: Math.round(r.height),
                    };
                }"""
            )
            self.assertTrue(dox_drawer["hasClass"])
            self.assertEqual(dox_drawer["display"], "block")
            self.assertEqual(dox_drawer["left"], 0)
            self.assertEqual(dox_drawer["top"], 128)
            self.assertGreaterEqual(dox_drawer["width"], 200)
            self.assertGreater(dox_drawer["height"], 400)
            self.assertEqual(page.locator("#drawer-toggle").get_attribute("aria-expanded"), "true")
            page.keyboard.press("Escape")
            self.assertFalse(page.evaluate("document.body.classList.contains('md3-doxygen-nav-open')"))
            self.assertEqual(page.evaluate("getComputedStyle(document.getElementById('side-nav')).display"), "none")
            self.assertEqual(page.locator("#drawer-toggle").get_attribute("aria-expanded"), "false")

            # 3. Mobile search icon button opens <md3-search> dialog
            page.locator("#search-mobile-trigger").click()
            self.assertTrue(page.evaluate("document.getElementById('md3-search-dialog').open"))
            page.keyboard.press("Escape")
            self.assertFalse(page.evaluate("document.getElementById('md3-search-dialog').open"))

            # 4. Mobile drawer toggle on Rustdoc opens/closes nav.sidebar.shown with visible geometry
            page.goto(f"{self.url}/rustdoc/pw_bytes/index.html")
            page.locator("#drawer-toggle").click()
            page.wait_for_function(
                "() => Math.round(document.querySelector('nav.sidebar').getBoundingClientRect().left) === 0"
            )
            rust_drawer = page.evaluate(
                """() => {
                    const sb = document.querySelector('nav.sidebar');
                    const r = sb.getBoundingClientRect();
                    return {
                        shown: sb.classList.contains('shown'),
                        left: Math.round(r.left),
                        top: Math.round(r.top),
                        width: Math.round(r.width),
                        height: Math.round(r.height),
                    };
                }"""
            )
            self.assertTrue(rust_drawer["shown"])
            self.assertEqual(rust_drawer["left"], 0)
            self.assertEqual(rust_drawer["top"], 128)
            self.assertGreaterEqual(rust_drawer["width"], 200)
            self.assertGreater(rust_drawer["height"], 400)
            page.locator("#md3-backdrop").click(position={"x": 340, "y": 300})
            self.assertFalse(page.evaluate("document.querySelector('nav.sidebar').classList.contains('shown')"))

    @md3_conformance(spec_key="COMPONENTS_UNIVERSAL_HEADER")
    def test_doxygen_and_rustdoc_subsite_layout_geometry_and_navigation(self):
        """Verifies desktop flex/fixed layout geometry and interactive tree/sidebar navigation on Rustdoc and Doxygen."""
        with self.run_playwright(viewport={"width": 1280, "height": 800}) as page:
            # 1. Rustdoc crate page: fixed universal header does not participate in body.rustdoc flex row
            page.goto(f"{self.url}/rustdoc/pw_bytes/index.html")
            rust_geom = page.evaluate(
                """() => {
                    const hdr = document.getElementById('md3-universal-header').getBoundingClientRect();
                    const sb = document.querySelector('nav.sidebar').getBoundingClientRect();
                    const main = document.querySelector('main').getBoundingClientRect();
                    return {
                        hdrPos: getComputedStyle(document.getElementById('md3-universal-header')).position,
                        hdrTop: Math.round(hdr.top),
                        hdrHeight: Math.round(hdr.height),
                        hdrWidth: Math.round(hdr.width),
                        sbLeft: Math.round(sb.left),
                        sbTop: Math.round(sb.top),
                        sbWidth: Math.round(sb.width),
                        sbHeight: Math.round(sb.height),
                        mainLeft: Math.round(main.left),
                        mainTop: Math.round(main.top),
                        mainWidth: Math.round(main.width),
                    };
                }"""
            )
            self.assertEqual(rust_geom["hdrPos"], "fixed")
            self.assertEqual(rust_geom["hdrTop"], 0)
            self.assertEqual(rust_geom["hdrHeight"], 128)
            self.assertEqual(rust_geom["hdrWidth"], 1280)
            self.assertEqual(rust_geom["sbLeft"], 0)
            self.assertEqual(rust_geom["sbTop"], 128)
            self.assertIn(rust_geom["sbWidth"], (200, 201))
            self.assertEqual(rust_geom["sbHeight"], 672)
            self.assertIn(rust_geom["mainLeft"], (200, 201))
            self.assertEqual(rust_geom["mainTop"], 128)
            self.assertIn(rust_geom["mainWidth"], (1079, 1080))

            # 2. Rustdoc source page: #sidebar-button is positioned below the fixed header and expands nav.sidebar
            page.goto(f"{self.url}/rustdoc/src/pw_bytes/lib.rs.html")
            src_before = page.evaluate(
                """() => {
                    const btn = document.getElementById('sidebar-button').getBoundingClientRect();
                    const sb = document.querySelector('nav.sidebar').getBoundingClientRect();
                    return { btnTop: Math.round(btn.top), sbWidth: Math.round(sb.width) };
                }"""
            )
            self.assertGreaterEqual(src_before["btnTop"], 128)
            self.assertIn(src_before["sbWidth"], (50, 51))
            page.locator("#sidebar-button a").click()
            src_after = page.evaluate(
                """() => ({
                    expanded: document.documentElement.classList.contains('src-sidebar-expanded'),
                    sbWidth: Math.round(document.querySelector('nav.sidebar').getBoundingClientRect().width),
                })"""
            )
            self.assertTrue(src_after["expanded"])
            self.assertIn(src_after["sbWidth"], (300, 301))

            # 3. Doxygen desktop geometry, .arrow content-box non-overlap, and interactive tree expansion
            page.goto(f"{self.url}/api/cc/group__pw__bytes.html")
            dox_geom = page.evaluate(
                """() => {
                    const sn = document.getElementById('side-nav').getBoundingClientRect();
                    const dc = document.getElementById('doc-content').getBoundingClientRect();
                    const arrow = document.querySelector('#pw-bytes-arrow-toggle .arrow');
                    const labelLink = document.getElementById('pw-bytes-label-link');
                    const ar = arrow.getBoundingClientRect();
                    const lr = labelLink.getBoundingClientRect();
                    return {
                        snLeft: Math.round(sn.left),
                        snTop: Math.round(sn.top),
                        snWidth: Math.round(sn.width),
                        snHeight: Math.round(sn.height),
                        dcLeft: Math.round(dc.left),
                        dcTop: Math.round(dc.top),
                        dcWidth: Math.round(dc.width),
                        dcHeight: Math.round(dc.height),
                        arrowBoxSizing: getComputedStyle(arrow).boxSizing,
                        arrowWidth: Math.round(ar.width),
                        arrowRight: Math.round(ar.right),
                        labelLeft: Math.round(lr.left),
                        childrenDisplay: getComputedStyle(document.getElementById('pw-bytes-children')).display,
                    };
                }"""
            )
            self.assertEqual(dox_geom["snLeft"], 0)
            self.assertEqual(dox_geom["snTop"], 128)
            self.assertGreaterEqual(dox_geom["snWidth"], 250)
            self.assertEqual(dox_geom["snHeight"], 672)
            self.assertGreaterEqual(dox_geom["dcLeft"], 250)
            self.assertEqual(dox_geom["dcTop"], 128)
            self.assertGreater(dox_geom["dcWidth"], 900)
            self.assertEqual(dox_geom["dcHeight"], 672)
            self.assertEqual(dox_geom["arrowBoxSizing"], "content-box")
            # With padding-left: 16px and width: 16px in content-box, total width is 32px and never overlaps label
            self.assertEqual(dox_geom["arrowWidth"], 32)
            self.assertLessEqual(dox_geom["arrowRight"], dox_geom["labelLeft"] + 1)
            self.assertEqual(dox_geom["childrenDisplay"], "none")

            # Click the ► arrow toggle to expand children without navigating away
            page.locator("#pw-bytes-arrow-toggle").click()
            self.assertTrue(page.url.endswith("api/cc/group__pw__bytes.html"))
            self.assertEqual(
                page.evaluate("getComputedStyle(document.getElementById('pw-bytes-children')).display"),
                "block",
            )
            # Click the revealed child link to navigate to index.html
            page.locator("#byte-builder-link").click()
            page.wait_for_load_state("networkidle")
            self.assertTrue(page.url.endswith("api/cc/index.html"))

    @md3_conformance(spec_key="COMPONENTS_PAGEFIND_SEARCH")
    def test_pagefind_indexes_doxygen_and_rustdoc_while_excluding_chrome_and_src_pages(self):
        """Verifies cross-subsite Pagefind indexing for Doxygen and Rustdoc and exclusion of non-content selectors."""
        with self.run_playwright(viewport={"width": 1280, "height": 800}) as page:
            page.goto(f"{self.url}/index.html")
            page.locator("#search-bar-trigger").click()
            search_input = page.locator("#md3-search-input")

            # Doxygen content is indexed
            search_input.fill("DoxygenByteBuilderUniqueToken")
            page.wait_for_function(
                "() => document.querySelector('#md3-search-results')?.textContent?.includes('pw_bytes')"
            )

            # Rustdoc content is indexed
            search_input.fill("RustdocBytesCrateUniqueToken")
            page.wait_for_function(
                "() => document.querySelector('#md3-search-results')?.textContent?.includes('pw_bytes')"
            )

            # Excluded tokens (#navrow1, #Loading, body.rustdoc.src) return 0 results
            for excluded_token in [
                "excludednavrowalpha",
                "excludedloadingbeta",
                "excludedsrcviewgamma",
            ]:
                count = page.evaluate(
                    f"""async () => {{
                        const mod = await import('./_static/app.js');
                        const pf = await mod.loadPagefind();
                        const res = await pf.search({excluded_token!r});
                        return res.results.length;
                    }}"""
                )
                self.assertEqual(count, 0, f"Expected 0 Pagefind results for excluded token {excluded_token!r}")

    @md3_conformance(spec_key="COMPONENTS_UNIVERSAL_HEADER")
    def test_local_and_staging_url_rewriting(self):
        """Verifies that hardcoded https://pigweed.dev/ URLs are rewritten to local site root paths on non-prod hosts."""
        with self.run_playwright(viewport={"width": 1280, "height": 800}) as page:
            page.goto(f"{self.url}/index.html")
            rewritten_href = page.locator("#prod-rewrite-link").get_attribute("href")
            self.assertEqual(rewritten_href, "/docs/concepts/index.html")
            self.assertFalse(page.evaluate("window.isProductionDomain('127.0.0.1')"))
            self.assertTrue(page.evaluate("window.isProductionDomain('pigweed.dev')"))


if __name__ == "__main__":
    unittest.main()
