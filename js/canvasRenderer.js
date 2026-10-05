import { calculateCoverDimensions } from './utils.js';

/**
 * High-performance Canvas Renderer for video frames
 * Preserves lossless native resolution across all devices and aspect ratios
 */
export class CanvasRenderer {
  /**
   * @param {HTMLCanvasElement} canvas 
   */
  constructor(canvas) {
    this.canvas = canvas;
    this.ctx = canvas.getContext('2d', { alpha: false, desynchronized: true });
    this.width = 0;
    this.height = 0;
    this.dpr = 1;
    this.lastRenderedFrame = null;
    
    this.resize();
    window.addEventListener('resize', () => this.resize(), { passive: true });
    window.addEventListener('orientationchange', () => this.resize(), { passive: true });
  }

  /**
   * Resizes canvas buffer to match physical device pixels and scaling
   */
  resize() {
    const viewWidth = window.innerWidth || document.documentElement.clientWidth || 1920;
    const viewHeight = window.innerHeight || document.documentElement.clientHeight || 1080;
    this.dpr = Math.min(window.devicePixelRatio || 1, 2);

    this.width = Math.round(viewWidth);
    this.height = Math.round(viewHeight);

    // Explicitly set matching physical buffer resolution
    this.canvas.width = Math.round(this.width * this.dpr);
    this.canvas.height = Math.round(this.height * this.dpr);

    // High quality image smoothing
    this.ctx.imageSmoothingEnabled = true;
    this.ctx.imageSmoothingQuality = 'high';

    if (this.lastRenderedFrame) {
      this.render(this.lastRenderedFrame);
    }
  }

  /**
   * Renders frame to canvas using centered cover projection
   * @param {HTMLImageElement} image 
   */
  render(image) {
    if (!image) return;
    this.lastRenderedFrame = image;

    const bufferWidth = this.canvas.width;
    const bufferHeight = this.canvas.height;
    if (bufferWidth === 0 || bufferHeight === 0) return;

    const imgWidth = image.naturalWidth || image.width || 1920;
    const imgHeight = image.naturalHeight || image.height || 1080;

    const { dx, dy, dWidth, dHeight } = calculateCoverDimensions(
      bufferWidth,
      bufferHeight,
      imgWidth,
      imgHeight
    );

    this.ctx.fillStyle = '#08090d';
    this.ctx.fillRect(0, 0, bufferWidth, bufferHeight);
    this.ctx.drawImage(image, dx, dy, dWidth, dHeight);
  }
}
