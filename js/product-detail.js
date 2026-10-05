/**
 * Product detail page interaction: thumbnail switching and pack selector link update
 */
document.addEventListener('DOMContentLoaded', () => {
  // 1. Thumbnail click handler
  const mainImage = document.getElementById('mainProductImage');
  const thumbButtons = document.querySelectorAll('.thumb-btn');

  thumbButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      thumbButtons.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      const newSrc = btn.getAttribute('data-img');
      if (mainImage && newSrc) {
        mainImage.src = newSrc;
      }
    });
  });

  // 2. Pack selector handler
  const packButtons = document.querySelectorAll('.pack-btn');
  const buyButton = document.getElementById('buyAmazonBtn');

  packButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      packButtons.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      const amazonUrl = btn.getAttribute('data-amazon');
      if (buyButton && amazonUrl) {
        buyButton.href = amazonUrl;
      }
    });
  });
});
