/**
 * Scroll Timeline Controller managing smooth lerping across full frame sequence,
 * reversible sand animation, fullscreen glass backdrop, and sequential typography/button reveals.
 * When in the end sequence, background canvas always presents the final frames cleanly.
 */
import { lerp, clamp, clamp01, calculateScrollProgress } from './utils.js';

export class ScrollTimeline {
  /**
   * @param {Object} options
   * @param {HTMLElement} options.wrapper
   * @param {import('./canvasRenderer.js').CanvasRenderer} options.renderer
   * @param {import('./frameLoader.js').FrameLoader} options.loader
   * @param {import('./sandAnimation.js').SandParticleEngine} options.sandEngine
   * @param {HTMLElement} options.glassCard
   * @param {HTMLElement} options.subheading
   * @param {HTMLElement} options.actions
   * @param {number} options.totalFrames
   * @param {number} options.lerpFactor
   */
  constructor({ wrapper, renderer, loader, sandEngine, glassCard, subheading, actions, totalFrames, lerpFactor }) {
    this.wrapper = wrapper;
    this.renderer = renderer;
    this.loader = loader;
    this.sandEngine = sandEngine || null;
    this.glassCard = glassCard || null;
    this.subheading = subheading || null;
    this.actions = actions || null;
    this.totalFrames = totalFrames;
    this.lerpFactor = lerpFactor;

    this.targetProgress = 0;
    this.currentProgress = 0;
    this.currentFrameIndex = 1;
    this.isRunning = false;

    this.onScroll = this.onScroll.bind(this);
    this.tick = this.tick.bind(this);
  }

  /**
   * Initializes event listeners and starts the render loop
   */
  init() {
    window.addEventListener('scroll', this.onScroll, { passive: true });
    this.onScroll();
    this.start();
  }

  /**
   * Handle scroll event to update target progress
   */
  onScroll() {
    this.targetProgress = calculateScrollProgress(this.wrapper);
  }

  /**
   * Starts the animation loop
   */
  start() {
    if (this.isRunning) return;
    this.isRunning = true;
    requestAnimationFrame(this.tick);
  }

  /**
   * Animation loop tick
   */
  tick() {
    if (!this.isRunning) return;

    // Smooth lerp to target progress for video-like scrub
    this.currentProgress = lerp(this.currentProgress, this.targetProgress, this.lerpFactor);

    // Frame sequence scrubbing maps across 0.0 to 0.85 of the total scroll
    // Once currentProgress >= 0.85, frame clamps to totalFrames (last frame), keeping it visible in the background
    const frameScrubProgress = clamp01(this.currentProgress / 0.85);
    const frameNumber = Math.round(frameScrubProgress * (this.totalFrames - 1)) + 1;
    const clampedFrame = clamp(frameNumber, 1, this.totalFrames);

    if (clampedFrame !== this.currentFrameIndex) {
      this.currentFrameIndex = clampedFrame;
      const img = this.loader.getFrame(this.currentFrameIndex);
      if (img) {
        this.renderer.render(img);
      }
    } else if (this.currentProgress >= 0.85 && this.currentFrameIndex !== this.totalFrames) {
      // Ensure the last frame is explicitly rendered for the background
      this.currentFrameIndex = this.totalFrames;
      const lastImg = this.loader.getFrame(this.totalFrames);
      if (lastImg) {
        this.renderer.render(lastImg);
      }
    }

    // Bi-directional reversible animation at scroll end (0.85 -> 1.0):
    const sandProgress = clamp01((this.currentProgress - 0.85) / 0.15);

    if (this.sandEngine) {
      this.sandEngine.render(sandProgress);
    }

    // Fullscreen transparent backdrop & sequential text/button choreography
    this.updateEndOverlay(sandProgress);

    requestAnimationFrame(this.tick);
  }

  /**
   * Updates fullscreen glass backdrop, subheading, and CTA button states based on sandProgress
   * @param {number} p 0.0 to 1.0
   */
  updateEndOverlay(p) {
    if (!this.glassCard) return;

    if (p <= 0.02) {
      this.glassCard.style.opacity = '0';
      this.glassCard.style.pointerEvents = 'none';
      if (this.subheading) this.subheading.style.opacity = '0';
      if (this.actions) this.actions.style.opacity = '0';
      return;
    }

    // Step 1: Fullscreen transparent backdrop fades in cleanly over the last frame
    const cardOpacity = clamp01(p / 0.15);
    this.glassCard.style.opacity = cardOpacity.toFixed(3);
    this.glassCard.style.pointerEvents = p > 0.4 ? 'auto' : 'none';

    // Step 2: "Luxury Inspired by Nature." reveals after initial text dissolution
    if (this.subheading) {
      const subAlpha = clamp01((p - 0.35) / 0.25);
      this.subheading.style.opacity = subAlpha.toFixed(3);
      this.subheading.style.transform = `translateY(${(15 * (1 - subAlpha)).toFixed(1)}px)`;
    }

    // Step 3: Two action buttons ("shop collection", "contact us") fade in sequentially below
    if (this.actions) {
      const btnAlpha = clamp01((p - 0.55) / 0.25);
      this.actions.style.opacity = btnAlpha.toFixed(3);
      this.actions.style.transform = `translateY(${(20 * (1 - btnAlpha)).toFixed(1)}px)`;
      this.actions.style.pointerEvents = btnAlpha > 0.5 ? 'auto' : 'none';
    }
  }

  /**
   * Destroys listeners and stops loop
   */
  destroy() {
    this.isRunning = false;
    window.removeEventListener('scroll', this.onScroll);
  }
}
