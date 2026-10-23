export class Md3Tabs extends HTMLElement {
  connectedCallback() {
    const tabs = Array.from(this.querySelectorAll('a'));
    if (tabs.length === 0) return;

    this.addEventListener('keydown', (e) => {
      const idx = tabs.indexOf(document.activeElement);
      if (idx === -1) return;

      let next = -1;
      if (e.key === 'ArrowRight') {
        next = (idx + 1) % tabs.length;
      } else if (e.key === 'ArrowLeft') {
        next = (idx - 1 + tabs.length) % tabs.length;
      } else if (e.key === 'Home') {
        next = 0;
      } else if (e.key === 'End') {
        next = tabs.length - 1;
      }

      if (next !== -1) {
        e.preventDefault();
        tabs[next].focus();
      }
    });
  }
}

customElements.define('md3-tabs', Md3Tabs);
