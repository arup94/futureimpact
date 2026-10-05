import { CONFIG } from './config.js';
import { FrameLoader } from './frameLoader.js';
import { CanvasRenderer } from './canvasRenderer.js';
import { SandParticleEngine } from './sandAnimation.js';
import { ScrollTimeline } from './scrollTimeline.js';
import { FeaturedProductsManager } from './featuredProducts.js';
import { PromiseSectionManager } from './promiseSection.js';
import { FooterManager } from './footer.js';

/**
 * Main Application Orchestrator for Full-screen Frame Animation Hero
 */
class App {
  constructor() {
    this.canvas = document.querySelector(CONFIG.canvasSelector);
    this.sandCanvas = document.querySelector(CONFIG.sandCanvasSelector);
    this.scrollWrapper = document.querySelector(CONFIG.scrollWrapperSelector);
    
    this.glassCard = document.querySelector(CONFIG.glassCardSelector);
    this.subheading = document.querySelector(CONFIG.subheadingSelector);
    this.actions = document.querySelector(CONFIG.actionsSelector);

    this.loaderEl = document.querySelector(CONFIG.loaderSelector);
    this.loaderBar = document.querySelector(CONFIG.loaderBarSelector);
    this.loaderStatus = document.querySelector(CONFIG.loaderStatusSelector);
  }

  /**
   * Initializes the application
   */
  async start() {
    if (!this.canvas || !this.scrollWrapper) {
      console.error('Core canvas or hero scroll wrapper missing.');
      return;
    }

    const renderer = new CanvasRenderer(this.canvas);

    // Initialize transparent sand animation engine
    let sandEngine = null;
    if (this.sandCanvas) {
      sandEngine = new SandParticleEngine(this.sandCanvas, {
        sandColor: CONFIG.sandColor
      });
    }

    const loader = new FrameLoader({
      totalFrames: CONFIG.totalFrames,
      framePath: CONFIG.framePath,
      onProgress: (loaded, total) => {
        const pct = Math.round((loaded / total) * 100);
        if (this.loaderBar) {
          this.loaderBar.style.width = `${pct}%`;
        }
        if (this.loaderStatus) {
          this.loaderStatus.textContent = `BUFFERING FRAMES ${pct}% (${loaded}/${total})`;
        }
      }
    });

    // Create Timeline right away with UI hooks
    const timeline = new ScrollTimeline({
      wrapper: this.scrollWrapper,
      renderer,
      loader,
      sandEngine,
      glassCard: this.glassCard,
      subheading: this.subheading,
      actions: this.actions,
      totalFrames: CONFIG.totalFrames,
      lerpFactor: CONFIG.lerpFactor
    });

    // Load first frame immediately and paint it
    const firstImg = await loader.loadImage(1);
    renderer.render(firstImg);

    // Fade out loader screen immediately once initial frame is ready
    if (this.loaderEl) {
      this.loaderEl.classList.add('hidden');
    }

    // Initialize animation timeline
    timeline.init();

    // Initialize featured products interactions
    const featuredManager = new FeaturedProductsManager('#featured-products');
    featuredManager.init();

    // Initialize promise section interactions
    const promiseManager = new PromiseSectionManager('#brand-promise');
    promiseManager.init();

    // Initialize brand footer interactions
    const footerManager = new FooterManager('#site-footer');
    footerManager.init();

    // Stream the rest of the 270 frames progressively in background
    loader.loadAll(10).then(() => {
      const current = loader.getFrame(timeline.currentFrameIndex);
      if (current) renderer.render(current);
    });
  }
}

// Boot application
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => {
    const app = new App();
    app.start();
  });
} else {
  const app = new App();
  app.start();
}
