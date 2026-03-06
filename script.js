/* ============================================================
   Hamptons Elite Powerwashing — script.js
   Features:
   - Mobile hamburger menu toggle (full-screen overlay)
   - Smooth scroll for anchor links
   - Sticky header scroll behavior
   - Service tab panel toggle (Residential / Commercial)
   - Formspree AJAX form submission with success message
   No external dependencies. Vanilla JS only.
============================================================ */

(function () {
  'use strict';

  /* ---- DOM References -------------------------------------- */
  var header       = document.getElementById('site-header');
  var hamburger    = document.getElementById('hamburger');
  var mobileNav    = document.getElementById('mobile-nav');
  var mobileClose  = document.getElementById('mobile-nav-close');
  var mobileLinks  = document.querySelectorAll('.mobile-nav-link');
  var toggleBtns   = document.querySelectorAll('.toggle-btn');
  var quoteForm    = document.getElementById('quote-form');
  var formSuccess  = document.getElementById('form-success');

  /* ---- Sticky Header on Scroll ---------------------------- */
  // Header is always solid — no additional logic needed.
  // If you want a transparent-to-solid transition, uncomment:
  /*
  function handleScroll() {
    if (window.scrollY > 60) {
      header.classList.add('scrolled');
    } else {
      header.classList.remove('scrolled');
    }
  }
  window.addEventListener('scroll', handleScroll, { passive: true });
  */

  /* ---- Mobile Menu Toggle --------------------------------- */
  function openMenu() {
    hamburger.classList.add('open');
    hamburger.setAttribute('aria-expanded', 'true');
    mobileNav.classList.add('open');
    mobileNav.removeAttribute('aria-hidden');
    document.body.style.overflow = 'hidden'; // prevent background scroll
  }

  function closeMenu() {
    hamburger.classList.remove('open');
    hamburger.setAttribute('aria-expanded', 'false');
    mobileNav.classList.remove('open');
    mobileNav.setAttribute('aria-hidden', 'true');
    document.body.style.overflow = '';
  }

  if (hamburger) {
    hamburger.addEventListener('click', function () {
      if (hamburger.classList.contains('open')) {
        closeMenu();
      } else {
        openMenu();
      }
    });
  }

  if (mobileClose) {
    mobileClose.addEventListener('click', closeMenu);
  }

  // Close menu when a nav link is tapped
  mobileLinks.forEach(function (link) {
    link.addEventListener('click', closeMenu);
  });

  // Close menu if user taps outside (on the overlay background)
  if (mobileNav) {
    mobileNav.addEventListener('click', function (e) {
      if (e.target === mobileNav) {
        closeMenu();
      }
    });
  }

  // Close menu on Escape key
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && mobileNav && mobileNav.classList.contains('open')) {
      closeMenu();
      hamburger.focus();
    }
  });

  /* ---- Service Panel Toggle (Residential / Commercial) ---- */
  toggleBtns.forEach(function (btn) {
    btn.addEventListener('click', function () {
      var target = btn.getAttribute('data-target');

      // Update button states
      toggleBtns.forEach(function (b) {
        b.classList.remove('active');
        b.setAttribute('aria-selected', 'false');
      });
      btn.classList.add('active');
      btn.setAttribute('aria-selected', 'true');

      // Show/hide panels
      var panels = document.querySelectorAll('.service-panel');
      panels.forEach(function (panel) {
        if (panel.id === 'panel-' + target) {
          panel.classList.add('active');
          panel.removeAttribute('hidden');
        } else {
          panel.classList.remove('active');
          panel.setAttribute('hidden', '');
        }
      });
    });
  });

  /* ---- Smooth Scroll for All Anchor Links ----------------- */
  document.addEventListener('click', function (e) {
    var link = e.target.closest('a[href^="#"]');
    if (!link) return;

    var targetId = link.getAttribute('href').slice(1);
    if (!targetId) return;

    var targetEl = document.getElementById(targetId);
    if (!targetEl) return;

    e.preventDefault();

    // Offset for fixed header height
    var headerHeight = header ? header.offsetHeight : 0;
    var targetTop = targetEl.getBoundingClientRect().top + window.pageYOffset - headerHeight - 8;

    window.scrollTo({ top: targetTop, behavior: 'smooth' });

    // Update focus for accessibility
    targetEl.setAttribute('tabindex', '-1');
    targetEl.focus({ preventScroll: true });
  });

  /* ---- Formspree AJAX Form Submission --------------------- */
  if (quoteForm) {
    quoteForm.addEventListener('submit', function (e) {
      var action = quoteForm.getAttribute('action');

      // If the user hasn't replaced the placeholder, let native submit happen
      // so they see the Formspree error page (reminder to set up their form)
      if (!action || action.indexOf('YOUR_FORMSPREE_ID') !== -1) {
        return; // fall through to native form submit
      }

      e.preventDefault();

      var submitBtn = quoteForm.querySelector('[type="submit"]');
      var originalText = submitBtn.textContent;
      submitBtn.disabled = true;
      submitBtn.textContent = 'Sending...';

      var data = new FormData(quoteForm);

      fetch(action, {
        method: 'POST',
        body: data,
        headers: { 'Accept': 'application/json' }
      })
        .then(function (response) {
          if (response.ok) {
            quoteForm.reset();
            if (formSuccess) {
              formSuccess.removeAttribute('hidden');
              formSuccess.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
            }
          } else {
            return response.json().then(function (json) {
              throw new Error(json.error || 'Submission failed');
            });
          }
        })
        .catch(function (err) {
          console.error('Form submission error:', err);
          alert('Sorry, there was a problem submitting the form. Please call us directly at (631) XXX-XXXX.');
        })
        .finally(function () {
          submitBtn.disabled = false;
          submitBtn.textContent = originalText;
        });
    });
  }

  /* ---- Highlight active nav section on scroll ------------- */
  // Optional: uncomment if you want active link highlighting
  /*
  var sections = document.querySelectorAll('section[id]');
  function highlightNav() {
    var scrollPos = window.scrollY + (header ? header.offsetHeight : 0) + 40;
    sections.forEach(function(section) {
      if (scrollPos >= section.offsetTop && scrollPos < section.offsetTop + section.offsetHeight) {
        // could add active class to corresponding nav link here
      }
    });
  }
  window.addEventListener('scroll', highlightNav, { passive: true });
  */

})();
