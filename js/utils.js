/**
 * Math, layout and particle interpolation utilities
 */

/**
 * Linear interpolation between start and end
 * @param {number} start 
 * @param {number} end 
 * @param {number} factor 
 * @returns {number}
 */
export function lerp(start, end, factor) {
  return start + (end - start) * factor;
}

/**
 * Clamp a number between min and max
 * @param {number} value 
 * @param {number} min 
 * @param {number} max 
 * @returns {number}
 */
export function clamp(value, min, max) {
  return Math.min(Math.max(value, min), max);
}

/**
 * Clamps value between 0 and 1
 * @param {number} v 
 * @returns {number}
 */
export function clamp01(v) {
  return Math.max(0, Math.min(1, v));
}

/**
 * Ease in-out cubic interpolation
 * @param {number} t 
 * @returns {number}
 */
export function easeInOutCubic(t) {
  return t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
}

/**
 * Calculates current scroll progress of an element relative to viewport
 * @param {HTMLElement} element 
 * @returns {number} Progress from 0.0 to 1.0
 */
export function calculateScrollProgress(element) {
  if (!element) return 0;
  const rect = element.getBoundingClientRect();
  const totalScrollableDistance = element.offsetHeight - window.innerHeight;
  if (totalScrollableDistance <= 0) return 0;
  
  const currentScrolled = -rect.top;
  const progress = currentScrolled / totalScrollableDistance;
  return clamp(progress, 0, 1);
}

/**
 * Calculates 'object-fit: cover' destination dimensions and offsets
 * @param {number} containerWidth 
 * @param {number} containerHeight 
 * @param {number} imageWidth 
 * @param {number} imageHeight 
 * @returns {{dx: number, dy: number, dWidth: number, dHeight: number}}
 */
export function calculateCoverDimensions(containerWidth, containerHeight, imageWidth, imageHeight) {
  if (!containerWidth || !containerHeight || !imageWidth || !imageHeight) {
    return { dx: 0, dy: 0, dWidth: 0, dHeight: 0 };
  }

  const containerRatio = containerWidth / containerHeight;
  const imageRatio = imageWidth / imageHeight;

  let dWidth, dHeight;

  if (containerRatio > imageRatio) {
    dWidth = containerWidth;
    dHeight = containerWidth / imageRatio;
  } else {
    dHeight = containerHeight;
    dWidth = containerHeight * imageRatio;
  }

  const dx = (containerWidth - dWidth) / 2;
  const dy = (containerHeight - dHeight) / 2;

  return { dx, dy, dWidth, dHeight };
}

/**
 * Pseudo-random range helper
 * @param {number} min 
 * @param {number} max 
 * @returns {number}
 */
export function rand(min, max) {
  return min + Math.random() * (max - min);
}

/**
 * Pseudo-random integer helper
 * @param {number} min 
 * @param {number} max 
 * @returns {number}
 */
export function randInt(min, max) {
  return Math.floor(min + Math.random() * (max - min + 1));
}
