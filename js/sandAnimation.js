import { clamp01, easeInOutCubic } from './utils.js';

/**
 * SandParticleEngine - Reversible, scroll-driven sand particle text animation
 * Renders "Future Impact" prominently in the middle of the screen.
 */
export class SandParticleEngine {
  /**
   * @param {HTMLCanvasElement} canvas
   * @param {Object} options
   */
  constructor(canvas, options = {}) {
    this.canvas = canvas;
    this.ctx = canvas.getContext('2d');

    this.settings = {
      cellSize: 3,
      startText: 'Future Impact',
      sandColor: options.sandColor || '#1b301e',
      ...options
    };

    this.w = 0;
    this.h = 0;
    this.dpr = Math.min(window.devicePixelRatio || 1, 2);

    this.particles = [];
    this.progress = 0; // 0.0 to 1.0 driven by scroll-end

    this.resize = this.resize.bind(this);
    this.resize();
    window.addEventListener('resize', this.resize, { passive: true });
  }

  resize() {
    this.w = window.innerWidth;
    this.h = window.innerHeight;
    this.dpr = Math.min(window.devicePixelRatio || 1, 2);

    this.canvas.width = Math.round(this.w * this.dpr);
    this.canvas.height = Math.round(this.h * this.dpr);
    this.canvas.style.width = `${this.w}px`;
    this.canvas.style.height = `${this.h}px`;

    this.ctx.setTransform(this.dpr, 0, 0, this.dpr, 0, 0);

    this.buildParticles();
    this.render(this.progress);
  }

  buildParticles() {
    this.particles = [];
    const off = document.createElement('canvas');
    off.width = this.w;
    off.height = this.h;
    const octx = off.getContext('2d');

    octx.clearRect(0, 0, this.w, this.h);
    octx.fillStyle = '#ffffff';
    octx.textAlign = 'center';
    octx.textBaseline = 'middle';

    // Position "Future Impact" in the true middle-upper zone of the centered block
    const startFontSize = Math.min(this.w * 0.14, this.h * 0.15, 92);
    octx.font = `900 ${startFontSize}px "Outfit", sans-serif`;

    const centerY = this.h * 0.40;
    octx.fillText(this.settings.startText, this.w / 2, centerY);

    const img = octx.getImageData(0, 0, this.w, this.h).data;
    const cs = this.settings.cellSize;
    const pileY = this.h * 0.60;

    for (let y = 0; y < this.h; y += cs) {
      for (let x = 0; x < this.w; x += cs) {
        const pIndex = (y * this.w + x) * 4;
        if (img[pIndex + 3] > 35) {
          const normX = x / this.w;
          const stagger = (normX * 0.25) + ((y / this.h) * 0.25) + (Math.sin(x * 0.05) * 0.08);

          this.particles.push({
            origX: x,
            origY: y,
            pileX: x + Math.sin(x * 0.1) * 30,
            pileY: pileY + Math.cos(x * 0.08) * (cs * 2.5),
            stagger: Math.max(0, Math.min(0.4, stagger)),
            driftX: (Math.sin(x + y) * 35),
            arcH: 35 + (Math.sin(x * 0.2) * 15)
          });
        }
      }
    }
  }

  /**
   * Render state corresponding to scroll progress (0.0 = initial text, 1.0 = fully reformed)
   * Smoothly reversible up-down and down-up
   * @param {number} p 0.0 to 1.0
   */
  render(p) {
    this.progress = clamp01(p);
    this.ctx.clearRect(0, 0, this.w, this.h);

    if (this.progress <= 0.001) {
      return; // Fully transparent when not at scroll end
    }

    const cs = this.settings.cellSize;
    this.ctx.fillStyle = this.settings.sandColor;
    const prog = this.progress;

    // Render individual sand particles
    for (let i = 0; i < this.particles.length; i++) {
      const part = this.particles[i];
      let px = part.origX;
      let py = part.origY;

      if (prog < 0.45) {
        // Falling down into sand pile
        const localT = clamp01((prog - part.stagger) / (0.45 - part.stagger));
        const eased = easeInOutCubic(localT);
        px = part.origX + part.driftX * Math.sin(eased * Math.PI);
        py = part.origY + (part.pileY - part.origY) * eased;
      } else if (prog < 0.70) {
        // Resting in sand pile
        px = part.pileX;
        py = part.pileY;
      } else {
        // Reforming back upwards into initial text
        const localT = clamp01((prog - 0.70) / 0.30);
        const eased = easeInOutCubic(localT);
        const arc = Math.sin(eased * Math.PI) * part.arcH;
        px = part.pileX + (part.origX - part.pileX) * eased;
        py = part.pileY + (part.origY - part.pileY) * eased - arc;
      }

      this.ctx.fillRect(px, py, cs, cs);
    }
  }

  destroy() {
    window.removeEventListener('resize', this.resize);
  }
}
