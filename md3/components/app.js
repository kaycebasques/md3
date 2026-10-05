/**
 * Material Design 3 (MD3) Sphinx Theme Runtime Web Components
 */

// ---------------------------------------------------------------------------
// Theme Management & Safe Storage Helpers
// ---------------------------------------------------------------------------
export function safeGetStorage(key) {
  try {
    return localStorage.getItem(key);
  } catch (e) {
    return null;
  }
}

export function safeSetStorage(key, value) {
  try {
    localStorage.setItem(key, value);
  } catch (e) {}
}

export function safeRemoveStorage(key) {
  try {
    localStorage.removeItem(key);
  } catch (e) {}
}

export function cleanUpLegacyAutoTheme() {
  const mode = safeGetStorage('mode');
  const theme = safeGetStorage('theme');
  if (mode === 'auto' || theme === 'auto') {
    safeRemoveStorage('mode');
    safeRemoveStorage('theme');
    safeSetStorage('rustdoc-use-system-theme', 'true');
  }
}

export function getStoredTheme() {
  cleanUpLegacyAutoTheme();
  return safeGetStorage('theme') || safeGetStorage('mode');
}

export function setStoredTheme(theme) {
  safeSetStorage('theme', theme);
  safeSetStorage('mode', theme);
  safeSetStorage('rustdoc-theme', theme);
  safeSetStorage('rustdoc-use-system-theme', 'false');
  safeSetStorage('rustdoc-preferred-dark-theme', 'dark');
  safeSetStorage('rustdoc-preferred-light-theme', 'light');
}

export function getPreferredTheme() {
  const stored = getStoredTheme();
  if (stored === 'light' || stored === 'dark') {
    return stored;
  }
  return window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches
    ? 'dark'
    : 'light';
}

export function syncPygmentsTheme(theme) {
  const darkCss = document.getElementById('pygments_dark_css');
  if (darkCss) {
    darkCss.media = theme === 'dark' ? 'all' : 'not all';
  }
}

export function applyTheme(theme, persist = true) {
  const resolved = theme === 'dark' ? 'dark' : 'light';
  document.documentElement.dataset.theme = resolved;
  document.documentElement.dataset.mode = resolved;
  document.documentElement.classList.remove('light-mode', 'dark-mode', 'auto-mode');
  document.documentElement.classList.add(`${resolved}-mode`);
  if (typeof window !== 'undefined' && typeof window.DarkModeToggle === 'function') {
    try {
      window.DarkModeToggle.enableDarkMode(resolved === 'dark');
    } catch (e) {}
  }
  if (persist) {
    setStoredTheme(resolved);
  }
  syncPygmentsTheme(resolved);
  document.dispatchEvent(new CustomEvent('md3-theme-change', { detail: { theme: resolved } }));
}

export function toggleTheme() {
  const current = document.documentElement.dataset.theme || getPreferredTheme();
  const next = current === 'dark' ? 'light' : 'dark';
  applyTheme(next, true);
  return next;
}

// Keep OS prefers-color-scheme and bfcache restoration synchronized across pages
if (typeof window !== 'undefined') {
  if (window.matchMedia) {
    const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
    if (typeof mediaQuery.addEventListener === 'function') {
      mediaQuery.addEventListener('change', (e) => {
        if (!getStoredTheme()) {
          applyTheme(e.matches ? 'dark' : 'light', false);
        }
      });
    }
  }

  window.addEventListener('pageshow', (event) => {
    if (event.persisted) {
      applyTheme(getPreferredTheme(), false);
    }
  });
}

// ---------------------------------------------------------------------------
// Local & Staging URL Rewriting + Skip Link Focus Transfer
// ---------------------------------------------------------------------------
export function getSiteRootPath() {
  const contentRoot = document.documentElement.getAttribute('data-content_root');
  if (contentRoot) {
    try {
      return new URL(contentRoot, window.location.href).pathname;
    } catch (e) {}
  }
  const header = document.querySelector('#md3-universal-header, pw-header');
  if (header) {
    const siteRoot = header.getAttribute('data-site-root');
    if (siteRoot) {
      try {
        return new URL(`${siteRoot}/`, window.location.href).pathname;
      } catch (e) {}
    }
  }
  return '/';
}

export function isProductionDomain(hostname) {
  const rawBase = document.documentElement.getAttribute('data-baseurl') || 'https://pigweed.dev/';
  let prodHost = 'pigweed.dev';
  try {
    prodHost = new URL(rawBase).hostname || 'pigweed.dev';
  } catch (e) {}
  return hostname === prodHost || hostname === 'pigweed.dev';
}

export function rewriteUrls() {
  if (typeof window === 'undefined') return;
  if (isProductionDomain(window.location.hostname)) return;

  const rootPath = getSiteRootPath();
  const rawBase = document.documentElement.getAttribute('data-baseurl') || 'https://pigweed.dev/';
  const prefixes = new Set(['https://pigweed.dev/']);
  if (rawBase) {
    prefixes.add(rawBase.endsWith('/') ? rawBase : `${rawBase}/`);
  }

  for (const prefix of prefixes) {
    const links = document.querySelectorAll(`a[href^="${prefix}"]`);
    links.forEach((link) => {
      const href = link.getAttribute('href');
      if (href && href.startsWith(prefix)) {
        const subpath = href.slice(prefix.length);
        link.setAttribute('href', `${rootPath}${subpath}`);
      }
    });
  }
}

if (typeof window !== 'undefined') {
  window.getSiteRootPath = getSiteRootPath;
  window.isProductionDomain = isProductionDomain;
  window.rewriteUrls = rewriteUrls;
}

export function initSkipLink() {
  const skipLink = document.getElementById('md3-skip-link') || document.querySelector('.md3-skip-link');
  if (!skipLink || skipLink._md3Initialized) return;
  skipLink._md3Initialized = true;

  skipLink.addEventListener('click', () => {
    const href = skipLink.getAttribute('href');
    if (!href || !href.startsWith('#')) return;
    const target =
      document.getElementById(href.slice(1)) ||
      document.getElementById('main') ||
      document.getElementById('doc-content') ||
      document.getElementById('main-content');
    if (target) {
      target.setAttribute('tabindex', '-1');
      target.focus();
      target.addEventListener(
        'blur',
        () => {
          target.removeAttribute('tabindex');
        },
        { once: true }
      );
    }
  });
}

function escapeHtml(str) {
  return String(str ?? '').replace(/[&<>"']/g, (m) => ({
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    '"': '&quot;',
    "'": '&#39;',
  }[m]));
}

// ---------------------------------------------------------------------------
// Custom Elements
// ---------------------------------------------------------------------------

/**
 * <md3-theme-toggle>: Compact MD3 icon button that switches between light and dark themes.
 */
export class Md3ThemeToggle extends HTMLElement {
  connectedCallback() {
    if (this._initialized) return;
    this._initialized = true;

    const initialTheme = getPreferredTheme();
    applyTheme(initialTheme, Boolean(getStoredTheme()));
    this.updateAria();
    this.syncRadioInputs();

    const btn = this.querySelector('#theme-menu-btn');
    if (btn) {
      btn.addEventListener('click', (e) => {
        e.preventDefault();
        this.toggle();
      });
    }

    const menu = this.querySelector('#md3-theme-menu');
    if (menu) {
      const inputs = menu.querySelectorAll('input[name="theme"]');
      inputs.forEach((input) => {
        input.addEventListener('change', (e) => {
          const selected = e.target.value;
          applyTheme(selected, true);
          if (typeof menu.hidePopover === 'function') {
            try {
              menu.hidePopover();
            } catch (err) {}
          }
        });
      });
    }

    document.addEventListener('md3-theme-change', () => {
      this.updateAria();
      this.syncRadioInputs();
    });
  }

  syncRadioInputs() {
    const current = document.documentElement.dataset.theme || getPreferredTheme();
    const menu = this.querySelector('#md3-theme-menu');
    if (menu) {
      const inputs = menu.querySelectorAll('input[name="theme"]');
      inputs.forEach((input) => {
        input.checked = input.value === current;
      });
    }
  }

  toggle() {
    const next = toggleTheme();
    const menu = this.querySelector('#md3-theme-menu');
    if (menu && typeof menu.hidePopover === 'function') {
      try {
        menu.hidePopover();
      } catch (e) {}
    }
    this.syncRadioInputs();
    return next;
  }

  updateAria() {
    const current = document.documentElement.dataset.theme || getPreferredTheme();
    const pressed = current === 'dark' ? 'true' : 'false';
    const btn = this.querySelector('#theme-menu-btn');
    if (btn) {
      btn.setAttribute('aria-pressed', pressed);
    }
  }
}

/**
 * <md3-top-app-bar>: Sticky MD3 small top app bar managing navigation drawer trigger,
 * quick search bar trigger, universal subsite mobile drawers, and scroll elevation state.
 */
export class Md3TopAppBar extends HTMLElement {
  connectedCallback() {
    if (this._initialized) return;
    this._initialized = true;

    initSkipLink();
    rewriteUrls();
    this.initUniversalHeaderMetrics();
    this.initDrawerToggle();
    this.initSearchTriggers();
    this.initSubsiteActiveItemScroll();

    this._onScroll = () => {
      const scrolled = window.scrollY > 4;
      this.classList.toggle('scrolled', scrolled);
      this.dataset.scrolled = scrolled ? 'true' : 'false';
    };
    window.addEventListener('scroll', this._onScroll, { passive: true });
    this._onScroll();
  }

  initUniversalHeaderMetrics() {
    const universalHeader = this.closest('#md3-universal-header');
    if (!universalHeader) return;

    const updateHeight = () => {
      const h = universalHeader.offsetHeight;
      if (h > 0) {
        document.documentElement.style.setProperty('--md3-universal-header-height', `${h}px`);
      }
    };
    updateHeight();
    if (typeof ResizeObserver !== 'undefined') {
      this._headerResizeObserver = new ResizeObserver(updateHeight);
      this._headerResizeObserver.observe(universalHeader);
    }
  }

  initDrawerToggle() {
    const drawerToggle = this.querySelector('#drawer-toggle');
    if (!drawerToggle) return;

    const backdrop = document.getElementById('md3-backdrop');

    const closeSubsiteDrawers = () => {
      const rustSidebar = document.querySelector('nav.sidebar');
      if (rustSidebar && rustSidebar.classList.contains('shown')) {
        rustSidebar.classList.remove('shown');
      }
      if (document.body.classList.contains('src')) {
        document.documentElement.classList.remove('src-sidebar-expanded');
      }
      if (
        document.body.classList.contains('md3-doxygen-nav-open') ||
        document.body.classList.contains('pw-doxygen-nav-open')
      ) {
        document.body.classList.remove('md3-doxygen-nav-open', 'pw-doxygen-nav-open');
      }
      backdrop?.classList.remove('open');
      drawerToggle.setAttribute('aria-expanded', 'false');
    };

    const toggleDrawer = () => {
      const sidebar = document.querySelector('md3-sidebar, #md3-sidebar');
      if (sidebar && typeof sidebar.toggle === 'function') {
        sidebar.toggle();
        return;
      }

      const rustSidebar = document.querySelector('nav.sidebar');
      const doxygenSidebar = document.getElementById('side-nav');

      if (rustSidebar) {
        const isOpen = rustSidebar.classList.toggle('shown');
        if (document.body.classList.contains('src')) {
          document.documentElement.classList.toggle('src-sidebar-expanded', isOpen);
        }
        backdrop?.classList.toggle('open', isOpen);
        drawerToggle.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
      } else if (doxygenSidebar) {
        const isOpen = !document.body.classList.contains('md3-doxygen-nav-open');
        document.body.classList.toggle('md3-doxygen-nav-open', isOpen);
        document.body.classList.toggle('pw-doxygen-nav-open', isOpen);
        backdrop?.classList.toggle('open', isOpen);
        drawerToggle.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
      }
    };

    drawerToggle.addEventListener('click', (e) => {
      e.preventDefault();
      toggleDrawer();
    });

    if (!document.querySelector('md3-sidebar, #md3-sidebar')) {
      backdrop?.addEventListener('click', (e) => {
        e.preventDefault();
        closeSubsiteDrawers();
      });

      this._onSubsiteLinkClick = (e) => {
        if (window.innerWidth >= 840) return;
        const rustLink = e.target.closest('nav.sidebar a, .rustdoc .sidebar a');
        if (rustLink) {
          closeSubsiteDrawers();
          return;
        }
        const doxLink = e.target.closest('#side-nav a');
        if (doxLink) {
          const href = doxLink.getAttribute('href') || '';
          if (href && !href.startsWith('javascript:')) {
            closeSubsiteDrawers();
          }
        }
      };
      document.addEventListener('click', this._onSubsiteLinkClick);

      this._onSubsiteKeyDown = (e) => {
        if (e.key === 'Escape') {
          closeSubsiteDrawers();
        }
      };
      document.addEventListener('keydown', this._onSubsiteKeyDown);

      this._onSubsiteResize = () => {
        if (window.innerWidth >= 840) {
          closeSubsiteDrawers();
        }
      };
      window.addEventListener('resize', this._onSubsiteResize);
    }
  }

  initSearchTriggers() {
    const openSearch = () => {
      const searchEl = document.querySelector('md3-search');
      if (searchEl && typeof searchEl.open === 'function') {
        searchEl.open();
      }
    };

    const searchTrigger = this.querySelector('#search-bar-trigger');
    if (searchTrigger) {
      searchTrigger.addEventListener('click', openSearch);
      searchTrigger.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          openSearch();
        }
      });
    }

    const mobileTrigger = this.querySelector('#search-mobile-trigger');
    if (mobileTrigger) {
      mobileTrigger.addEventListener('click', (e) => {
        e.preventDefault();
        openSearch();
      });
    }
  }

  initSubsiteActiveItemScroll() {
    const centerInContainer = (container, item) => {
      if (!container || !item) return false;
      if (container.scrollHeight > container.clientHeight) {
        const containerRect = container.getBoundingClientRect();
        const itemRect = item.getBoundingClientRect();
        const offset = itemRect.top - containerRect.top + container.scrollTop;
        container.scrollTop = Math.max(0, offset - container.clientHeight / 2 + itemRect.height / 2);
      }
      return true;
    };

    const rustSidebar = document.querySelector('nav.sidebar');
    if (rustSidebar) {
      const activeItem = rustSidebar.querySelector('a.current, .current');
      centerInContainer(rustSidebar, activeItem);
    }

    const doxygenNavTree = document.getElementById('nav-tree');
    if (doxygenNavTree) {
      const scrollSelected = () => {
        const selected = doxygenNavTree.querySelector('.selected');
        return centerInContainer(doxygenNavTree, selected);
      };
      if (!scrollSelected() && typeof MutationObserver !== 'undefined') {
        const obs = new MutationObserver(() => {
          if (scrollSelected()) {
            obs.disconnect();
          }
        });
        obs.observe(doxygenNavTree, { childList: true, subtree: true });
      }
    }
  }

  disconnectedCallback() {
    if (this._onScroll) {
      window.removeEventListener('scroll', this._onScroll);
    }
    if (this._onSubsiteLinkClick) {
      document.removeEventListener('click', this._onSubsiteLinkClick);
    }
    if (this._onSubsiteKeyDown) {
      document.removeEventListener('keydown', this._onSubsiteKeyDown);
    }
    if (this._onSubsiteResize) {
      window.removeEventListener('resize', this._onSubsiteResize);
    }
    if (this._headerResizeObserver) {
      this._headerResizeObserver.disconnect();
    }
  }
}

/**
 * <md3-sidebar>: Responsive MD3 navigation drawer (persistent on desktop, modal drawer on mobile).
 */
export class Md3Sidebar extends HTMLElement {
  get isOpen() {
    return this.classList.contains('open');
  }

  open() {
    this._triggerEl = document.activeElement;
    const backdrop = document.getElementById('md3-backdrop');
    const toggle = document.getElementById('drawer-toggle');
    this.classList.add('open');
    this.dataset.open = 'true';
    backdrop?.classList.add('open');
    toggle?.setAttribute('aria-expanded', 'true');
  }

  close() {
    const backdrop = document.getElementById('md3-backdrop');
    const toggle = document.getElementById('drawer-toggle');
    this.classList.remove('open');
    this.dataset.open = 'false';
    backdrop?.classList.remove('open');
    toggle?.setAttribute('aria-expanded', 'false');
    if (typeof this.hidePopover === 'function') {
      try {
        if (this.matches(':popover-open')) {
          this.hidePopover();
        }
      } catch (e) {}
    }
    if (this._triggerEl && typeof this._triggerEl.focus === 'function') {
      this._triggerEl.focus();
    }
    this._triggerEl = null;
  }

  toggle() {
    if (this.isOpen) {
      this.close();
    } else {
      this.open();
    }
  }

  connectedCallback() {
    if (this._initialized) return;
    this._initialized = true;

    const backdrop = document.getElementById('md3-backdrop');
    backdrop?.addEventListener('click', (e) => {
      e.preventDefault();
      this.close();
    });

    const closeBtn = this.querySelector('#sidebar-close');
    closeBtn?.addEventListener('click', (e) => {
      e.preventDefault();
      this.close();
    });

    this._onKeyDown = (e) => {
      if (e.key === 'Escape' && this.isOpen) {
        this.close();
      }
    };
    document.addEventListener('keydown', this._onKeyDown);

    this.querySelectorAll('a').forEach((link) => {
      if (link.classList.contains('current')) {
        link.setAttribute('aria-current', 'page');
      }
    });

    this.initGraphNavigation();
    this.initFilter();
  }

  getNavGraph() {
    if (this._navGraph !== undefined) {
      return this._navGraph;
    }
    const scriptEl = this.querySelector('#md3-nav-graph-data');
    if (!scriptEl || !scriptEl.textContent) {
      this._navGraph = null;
      return null;
    }
    try {
      this._navGraph = JSON.parse(scriptEl.textContent);
    } catch (e) {
      this._navGraph = null;
    }
    return this._navGraph;
  }

  resolveDocUrl(docname) {
    const siteRoot = this.dataset.siteRoot || 'index.html';
    const rootDoc = this.dataset.rootDoc || 'index';
    const suffix = this.dataset.fileSuffix || '.html';
    const rootTarget = `${rootDoc}${suffix}`;
    let prefix = '';
    if (siteRoot.endsWith(rootTarget)) {
      prefix = siteRoot.slice(0, siteRoot.length - rootTarget.length);
    } else if (siteRoot.endsWith('/')) {
      prefix = siteRoot;
    }
    return `${prefix}${docname}${suffix}`;
  }

  initGraphNavigation() {
    const nav = this.querySelector('#sidebar-nav');
    if (!nav) return;

    nav.addEventListener('click', (e) => {
      const link = e.target.closest('a');
      if (!link) return;

      // Allow modified clicks (new tab / window) to proceed normally
      if (e.metaKey || e.ctrlKey || e.shiftKey || e.altKey || e.button !== 0) {
        return;
      }

      const targetLevel = link.getAttribute('data-nav-level');
      if (targetLevel && this.navigateToLevel(targetLevel)) {
        e.preventDefault();
        e.stopPropagation();
        return;
      }

      if (window.innerWidth < 840) {
        this.close();
      }
    });
  }

  navigateToLevel(levelDocname) {
    const graph = this.getNavGraph();
    const nav = this.querySelector('#sidebar-nav');
    if (!graph || !graph.nodes || !nav) return false;

    const node = graph.nodes[levelDocname];
    if (!node) return false;

    const rootDoc = graph.root_doc || this.dataset.rootDoc || 'index';
    const currentDoc = this.dataset.currentDoc || '';

    // Build the chain of ancestors for currentDoc so we can highlight active branch items
    const currentChain = new Set();
    let probe = currentDoc;
    const probeVisited = new Set();
    while (probe && !probeVisited.has(probe)) {
      probeVisited.add(probe);
      currentChain.add(probe);
      probe = graph.nodes[probe]?.parent || null;
    }

    // Build ancestors list for levelDocname
    const ancestorDocs = [];
    let curr = node.parent;
    const visited = new Set();
    while (curr && !visited.has(curr)) {
      visited.add(curr);
      ancestorDocs.push(curr);
      curr = graph.nodes[curr]?.parent || null;
    }
    ancestorDocs.reverse();

    let ancestorsHtml = '';
    if (levelDocname !== rootDoc || currentDoc !== rootDoc) {
      const ancItemsHtml = ancestorDocs
        .map((ancDoc) => {
          const ancNode = graph.nodes[ancDoc] || {};
          const ancTitle = ancNode.title || ancDoc;
          const ancUrl = this.resolveDocUrl(ancDoc);
          return `
            <li class="md3-sidebar__ancestor-item">
              <a class="md3-sidebar__back-link" href="${escapeHtml(ancUrl)}" data-nav-level="${escapeHtml(ancDoc)}">
                <svg class="md3-icon md3-sidebar__back-icon" viewBox="0 0 24 24" width="16" height="16" aria-hidden="true">
                  <path d="M20 11H7.83l5.59-5.59L12 4l-8 8 8 8 1.41-1.41L7.83 13H20v-2z"/>
                </svg>
                <span class="md3-nav-item__text">${escapeHtml(ancTitle)}</span>
              </a>
            </li>
          `;
        })
        .join('');

      const isSectionCurrent = levelDocname === currentDoc;
      const sectionUrl = isSectionCurrent ? '#' : this.resolveDocUrl(levelDocname);
      const sectionTitle = node.title || levelDocname;
      const backIconHtml =
        !isSectionCurrent && levelDocname !== rootDoc
          ? `<svg class="md3-icon md3-sidebar__back-icon" viewBox="0 0 24 24" width="16" height="16" aria-hidden="true">
              <path d="M20 11H7.83l5.59-5.59L12 4l-8 8 8 8 1.41-1.41L7.83 13H20v-2z"/>
            </svg>`
          : '';

      const sectionHeaderHtml = `
        <li class="md3-sidebar__section-item${isSectionCurrent ? ' current' : ''}">
          <a class="md3-sidebar__section-link${isSectionCurrent ? ' current' : ' md3-sidebar__back-link'}" href="${escapeHtml(sectionUrl)}"${isSectionCurrent ? ' aria-current="page"' : ''}>
            ${backIconHtml}
            <span class="md3-nav-item__text">${escapeHtml(sectionTitle)}</span>
          </a>
        </li>
      `;

      ancestorsHtml = `<ul class="md3-sidebar__ancestors">${ancItemsHtml}${sectionHeaderHtml}</ul>`;
    }

    let totalItems = 0;
    const groupsHtml = (node.groups || [])
      .map((group) => {
        const captionHtml = group.caption
          ? `<p class="caption" role="heading"><span class="caption-text">${escapeHtml(group.caption)}</span></p>`
          : '';
        const itemsHtml = (group.items || [])
          .map((item) => {
            totalItems += 1;
            const isCurrent = item.docname === currentDoc || currentChain.has(item.docname);
            const isExactPage = item.docname === currentDoc;
            const itemUrl = this.resolveDocUrl(item.docname);
            const hasChildren = Boolean(item.has_children);
            const liClasses = [
              'toctree-l1',
              isCurrent ? 'current' : '',
              hasChildren ? 'has-children' : '',
            ]
              .filter(Boolean)
              .join(' ');
            const aClasses = ['reference', 'internal', isCurrent ? 'current' : '']
              .filter(Boolean)
              .join(' ');
            const chevronHtml = hasChildren
              ? `<svg class="md3-icon md3-nav-item__chevron" viewBox="0 0 24 24" width="16" height="16" aria-hidden="true">
                  <path d="M10 6L8.59 7.41 13.17 12l-4.58 4.59L10 18l6-6z"/>
                </svg>`
              : '';
            return `
              <li class="${liClasses}">
                <a class="${aClasses}" href="${escapeHtml(itemUrl)}"${isExactPage ? ' aria-current="page"' : ''}${hasChildren ? ` data-nav-level="${escapeHtml(item.docname)}"` : ''}>
                  <span class="md3-nav-item__text">${escapeHtml(item.title)}</span>
                  ${chevronHtml}
                </a>
              </li>
            `;
          })
          .join('');
        return `${captionHtml}<ul class="md3-nav-list">${itemsHtml}</ul>`;
      })
      .join('');

    nav.dataset.activeLevel = levelDocname;
    nav.innerHTML = `${ancestorsHtml}${groupsHtml}`;

    const filterWrapper = this.querySelector('.md3-sidebar__filter');
    const filterInput = this.querySelector('#sidebar-filter-input');
    if (filterInput) {
      filterInput.value = '';
    }
    if (filterWrapper) {
      filterWrapper.hidden = totalItems < 8;
    }

    this.dispatchEvent(
      new CustomEvent('md3-sidebar-level-change', {
        detail: { level: levelDocname, totalItems },
      })
    );
    return true;
  }

  initFilter() {
    const filterInput = this.querySelector('#sidebar-filter-input');
    if (!filterInput) return;

    filterInput.addEventListener('input', () => {
      this.filterItems(filterInput.value);
    });
  }

  filterItems(rawQuery) {
    const query = (rawQuery || '').trim().toLowerCase();
    const nav = this.querySelector('#sidebar-nav');
    if (!nav) return;

    const lists = nav.querySelectorAll('ul.md3-nav-list');
    lists.forEach((list) => {
      let visibleCount = 0;
      const items = list.querySelectorAll('li');
      items.forEach((item) => {
        const text = (item.textContent || '').trim().toLowerCase();
        const matches = !query || text.includes(query);
        item.hidden = !matches;
        if (matches) {
          visibleCount += 1;
        }
      });

      const prev = list.previousElementSibling;
      if (prev && prev.classList.contains('caption')) {
        prev.hidden = Boolean(query && visibleCount === 0);
      }
    });
  }

  disconnectedCallback() {
    if (this._onKeyDown) {
      document.removeEventListener('keydown', this._onKeyDown);
    }
  }
}

/**
 * <md3-nav-tabs>: Top-level primary navigation tabs with keyboard arrow-key navigation.
 */
export class Md3NavTabs extends HTMLElement {
  connectedCallback() {
    if (this._initialized) return;
    this._initialized = true;

    const tabs = Array.from(this.querySelectorAll('.md3-nav-tabs__link'));
    if (tabs.length === 0) return;

    const activeTab = this.querySelector('.md3-nav-tabs__link.active');
    const navContainer = this.querySelector('.md3-nav-tabs__nav');
    if (activeTab && navContainer && navContainer.scrollWidth > navContainer.clientWidth) {
      const targetLeft =
        activeTab.offsetLeft - navContainer.clientWidth / 2 + activeTab.offsetWidth / 2;
      navContainer.scrollLeft = Math.max(0, targetLeft);
    }

    this.addEventListener('keydown', (e) => {
      const currentIdx = tabs.indexOf(document.activeElement);
      if (currentIdx === -1) return;

      let nextIdx = -1;
      if (e.key === 'ArrowRight') {
        nextIdx = (currentIdx + 1) % tabs.length;
      } else if (e.key === 'ArrowLeft') {
        nextIdx = (currentIdx - 1 + tabs.length) % tabs.length;
      } else if (e.key === 'Home') {
        nextIdx = 0;
      } else if (e.key === 'End') {
        nextIdx = tabs.length - 1;
      }

      if (nextIdx !== -1) {
        e.preventDefault();
        tabs[nextIdx].focus();
      }
    });
  }
}

/**
 * <md3-toc>: Right-column "On this page" table of contents with IntersectionObserver scrollspy.
 */
export class Md3Toc extends HTMLElement {
  connectedCallback() {
    if (this._initialized) return;
    this._initialized = true;

    this.initScrollspy();
    this.initBackToTop();
  }

  initScrollspy() {
    const tocNav = this.querySelector('#md3-toc-nav');
    const article = document.querySelector('.md3-article');
    if (!tocNav || !article) return;

    let tocList = tocNav.querySelector('ul');
    const headings = Array.from(article.querySelectorAll('h2, h3'));

    if ((!tocList || tocList.children.length === 0) && headings.length > 0) {
      tocList = document.createElement('ul');
      headings.forEach((h, idx) => {
        if (!h.id) {
          h.id = `heading-${idx}`;
        }
        const li = document.createElement('li');
        const a = document.createElement('a');
        a.href = `#${h.id}`;
        a.textContent = h.textContent.replace(/¶$/, '').trim();
        li.appendChild(a);
        tocList.appendChild(li);
      });
      tocNav.appendChild(tocList);
    }

    const links = Array.from(tocNav.querySelectorAll('a'));
    if (links.length === 0) return;

    // Set initial active state on first TOC link
    links[0].classList.add('active');

    this._observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            const id = entry.target.getAttribute('id');
            if (!id) return;
            links.forEach((link) => {
              const href = link.getAttribute('href');
              if (href === `#${id}` || href?.endsWith(`#${id}`)) {
                link.classList.add('active');
              } else {
                link.classList.remove('active');
              }
            });
          }
        });
      },
      { rootMargin: '-70px 0px -70% 0px' }
    );

    headings.forEach((h) => this._observer.observe(h));
  }

  initBackToTop() {
    const btn = this.querySelector('#back-to-top');
    if (!btn) return;
    btn.addEventListener('click', (e) => {
      e.preventDefault();
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

  disconnectedCallback() {
    if (this._observer) {
      this._observer.disconnect();
    }
  }
}

// ---------------------------------------------------------------------------
// Pagefind Full-Site Search Engine Loader & Renderer
// ---------------------------------------------------------------------------
let pagefindInstance = null;
let pagefindLoadPromise = null;

function getPagefindScriptUrl() {
  const scriptEl = document.querySelector('script[data-pagefind-js]');
  const raw = scriptEl?.getAttribute('data-pagefind-js');
  if (!raw) return null;
  try {
    return new URL(raw, window.location.href);
  } catch (e) {
    return null;
  }
}

export function resolvePagefindUrl(rawUrl) {
  if (!rawUrl) return '#';
  const scriptUrl = getPagefindScriptUrl();
  if (!scriptUrl) return rawUrl;
  try {
    const siteRootUrl = new URL('../', scriptUrl);
    const cleanRel = rawUrl.replace(/^\/+/, '');
    return new URL(cleanRel, siteRootUrl).href;
  } catch (e) {
    return rawUrl;
  }
}

export async function loadPagefind() {
  if (pagefindInstance) return pagefindInstance;
  if (pagefindLoadPromise) return pagefindLoadPromise;
  const scriptUrl = getPagefindScriptUrl();
  if (!scriptUrl) return null;

  pagefindLoadPromise = (async () => {
    try {
      const pf = await import(scriptUrl.href);
      if (typeof pf.init === 'function') {
        await pf.init();
      }
      pagefindInstance = pf;
      return pf;
    } catch (err) {
      pagefindLoadPromise = null;
      return null;
    }
  })();

  return pagefindLoadPromise;
}

function renderPagefindItemsHtml(items) {
  return items
    .map((data) => {
      const pageTitle = (data.meta && data.meta.title) || 'Documentation';
      const subResults = Array.isArray(data.sub_results) ? data.sub_results : [];
      const primarySub = subResults[0] || null;
      const primaryHref = resolvePagefindUrl(primarySub ? primarySub.url : data.url);
      const primarySectionTitle =
        primarySub && primarySub.title && primarySub.title !== pageTitle ? primarySub.title : '';
      const primaryExcerpt = (primarySub && primarySub.excerpt) || data.excerpt || '';

      let subLinksHtml = '';
      if (subResults.length > 1) {
        const chips = subResults
          .slice(0, 4)
          .map((sub) => {
            const subHref = resolvePagefindUrl(sub.url);
            const subTitle = sub.title || pageTitle;
            return `<a class="md3-search-sub-result-link" href="${escapeHtml(subHref)}">${escapeHtml(subTitle)}</a>`;
          })
          .join('');
        subLinksHtml = `<div class="md3-search-sub-results">${chips}</div>`;
      }

      return `
        <div class="md3-search-result-item">
          <a class="md3-search-result-main-link" href="${escapeHtml(primaryHref)}">
            <div class="md3-search-result-title">
              <span>${escapeHtml(pageTitle)}</span>
              ${primarySectionTitle ? `<span class="md3-search-result-section">› ${escapeHtml(primarySectionTitle)}</span>` : ''}
            </div>
            <div class="md3-search-result-snippet">${primaryExcerpt}</div>
          </a>
          ${subLinksHtml}
        </div>
      `;
    })
    .join('');
}

/**
 * <md3-search>: Modal quick-search dialog with keyboard shortcuts (Cmd+K / '/')
 * and Pagefind full-site search with instant local fallback.
 */
export class Md3Search extends HTMLElement {
  get dialog() {
    return this.querySelector('#md3-search-dialog');
  }

  get input() {
    return this.querySelector('#md3-search-input');
  }

  get resultsContainer() {
    return this.querySelector('#md3-search-results');
  }

  get isOpen() {
    return Boolean(this.dialog?.open);
  }

  open() {
    const dialog = this.dialog;
    if (!dialog) return;
    this._triggerEl = document.activeElement;
    loadPagefind();
    if (!dialog.open) {
      dialog.showModal();
    }
    this.input?.focus();
  }

  close() {
    const dialog = this.dialog;
    if (!dialog) return;
    if (dialog.open) {
      dialog.close();
    }
    if (this.input) {
      this.input.value = '';
    }
    if (this.resultsContainer) {
      this.resultsContainer.innerHTML =
        '<div class="md3-search-hint">Type a query to search documentation. Press <kbd class="md3-kbd-shortcut">ESC</kbd> to exit.</div>';
    }
    if (this._triggerEl && typeof this._triggerEl.focus === 'function') {
      this._triggerEl.focus();
    }
    this._triggerEl = null;
  }

  searchLocalArticle(query) {
    const matches = [];
    const seen = new Set();
    const article = document.querySelector('.md3-article');
    if (article) {
      const elements = article.querySelectorAll('h1, h2, h3, h4, p, li, td');
      elements.forEach((el) => {
        const text = el.textContent.replace(/¶$/, '').trim();
        if (text && text.toLowerCase().includes(query)) {
          let title = 'Document Section';
          let href = '#';
          const nearestHeading = el.matches('h1, h2, h3, h4')
            ? el
            : el.closest('section')?.querySelector('h1, h2, h3, h4') || el;
          if (nearestHeading.id) {
            href = `#${nearestHeading.id}`;
          } else if (nearestHeading.closest('section')?.id) {
            href = `#${nearestHeading.closest('section').id}`;
          }
          title = nearestHeading.textContent.replace(/¶$/, '').trim();

          const key = `${href}::${text.slice(0, 60)}`;
          if (!seen.has(key)) {
            seen.add(key);
            matches.push({
              title,
              snippet: text.length > 120 ? text.slice(0, 120) + '...' : text,
              href,
            });
          }
        }
      });
    }
    return matches;
  }

  attachResultCloseListeners(container) {
    container.querySelectorAll('a').forEach((link) => {
      link.addEventListener('click', () => this.close());
    });
  }

  search(rawQuery) {
    const resultsContainer = this.resultsContainer;
    if (!resultsContainer) return;

    this._searchSeq = (this._searchSeq || 0) + 1;
    const seq = this._searchSeq;

    const trimmed = (rawQuery || '').trim();
    const query = trimmed.toLowerCase();
    if (!query) {
      resultsContainer.innerHTML =
        '<div class="md3-search-hint">Type a query to search documentation. Press <kbd class="md3-kbd-shortcut">ESC</kbd> to exit.</div>';
      return;
    }

    // Immediate synchronous pass on current article so synchronous assertions have instant feedback
    const localMatches = this.searchLocalArticle(query);
    if (localMatches.length > 0) {
      const uniqueMatches = localMatches.slice(0, 8);
      resultsContainer.innerHTML = uniqueMatches
        .map(
          (m) => `
        <div class="md3-search-result-item">
          <a class="md3-search-result-main-link" href="${m.href}">
            <div class="md3-search-result-title">${escapeHtml(m.title)}</div>
            <div class="md3-search-result-snippet">${escapeHtml(m.snippet)}</div>
          </a>
        </div>
      `
        )
        .join('');
      this.attachResultCloseListeners(resultsContainer);
    } else {
      resultsContainer.innerHTML = `<div class="md3-search-hint">Searching documentation for "<strong>${escapeHtml(trimmed)}</strong>"...</div>`;
    }

    // Full-site Pagefind search
    this.searchWithPagefind(trimmed, seq, localMatches.length);
  }

  async searchWithPagefind(trimmedQuery, seq, localMatchCount) {
    const resultsContainer = this.resultsContainer;
    if (!resultsContainer) return;

    const pf = await loadPagefind();
    if (seq !== this._searchSeq) return;

    if (!pf) {
      if (localMatchCount === 0) {
        resultsContainer.innerHTML = `<div class="md3-search-hint">No results found for "<strong>${escapeHtml(trimmedQuery)}</strong>"</div>`;
      }
      return;
    }

    try {
      const searchResult = await pf.search(trimmedQuery);
      if (seq !== this._searchSeq) return;

      if (!searchResult || !searchResult.results || searchResult.results.length === 0) {
        if (localMatchCount === 0) {
          resultsContainer.innerHTML = `<div class="md3-search-hint">No results found for "<strong>${escapeHtml(trimmedQuery)}</strong>"</div>`;
        }
        return;
      }

      const items = await Promise.all(searchResult.results.slice(0, 10).map((r) => r.data()));
      if (seq !== this._searchSeq) return;

      resultsContainer.innerHTML = renderPagefindItemsHtml(items);
      this.attachResultCloseListeners(resultsContainer);
    } catch (err) {
      if (localMatchCount === 0 && seq === this._searchSeq) {
        resultsContainer.innerHTML = `<div class="md3-search-hint">No results found for "<strong>${escapeHtml(trimmedQuery)}</strong>"</div>`;
      }
    }
  }

  connectedCallback() {
    if (this._initialized) return;
    this._initialized = true;

    // Preload Pagefind index in background
    loadPagefind();

    const dialog = this.dialog;
    const closeBtn = this.querySelector('#md3-search-close');
    const input = this.input;

    closeBtn?.addEventListener('click', () => this.close());

    dialog?.addEventListener('click', (e) => {
      const container = dialog.querySelector('.md3-search-dialog__container');
      if (container && !container.contains(e.target)) {
        this.close();
      }
    });

    this._onKeyDown = (e) => {
      if (e.key === 'Escape' && this.isOpen) {
        e.preventDefault();
        this.close();
      } else if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'k') {
        e.preventDefault();
        this.isOpen ? this.close() : this.open();
      } else if (
        e.key === '/' &&
        !this.isOpen &&
        !['INPUT', 'TEXTAREA'].includes(document.activeElement?.tagName)
      ) {
        e.preventDefault();
        this.open();
      }
    };
    document.addEventListener('keydown', this._onKeyDown);

    input?.addEventListener('input', () => {
      this.search(input.value);
    });
  }

  disconnectedCallback() {
    if (this._onKeyDown) {
      document.removeEventListener('keydown', this._onKeyDown);
    }
  }
}

export function initSearchPage() {
  const searchPage = document.querySelector('.md3-search-page');
  if (!searchPage) return;

  const form = searchPage.querySelector('.md3-search-page-form');
  const input = searchPage.querySelector('#search-input');
  const resultsContainer = searchPage.querySelector('#search-results');
  if (!input || !resultsContainer) return;

  let searchSeq = 0;
  const runPageSearch = async (rawQuery) => {
    searchSeq += 1;
    const seq = searchSeq;
    const trimmed = (rawQuery || '').trim();
    if (!trimmed) {
      resultsContainer.innerHTML = '';
      return;
    }

    const pf = await loadPagefind();
    if (seq !== searchSeq) return;
    if (!pf) {
      resultsContainer.innerHTML = `<div class="md3-search-hint">No results found for "<strong>${escapeHtml(trimmed)}</strong>"</div>`;
      return;
    }

    const searchResult = await pf.search(trimmed);
    if (seq !== searchSeq) return;
    if (!searchResult || !searchResult.results || searchResult.results.length === 0) {
      resultsContainer.innerHTML = `<div class="md3-search-hint">No results found for "<strong>${escapeHtml(trimmed)}</strong>"</div>`;
      return;
    }

    const items = await Promise.all(searchResult.results.slice(0, 20).map((r) => r.data()));
    if (seq !== searchSeq) return;
    resultsContainer.innerHTML = renderPagefindItemsHtml(items);
  };

  form?.addEventListener('submit', (e) => {
    e.preventDefault();
    runPageSearch(input.value);
  });

  input.addEventListener('input', () => {
    runPageSearch(input.value);
  });

  try {
    const params = new URLSearchParams(window.location.search);
    const initialQuery = params.get('q');
    if (initialQuery) {
      input.value = initialQuery;
      runPageSearch(initialQuery);
    }
  } catch (e) {}
}

/**
 * <md3-copy-button>: Compact MD3 code block copy button with clipboard feedback.
 */
export class Md3CopyButton extends HTMLElement {
  connectedCallback() {
    if (this._initialized) return;
    this._initialized = true;

    this.classList.add('md3-code-copy-btn');
    if (!this.hasAttribute('role')) {
      this.setAttribute('role', 'button');
    }
    if (!this.hasAttribute('tabindex')) {
      this.setAttribute('tabindex', '0');
    }
    if (!this.hasAttribute('aria-label')) {
      this.setAttribute('aria-label', 'Copy code snippet');
    }
    if (!this.hasAttribute('title')) {
      this.setAttribute('title', this.getAttribute('aria-label') || 'Copy code snippet');
    }

    if (!this.querySelector('.copy-text')) {
      this.innerHTML = `
        <svg class="md3-icon" viewBox="0 0 24 24" width="14" height="14">
          <path d="M16 1H4c-1.1 0-2 .9-2 2v14h2V3h12V1zm3 4H8c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h11c1.1 0 2-.9 2-2V7c0-1.1-.9-2-2-2zm0 16H8V7h11v14z"/>
        </svg>
        <span class="copy-text">Copy</span>
      `;
    }

    this.addEventListener('click', () => this.copy());
    this.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        this.copy();
      }
    });
  }

  async copy() {
    const block = this.closest('div.highlight') || this.parentElement;
    const pre = block?.querySelector('pre');
    if (!pre) return;

    const codeText = pre.innerText || pre.textContent || '';
    try {
      if (navigator.clipboard && navigator.clipboard.writeText) {
        await navigator.clipboard.writeText(codeText);
      } else {
        throw new Error('Clipboard API not available');
      }
    } catch (err) {
      try {
        const textArea = document.createElement('textarea');
        textArea.value = codeText;
        textArea.style.position = 'fixed';
        textArea.style.opacity = '0';
        document.body.appendChild(textArea);
        textArea.select();
        document.execCommand('copy');
        document.body.removeChild(textArea);
      } catch (e) {}
    }

    this.classList.add('copied');
    const label = this.querySelector('.copy-text');
    if (label) label.textContent = 'Copied!';
    if (this._resetTimer) clearTimeout(this._resetTimer);
    this._resetTimer = setTimeout(() => {
      this.classList.remove('copied');
      if (label) label.textContent = 'Copy';
    }, 2000);
  }
}

export function initMobileToc() {
  const mobileMenu = document.getElementById('md3-toc-mobile-menu');
  if (!mobileMenu) return;

  mobileMenu.addEventListener('click', (e) => {
    const link = e.target.closest('a');
    if (link && typeof mobileMenu.hidePopover === 'function') {
      try {
        mobileMenu.hidePopover();
      } catch (err) {}
    }
  });
}

/**
 * <md3-app>: Root application container orchestrating theme state and code block upgrades.
 */
export class Md3App extends HTMLElement {
  connectedCallback() {
    const currentTheme = document.documentElement.dataset.theme || getPreferredTheme();
    syncPygmentsTheme(currentTheme);
    this.initCodeCopy();
    initMobileToc();
    initSearchPage();
  }

  initCodeCopy() {
    const codeBlocks = this.querySelectorAll('div.highlight');
    codeBlocks.forEach((block) => {
      if (block.querySelector('md3-copy-button, .md3-code-copy-btn')) return;
      const pre = block.querySelector('pre');
      if (!pre) return;

      const copyBtn = document.createElement('md3-copy-button');
      copyBtn.className = 'md3-code-copy-btn';
      block.appendChild(copyBtn);
    });
  }
}

// ---------------------------------------------------------------------------
// Register Web Components
// ---------------------------------------------------------------------------
const components = {
  'md3-app': Md3App,
  'md3-theme-toggle': Md3ThemeToggle,
  'md3-top-app-bar': Md3TopAppBar,
  'md3-nav-tabs': Md3NavTabs,
  'md3-sidebar': Md3Sidebar,
  'md3-toc': Md3Toc,
  'md3-search': Md3Search,
  'md3-copy-button': Md3CopyButton,
};

for (const [tag, cls] of Object.entries(components)) {
  if (!customElements.get(tag)) {
    customElements.define(tag, cls);
  }
}
