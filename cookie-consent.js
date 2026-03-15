/**
 * Protevio Cookie Consent
 * Self-contained popup with built-in styles.
 * Loads GA4 + Meta Pixel only when user accepts.
 */
(function() {
  var GA_ID = 'G-W2LVCL8XJP';
  var META_PIXEL_ID = '';
  var COOKIE_NAME = 'protevio_consent';
  var COOKIE_DAYS = 365;

  function setCookie(n, v, d) {
    var e = new Date();
    e.setTime(e.getTime() + d * 864e5);
    document.cookie = n + '=' + v + ';expires=' + e.toUTCString() + ';path=/;SameSite=Lax;Secure';
  }
  function getCookie(n) {
    var m = document.cookie.match(new RegExp('(^| )' + n + '=([^;]+)'));
    return m ? m[2] : null;
  }

  function loadAnalytics() {
    if (GA_ID) {
      var s = document.createElement('script');
      s.async = true;
      s.src = 'https://www.googletagmanager.com/gtag/js?id=' + GA_ID;
      document.head.appendChild(s);
      window.dataLayer = window.dataLayer || [];
      function gtag() { window.dataLayer.push(arguments); }
      gtag('js', new Date());
      gtag('config', GA_ID, { anonymize_ip: true });
      window.gtag = gtag;
    }
    if (META_PIXEL_ID) {
      !function(f,b,e,v,n,t,s){if(f.fbq)return;n=f.fbq=function(){n.callMethod?
      n.callMethod.apply(n,arguments):n.queue.push(arguments)};if(!f._fbq)f._fbq=n;
      n.push=n;n.loaded=!0;n.version='2.0';n.queue=[];t=b.createElement(e);t.async=!0;
      t.src=v;s=b.getElementsByTagName(e)[0];s.parentNode.insertBefore(t,s)}
      (window,document,'script','https://connect.facebook.net/en_US/fbevents.js');
      fbq('init', META_PIXEL_ID);
      fbq('track', 'PageView');
    }
  }

  function injectStyles() {
    if (document.getElementById('cc-styles')) return;
    var style = document.createElement('style');
    style.id = 'cc-styles';
    style.textContent =
      '.cc-overlay{position:fixed;inset:0;background:rgba(0,0,0,.45);backdrop-filter:blur(4px);z-index:99998;opacity:0;transition:opacity .3s ease}' +
      '.cc-overlay.cc-show{opacity:1}' +
      '.cc-popup{position:fixed;bottom:32px;left:50%;transform:translateX(-50%) translateY(30px);z-index:99999;' +
        'background:#fff;border-radius:16px;box-shadow:0 20px 60px rgba(0,0,0,.15),0 0 0 1px rgba(0,0,0,.04);' +
        'padding:32px;max-width:440px;width:calc(100% - 32px);opacity:0;transition:all .4s cubic-bezier(.4,0,.2,1);font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif}' +
      '.cc-popup.cc-show{opacity:1;transform:translateX(-50%) translateY(0)}' +
      '.cc-popup__icon{width:48px;height:48px;border-radius:12px;background:linear-gradient(135deg,#f0f4ff,#e8eeff);display:flex;align-items:center;justify-content:center;margin-bottom:16px}' +
      '.cc-popup__icon svg{width:24px;height:24px;stroke:#2563eb;stroke-width:2;fill:none}' +
      '.cc-popup__title{font-size:1.1rem;font-weight:700;color:#18181b;margin-bottom:8px}' +
      '.cc-popup__text{font-size:.85rem;color:#71717a;line-height:1.65;margin-bottom:24px}' +
      '.cc-popup__text a{color:#2563eb;text-decoration:underline}' +
      '.cc-popup__actions{display:flex;gap:10px}' +
      '.cc-popup__btn{flex:1;padding:12px 16px;border-radius:10px;font-size:.88rem;font-weight:600;cursor:pointer;border:none;transition:all .15s;font-family:inherit}' +
      '.cc-popup__btn--accept{background:#18181b;color:#fff}' +
      '.cc-popup__btn--accept:hover{background:#2563eb}' +
      '.cc-popup__btn--decline{background:#f4f4f5;color:#52525b}' +
      '.cc-popup__btn--decline:hover{background:#e4e4e7;color:#18181b}' +
      '@media(max-width:480px){.cc-popup{bottom:16px;padding:24px;max-width:calc(100% - 24px)}.cc-popup__actions{flex-direction:column-reverse}}';
    document.head.appendChild(style);
  }

  function showPopup() {
    injectStyles();
    var overlay = document.createElement('div');
    overlay.className = 'cc-overlay';
    overlay.id = 'ccOverlay';
    document.body.appendChild(overlay);

    var popup = document.createElement('div');
    popup.className = 'cc-popup';
    popup.id = 'ccPopup';
    popup.innerHTML =
      '<div class="cc-popup__icon">' +
        '<svg viewBox="0 0 24 24"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="M9 12l2 2 4-4"/></svg>' +
      '</div>' +
      '<div class="cc-popup__title">Your privacy matters</div>' +
      '<div class="cc-popup__text">' +
        'We use cookies to analyze traffic and improve your experience. ' +
        'You can accept all cookies or decline non-essential ones. ' +
        '<a href="/privacy-policy.html">Privacy Policy</a>' +
      '</div>' +
      '<div class="cc-popup__actions">' +
        '<button class="cc-popup__btn cc-popup__btn--decline" id="ccDecline">Decline</button>' +
        '<button class="cc-popup__btn cc-popup__btn--accept" id="ccAccept">Accept all</button>' +
      '</div>';
    document.body.appendChild(popup);

    requestAnimationFrame(function() {
      requestAnimationFrame(function() {
        overlay.classList.add('cc-show');
        popup.classList.add('cc-show');
      });
    });

    function close(accepted) {
      popup.classList.remove('cc-show');
      overlay.classList.remove('cc-show');
      setTimeout(function() { popup.remove(); overlay.remove(); }, 350);
      setCookie(COOKIE_NAME, accepted ? 'accepted' : 'declined', COOKIE_DAYS);
      if (accepted) loadAnalytics();
    }

    document.getElementById('ccAccept').addEventListener('click', function() { close(true); });
    document.getElementById('ccDecline').addEventListener('click', function() { close(false); });
    overlay.addEventListener('click', function() { close(false); });
  }

  function bindManageLinks() {
    document.querySelectorAll('[data-cc-manage]').forEach(function(el) {
      el.addEventListener('click', function(e) {
        e.preventDefault();
        setCookie(COOKIE_NAME, '', -1);
        if (!document.getElementById('ccPopup')) showPopup();
      });
    });
  }

  function init() {
    var consent = getCookie(COOKIE_NAME);
    if (consent === 'accepted') loadAnalytics();
    else if (!consent) showPopup();
    bindManageLinks();
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
