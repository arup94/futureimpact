/**
 * Featured Products Interactive Module
 * Provides subtle interactive enhancements for the botanical showcase cards.
 */

export class FeaturedProductsManager {
  constructor(sectionSelector = '#featured-products') {
    this.section = document.querySelector(sectionSelector);
    this.cards = this.section ? this.section.querySelectorAll('.bento-card') : [];
  }

  /**
   * Initializes event listeners and accessibility attributes.
   */
  init() {
    if (!this.section || this.cards.length === 0) {
      return false;
    }

    this.bindHoverParallax();
    return true;
  }

  /**
   * Subtle mouse movement tilt for enhanced luxury feel on hover.
   */
  bindHoverParallax() {
    this.cards.forEach((card) => {
      card.addEventListener('pointerenter', () => {
        card.style.willChange = 'transform, box-shadow';
      });

      card.addEventListener('pointerleave', () => {
        card.style.willChange = 'auto';
      });
    });
  }

  /**
   * Returns list of configured product names in the section.
   */
  getProductNames() {
    const titles = this.section ? this.section.querySelectorAll('.bento-title, .bento-side-title, .bento-bottom-title') : [];
    return Array.from(titles).map(el => el.textContent.trim());
  }
}
