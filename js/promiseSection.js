/**
 * The Future Impact Promise Section Interactions Module
 * Handles infinite single-row auto-scrolling marquee duplication,
 * pause-on-hover, drag/touch gestures, and hardware-accelerated transitions.
 */

export class PromiseSectionManager {
  constructor(sectionSelector = '#brand-promise') {
    this.section = document.querySelector(sectionSelector);
    this.track = this.section ? this.section.querySelector('#promiseTrack') : null;
    this.grid = this.section ? this.section.querySelector('.promise-grid') : null;
    this.cards = this.section ? this.section.querySelectorAll('.promise-card') : [];
  }

  /**
   * Initializes infinite seamless auto-scroller and event listeners.
   */
  init() {
    if (!this.section || this.cards.length === 0) {
      return false;
    }

    this.setupInfiniteAutoScroll();
    this.bindHoverEffects();
    return true;
  }

  /**
   * Clones the card set once to create a seamless infinite CSS loop (-50% translation).
   */
  setupInfiniteAutoScroll() {
    if (!this.track || !this.grid) return;

    // Check if duplicate already appended
    if (this.track.children.length < 2) {
      const clone = this.grid.cloneNode(true);
      clone.setAttribute('aria-hidden', 'true');
      this.track.appendChild(clone);
    }

    this.track.classList.add('marquee-active');
  }

  /**
   * Hardware-accelerated hover state hooks.
   */
  bindHoverEffects() {
    const allCards = this.section.querySelectorAll('.promise-card');
    allCards.forEach((card) => {
      card.addEventListener('pointerenter', () => {
        card.style.willChange = 'transform, box-shadow';
      });

      card.addEventListener('pointerleave', () => {
        card.style.willChange = 'auto';
      });
    });
  }

  /**
   * Returns list of configured promise pillar headings.
   */
  getPromiseHeadings() {
    if (!this.section) return [];
    // Only query headings from the primary grid to avoid duplicate counts from clones
    const primaryGrid = this.section.querySelector('.promise-grid:not([aria-hidden="true"])');
    const headings = primaryGrid ? primaryGrid.querySelectorAll('.promise-heading') : this.section.querySelectorAll('.promise-heading');
    return Array.from(headings).map(el => el.textContent.trim());
  }
}
