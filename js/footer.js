/**
 * Site Footer Interactions Module
 * Handles formal query interactions, accessibility tags, and analytics hook points.
 */

export class FooterManager {
  constructor(footerSelector = '#site-footer') {
    this.footer = document.querySelector(footerSelector);
    this.queryBtn = document.querySelector('#btnQueryForm');
    this.socialButtons = this.footer ? this.footer.querySelectorAll('.social-icon-btn') : [];
  }

  /**
   * Initializes footer event listeners.
   */
  init() {
    if (!this.footer) {
      return false;
    }

    this.bindQueryButton();
    this.bindSocialButtons();
    return true;
  }

  /**
   * Smooth interaction handler for query button.
   */
  bindQueryButton() {
    if (!this.queryBtn) return;
    this.queryBtn.addEventListener('pointerenter', () => {
      this.queryBtn.style.willChange = 'transform, box-shadow';
    });
    this.queryBtn.addEventListener('pointerleave', () => {
      this.queryBtn.style.willChange = 'auto';
    });
  }

  /**
   * Ensures secure cross-origin openers on all external social media links.
   */
  bindSocialButtons() {
    this.socialButtons.forEach((btn) => {
      btn.setAttribute('rel', 'noopener noreferrer');
    });
  }
}
