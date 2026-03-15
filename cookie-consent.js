/**
 * Protevio Cookie Consent
 * 
 * Simple accept/decline banner. Only loads analytics and marketing
 * scripts when the user accepts. Stores preference in a cookie
 * that lasts 365 days.
 * 
 * SETUP: Replace the placeholder IDs below with your real ones:
 *   - GA_ID: Your Google Analytics 4 Measurement ID (e.g. "G-XXXXXXXXXX")
 *   - META_PIXEL_ID: Your Meta/Facebook Pixel ID (e.g. "1234567890")
 */

(function() {
  // ══════════════════════════════════════════════════════════
  // CONFIG — Fill in your tracking IDs here
  // ══════════════════════════════════════════════════════════
  var GA_ID = '';           // e.g. 'G-XXXXXXXXXX'
  var META_PIXEL_ID = '';   // e.g. '1234567890'
  // ══════════════════════════════════════════════════════════

  var COOKIE_NAME = 'protevio_consent';
  var COOKIE_DAYS = 365;

  // --- Cookie helpers ---
  function setCookie(name, value, days) {
    var d = new Date();
    d.setTime(d.getTime() + days * 86400000);
    document.cookie = name + '=' + value + ';expires=' + d.toUTCString() + ';path=/;SameSite=Lax;Secure';
  }

  function getCookie(name) {
    var match = document.cookie.match(new RegExp('(^| )' + name + '=([^;]+)'));
    return match ? match[2] : null;
  }

  // --- Load tracking scripts ---
  function loadAnalytics() {
    // Google Analytics 4
    if (GA_ID) {
      var s = document.createElement('script');
      s.async = true;
      s.src = 'https://www.googletagmanager.com/gtag/js?id=' + GA_ID;
      document.head.appendChild(s);
      window.dataLayer = window.dataLayer || [];
      function gtag() { window.dataLayer.push(arguments); }
      gtag('js', new Date());
      gtag('config', GA_ID, {
        anonymize_ip: true,
        cookie_flags: 'SameSite=None;Secure'
      });
      window.gtag = gtag;
    }

    // Meta / Facebook Pixel
    if (META_PIXEL_ID) {
      !function(f,b,e,v,n,t,s) {
        if(f.fbq)return;n=f.fbq=function(){n.callMethod?
        n.callMethod.apply(n,arguments):n.queue.push(arguments)};
        if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
        n.queue=[];t=b.createElement(e);t.async=!0;
        t.src=v;s=b.getElementsByTagName(e)[0];
        s.parentNode.insertBefore(t,s)
      }(window,document,'script','https://connect.facebook.net/en_US/fbevents.js');
      fbq('init', META_PIXEL_ID);
      fbq('track', 'PageView');
    }
  }

  // --- Store user preferences cookie ---
  function savePreferences() {
    // Language preference (default: en)
    var lang = document.documentElement.lang || 'en';
    setCookie('protevio_lang', lang, COOKIE_DAYS);
  }

  // --- Banner ---
  function showBanner() {
    var banner = document.createElement('div');
    banner.className = 'cc-banner';
    banner.id = 'cookieBanner';
    banner.innerHTML =
      '<div class="cc-banner__text">' +
        'We use cookies to improve your experience, analyze traffic, and for marketing. ' +
        'By clicking "Accept", you consent to our use of cookies. ' +
        '<a href="/privacy-policy.html">Privacy Policy</a>' +
      '</div>' +
      '<div class="cc-banner__actions">' +
        '<button class="cc-banner__btn cc-banner__btn--decline" id="ccDecline">Decline</button>' +
        '<button class="cc-banner__btn cc-banner__btn--accept" id="ccAccept">Accept</button>' +
      '</div>';
    document.body.appendChild(banner);

    document.getElementById('ccAccept').addEventListener('click', function() {
      setCookie(COOKIE_NAME, 'accepted', COOKIE_DAYS);
      loadAnalytics();
      savePreferences();
      banner.remove();
    });

    document.getElementById('ccDecline').addEventListener('click', function() {
      setCookie(COOKIE_NAME, 'declined', COOKIE_DAYS);
      savePreferences();
      banner.remove();
    });
  }

  // --- "Manage cookies" link handler ---
  function bindManageLinks() {
    document.querySelectorAll('[data-cc-manage]').forEach(function(el) {
      el.addEventListener('click', function(e) {
        e.preventDefault();
        // Remove existing consent so banner shows again
        setCookie(COOKIE_NAME, '', -1);
        // Show banner
        if (!document.getElementById('cookieBanner')) {
          showBanner();
        }
      });
    });
  }

  // --- Init ---
  function init() {
    var consent = getCookie(COOKIE_NAME);

    if (consent === 'accepted') {
      // User already accepted — load scripts
      loadAnalytics();
      savePreferences();
    } else if (consent === 'declined') {
      // User declined — save preferences only (no tracking)
      savePreferences();
    } else {
      // No consent yet — show banner
      showBanner();
    }

    // Bind "manage cookies" footer links
    bindManageLinks();
  }

  // Wait for DOM
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
