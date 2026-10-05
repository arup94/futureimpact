/**
 * Contact Form Interactive Handler & Validation Module
 */

export function initContactForm() {
  const contactForm = document.getElementById('contactForm');
  const formStatus = document.getElementById('formStatus');

  if (!contactForm) return;

  contactForm.addEventListener('submit', handleContactSubmit);
}

export function validateContactData(formData) {
  const errors = [];

  if (!formData.fullName || formData.fullName.trim().length < 2) {
    errors.push('Please enter a valid full name.');
  }

  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!formData.email || !emailRegex.test(formData.email.trim())) {
    errors.push('Please enter a valid email address.');
  }

  const phoneDigits = (formData.mobile || '').replace(/\D/g, '');
  if (!phoneDigits || phoneDigits.length < 10) {
    errors.push('Please enter a valid 10-digit mobile number.');
  }

  if (!formData.message || formData.message.trim().length < 5) {
    errors.push('Please enter your message (at least 5 characters).');
  }

  return {
    isValid: errors.length === 0,
    errors
  };
}

function handleContactSubmit(e) {
  e.preventDefault();

  const form = e.currentTarget;
  const statusEl = document.getElementById('formStatus');
  const submitBtn = form.querySelector('.btn-submit-contact');

  const formData = {
    fullName: form.fullName?.value || '',
    email: form.email?.value || '',
    mobile: form.mobile?.value || '',
    message: form.message?.value || ''
  };

  const validation = validateContactData(formData);

  if (!validation.isValid) {
    if (statusEl) {
      statusEl.className = 'form-status-alert error';
      statusEl.textContent = validation.errors[0];
      statusEl.style.display = 'block';
    }
    return;
  }

  if (submitBtn) {
    submitBtn.disabled = true;
    submitBtn.textContent = 'Sending Message...';
  }

  // Simulate network request dispatch
  setTimeout(() => {
    if (statusEl) {
      statusEl.className = 'form-status-alert success';
      statusEl.textContent = `Thank you, ${formData.fullName}! Your message has been received. Our botanical care team will get back to you shortly.`;
      statusEl.style.display = 'block';
    }

    form.reset();

    if (submitBtn) {
      submitBtn.disabled = false;
      submitBtn.innerHTML = `
        <span>Send Message</span>
        <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <line x1="22" y1="2" x2="11" y2="13"></line>
          <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
        </svg>
      `;
    }
  }, 600);
}

document.addEventListener('DOMContentLoaded', () => {
  initContactForm();
});
