/**
 * Animation Configuration Constants
 */
export const CONFIG = {
  totalFrames: 270,
  framePath: (index) => `frameswl/ezgif-frame-${String(index).padStart(3, '0')}.jpg`,
  aspectRatio: 1920 / 1080,
  dprMax: 2,
  lerpFactor: 0.12, // Smooth interpolation rate for video-like scrub
  scrollWrapperSelector: '.hero-scroll-wrapper',
  canvasSelector: '#scrollCanvas',
  sandCanvasSelector: '#sandCanvas',
  glassCardSelector: '#glassContentCard',
  subheadingSelector: '#glassSubheading',
  actionsSelector: '#glassActions',
  loaderSelector: '#loaderScreen',
  loaderBarSelector: '#loaderBarFill',
  loaderStatusSelector: '#loaderStatus',
  sandColor: '#1b301e'
};
