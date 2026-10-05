/**
 * Preloader for frames with concurrency control and progress tracking
 */
export class FrameLoader {
  /**
   * @param {Object} options
   * @param {number} options.totalFrames
   * @param {function(number): string} options.framePath
   * @param {function(number, number): void} options.onProgress
   */
  constructor({ totalFrames, framePath, onProgress }) {
    this.totalFrames = totalFrames;
    this.framePath = framePath;
    this.onProgress = onProgress || (() => {});
    this.images = new Array(totalFrames);
    this.loadedCount = 0;
  }

  /**
   * Loads a single image by 1-based index
   * @param {number} index 
   * @returns {Promise<HTMLImageElement>}
   */
  loadImage(index) {
    return new Promise((resolve) => {
      const img = new Image();
      img.src = this.framePath(index);
      
      const onDone = () => {
        this.images[index - 1] = img;
        this.loadedCount++;
        this.onProgress(this.loadedCount, this.totalFrames);
        resolve(img);
      };

      img.onload = onDone;
      img.onerror = () => {
        console.warn(`Failed to load frame ${index}`);
        onDone();
      };
    });
  }

  /**
   * Loads all frames with batched concurrency
   * @param {number} concurrency 
   * @returns {Promise<HTMLImageElement[]>}
   */
  async loadAll(concurrency = 8) {
    const indices = Array.from({ length: this.totalFrames }, (_, i) => i + 1);
    const executing = [];

    for (const index of indices) {
      const p = this.loadImage(index).then(() => {
        const idx = executing.indexOf(p);
        if (idx !== -1) executing.splice(idx, 1);
      });
      executing.push(p);

      if (executing.length >= concurrency) {
        await Promise.race(executing);
      }
    }

    await Promise.all(executing);
    return this.images;
  }

  /**
   * Returns image at given 0-based or 1-based index
   * @param {number} frameIndex 1-based index
   * @returns {HTMLImageElement|null}
   */
  getFrame(frameIndex) {
    const idx = Math.max(0, Math.min(this.totalFrames - 1, frameIndex - 1));
    return this.images[idx] || null;
  }
}
