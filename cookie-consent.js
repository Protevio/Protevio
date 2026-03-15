/**
 * Protevio Cookie Consent — Full GDPR Version
 * Categories: Necessary (always on), Analytics, Marketing
 * Self-contained with built-in styles.
 */
(function() {
  var GA_ID = 'G-W2LVCL8XJP';
  var META_PIXEL_ID = '';
  var COOKIE_NAME = 'protevio_consent';
  var COOKIE_DAYS = 365;

  // ── Helpers ──
  function setCookie(n, v, d) {
    var e = new Date(); e.setTime(e.getTime() + d * 864e5);
    document.cookie = n + '=' + encodeURIComponent(v) + ';expires=' + e.toUTCString() + ';path=/;SameSite=Lax;Secure';
  }
  function getCookie(n) {
    var m = document.cookie.match(new RegExp('(^| )' + n + '=([^;]+)'));
    return m ? decodeURIComponent(m[2]) : null;
  }
  function getConsent() {
    try { return JSON.parse(getCookie(COOKIE_NAME)); } catch(e) { return null; }
  }
  function saveConsent(obj) {
    setCookie(COOKIE_NAME, JSON.stringify(obj), COOKIE_DAYS);
  }

  // ── Load scripts ──
  function loadGA() {
    if (!GA_ID || window._ga_loaded) return;
    window._ga_loaded = true;
    var s = document.createElement('script');
    s.async = true; s.src = 'https://www.googletagmanager.com/gtag/js?id=' + GA_ID;
    document.head.appendChild(s);
    window.dataLayer = window.dataLayer || [];
    function gtag() { window.dataLayer.push(arguments); }
    gtag('js', new Date());
    gtag('config', GA_ID, { anonymize_ip: true });
    window.gtag = gtag;
  }
  function loadMeta() {
    if (!META_PIXEL_ID || window._fb_loaded) return;
    window._fb_loaded = true;
    !function(f,b,e,v,n,t,s){if(f.fbq)return;n=f.fbq=function(){n.callMethod?
    n.callMethod.apply(n,arguments):n.queue.push(arguments)};if(!f._fbq)f._fbq=n;
    n.push=n;n.loaded=!0;n.version='2.0';n.queue=[];t=b.createElement(e);t.async=!0;
    t.src=v;s=b.getElementsByTagName(e)[0];s.parentNode.insertBefore(t,s)}
    (window,document,'script','https://connect.facebook.net/en_US/fbevents.js');
    fbq('init', META_PIXEL_ID); fbq('track', 'PageView');
  }
  function applyConsent(c) {
    if (c.analytics) loadGA();
    if (c.marketing) loadMeta();
  }

  // ── Styles ──
  function injectStyles() {
    if (document.getElementById('cc-styles')) return;
    var s = document.createElement('style'); s.id = 'cc-styles';
    s.textContent =
      ':root{--cc-bg:#fff;--cc-ink:#18181b;--cc-muted:#71717a;--cc-border:#e4e4e7;--cc-blue:#2563eb;--cc-blue-soft:#eff3ff;--cc-green:#22c55e;--cc-r:14px}' +
      '.cc-overlay{position:fixed;inset:0;background:rgba(0,0,0,.45);backdrop-filter:blur(4px);z-index:99998;opacity:0;transition:opacity .3s}.cc-overlay.cc-show{opacity:1}' +
      '.cc-box{position:fixed;bottom:28px;left:50%;transform:translateX(-50%) translateY(24px);z-index:99999;background:var(--cc-bg);border-radius:var(--cc-r);' +
        'box-shadow:0 20px 60px rgba(0,0,0,.14),0 0 0 1px rgba(0,0,0,.04);width:480px;max-width:calc(100% - 24px);max-height:calc(100vh - 56px);overflow:hidden;' +
        'opacity:0;transition:all .4s cubic-bezier(.4,0,.2,1);font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;display:flex;flex-direction:column}' +
      '.cc-box.cc-show{opacity:1;transform:translateX(-50%) translateY(0)}' +
      '.cc-box *{box-sizing:border-box}' +
      /* Header */
      '.cc-hdr{padding:28px 28px 0;flex-shrink:0}' +
      '.cc-hdr__icon{width:44px;height:44px;border-radius:12px;background:var(--cc-blue-soft);display:flex;align-items:center;justify-content:center;margin-bottom:14px}' +
      '.cc-hdr__icon svg{width:22px;height:22px;stroke:var(--cc-blue);stroke-width:2;fill:none}' +
      '.cc-hdr__title{font-size:1.1rem;font-weight:700;color:var(--cc-ink);margin-bottom:6px}' +
      '.cc-hdr__text{font-size:.82rem;color:var(--cc-muted);line-height:1.6}' +
      '.cc-hdr__text a{color:var(--cc-blue);text-decoration:underline}' +
      /* Main view buttons */
      '.cc-main-btns{padding:20px 28px 24px;display:flex;flex-direction:column;gap:8px;flex-shrink:0}' +
      '.cc-btn{padding:12px 16px;border-radius:10px;font-size:.88rem;font-weight:600;cursor:pointer;border:none;transition:all .15s;font-family:inherit;text-align:center;width:100%}' +
      '.cc-btn--accept{background:var(--cc-ink);color:#fff}.cc-btn--accept:hover{background:var(--cc-blue)}' +
      '.cc-btn--decline{background:#f4f4f5;color:#52525b}.cc-btn--decline:hover{background:#e4e4e7;color:var(--cc-ink)}' +
      '.cc-btn--manage{background:none;color:var(--cc-blue);padding:8px 16px;font-size:.82rem}.cc-btn--manage:hover{text-decoration:underline}' +
      '.cc-btn--save{background:var(--cc-blue);color:#fff}.cc-btn--save:hover{background:#1d4ed8}' +
      '.cc-btn--back{background:none;color:var(--cc-muted);padding:8px 16px;font-size:.82rem}.cc-btn--back:hover{color:var(--cc-ink)}' +
      /* Preferences view */
      '.cc-prefs{padding:0 28px;overflow-y:auto;flex:1}' +
      '.cc-cat{padding:16px 0;border-bottom:1px solid var(--cc-border)}' +
      '.cc-cat:last-child{border-bottom:none}' +
      '.cc-cat__row{display:flex;align-items:center;justify-content:space-between;gap:12px}' +
      '.cc-cat__info{flex:1;min-width:0}' +
      '.cc-cat__name{font-size:.88rem;font-weight:600;color:var(--cc-ink);margin-bottom:2px}' +
      '.cc-cat__desc{font-size:.78rem;color:var(--cc-muted);line-height:1.5}' +
      '.cc-cat__badge{font-size:.65rem;font-weight:700;color:var(--cc-green);background:rgba(34,197,94,.08);padding:2px 7px;border-radius:6px;white-space:nowrap}' +
      /* Toggle */
      '.cc-toggle{position:relative;width:44px;height:24px;flex-shrink:0}' +
      '.cc-toggle input{opacity:0;width:0;height:0;position:absolute}' +
      '.cc-toggle__track{position:absolute;inset:0;background:#d4d4d8;border-radius:12px;cursor:pointer;transition:background .2s}' +
      '.cc-toggle__thumb{position:absolute;top:2px;left:2px;width:20px;height:20px;background:#fff;border-radius:50%;box-shadow:0 1px 3px rgba(0,0,0,.12);transition:transform .2s}' +
      '.cc-toggle input:checked+.cc-toggle__track{background:var(--cc-blue)}' +
      '.cc-toggle input:checked+.cc-toggle__track .cc-toggle__thumb{transform:translateX(20px)}' +
      '.cc-toggle input:disabled+.cc-toggle__track{background:var(--cc-green);cursor:default}' +
      '.cc-toggle input:disabled+.cc-toggle__track .cc-toggle__thumb{transform:translateX(20px)}' +
      /* Prefs footer */
      '.cc-prefs-btns{padding:16px 28px 24px;display:flex;gap:8px;flex-shrink:0}' +
      /* Responsive */
      '@media(max-width:480px){.cc-box{bottom:12px;width:calc(100% - 16px)}.cc-hdr{padding:22px 20px 0}.cc-main-btns,.cc-prefs-btns{padding-left:20px;padding-right:20px}.cc-prefs{padding:0 20px}}';
    document.head.appendChild(s);
  }

  // ── Build popup ──
  function showPopup(startOnPrefs) {
    if (document.getElementById('ccBox')) return;
    injectStyles();

    var overlay = document.createElement('div');
    overlay.className = 'cc-overlay'; overlay.id = 'ccOverlay';
    document.body.appendChild(overlay);

    var box = document.createElement('div');
    box.className = 'cc-box'; box.id = 'ccBox';

    // Header (shared)
    var hdr =
      '<div class="cc-hdr">' +
        '<div class="cc-hdr__icon"><svg viewBox="0 0 24 24"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="M9 12l2 2 4-4"/></svg></div>' +
        '<div class="cc-hdr__title">Your privacy matters</div>' +
        '<div class="cc-hdr__text">We use cookies to keep Protevio running (necessary), understand how you use the site (analytics), and show relevant content (marketing). You choose what to allow. <a href="/privacy-policy.html">Privacy Policy</a></div>' +
      '</div>';

    // Main view
    var mainView =
      '<div id="ccMain">' +
        hdr +
        '<div class="cc-main-btns">' +
          '<button class="cc-btn cc-btn--accept" id="ccAcceptAll">Accept all</button>' +
          '<button class="cc-btn cc-btn--decline" id="ccDeclineAll">Necessary only</button>' +
          '<button class="cc-btn cc-btn--manage" id="ccManageBtn">Customize preferences</button>' +
        '</div>' +
      '</div>';

    // Get current consent for default toggle states
    var current = getConsent() || { necessary: true, analytics: false, marketing: false };

    // Preferences view
    var prefsView =
      '<div id="ccPrefs" style="display:none;flex-direction:column;flex:1;overflow:hidden">' +
        hdr.replace('Your privacy matters', 'Cookie preferences') +
        '<div class="cc-prefs">' +
          /* Necessary */
          '<div class="cc-cat">' +
            '<div class="cc-cat__row">' +
              '<div class="cc-cat__info">' +
                '<div class="cc-cat__name">Necessary</div>' +
                '<div class="cc-cat__desc">Essential for the site to function. Authentication, security, and your preferences. These cannot be disabled.</div>' +
              '</div>' +
              '<span class="cc-cat__badge">Always on</span>' +
              '<label class="cc-toggle"><input type="checkbox" checked disabled><span class="cc-toggle__track"><span class="cc-toggle__thumb"></span></span></label>' +
            '</div>' +
          '</div>' +
          /* Analytics */
          '<div class="cc-cat">' +
            '<div class="cc-cat__row">' +
              '<div class="cc-cat__info">' +
                '<div class="cc-cat__name">Analytics</div>' +
                '<div class="cc-cat__desc">Help us understand how visitors interact with our site. This includes Google Analytics for page views, sessions, and general usage patterns. All data is anonymized.</div>' +
              '</div>' +
              '<label class="cc-toggle"><input type="checkbox" id="ccToggleAnalytics"' + (current.analytics ? ' checked' : '') + '><span class="cc-toggle__track"><span class="cc-toggle__thumb"></span></span></label>' +
            '</div>' +
          '</div>' +
          /* Marketing */
          '<div class="cc-cat">' +
            '<div class="cc-cat__row">' +
              '<div class="cc-cat__info">' +
                '<div class="cc-cat__name">Marketing</div>' +
                '<div class="cc-cat__desc">Used to deliver relevant advertisements and track campaign effectiveness. This includes Meta Pixel and similar tools. You can opt out at any time.</div>' +
              '</div>' +
              '<label class="cc-toggle"><input type="checkbox" id="ccToggleMarketing"' + (current.marketing ? ' checked' : '') + '><span class="cc-toggle__track"><span class="cc-toggle__thumb"></span></span></label>' +
            '</div>' +
          '</div>' +
        '</div>' +
        '<div class="cc-prefs-btns">' +
          '<button class="cc-btn cc-btn--back" id="ccBackBtn">&larr; Back</button>' +
          '<button class="cc-btn cc-btn--save" id="ccSaveBtn" style="flex:1">Save preferences</button>' +
        '</div>' +
      '</div>';

    box.innerHTML = mainView + prefsView;
    document.body.appendChild(box);

    // Animate in
    requestAnimationFrame(function() {
      requestAnimationFrame(function() {
        overlay.classList.add('cc-show');
        box.classList.add('cc-show');
        if (startOnPrefs) switchTo('ccPrefs');
      });
    });

    // ── View switching ──
    function switchTo(viewId) {
      document.getElementById('ccMain').style.display = viewId === 'ccMain' ? '' : 'none';
      var prefs = document.getElementById('ccPrefs');
      prefs.style.display = viewId === 'ccPrefs' ? 'flex' : 'none';
    }

    // ── Close ──
    function close(consent) {
      box.classList.remove('cc-show');
      overlay.classList.remove('cc-show');
      setTimeout(function() { box.remove(); overlay.remove(); }, 350);
      saveConsent(consent);
      applyConsent(consent);
    }

    // ── Event handlers ──
    document.getElementById('ccAcceptAll').addEventListener('click', function() {
      close({ necessary: true, analytics: true, marketing: true });
    });

    document.getElementById('ccDeclineAll').addEventListener('click', function() {
      close({ necessary: true, analytics: false, marketing: false });
    });

    document.getElementById('ccManageBtn').addEventListener('click', function() {
      switchTo('ccPrefs');
    });

    document.getElementById('ccBackBtn').addEventListener('click', function() {
      switchTo('ccMain');
    });

    document.getElementById('ccSaveBtn').addEventListener('click', function() {
      close({
        necessary: true,
        analytics: document.getElementById('ccToggleAnalytics').checked,
        marketing: document.getElementById('ccToggleMarketing').checked
      });
    });

    overlay.addEventListener('click', function() {
      close({ necessary: true, analytics: false, marketing: false });
    });
  }

  // ── "Manage cookies" links ──
  function bindManageLinks() {
    document.querySelectorAll('[data-cc-manage]').forEach(function(el) {
      el.addEventListener('click', function(e) {
        e.preventDefault();
        if (!document.getElementById('ccBox')) showPopup(true);
      });
    });
  }

  // ── Init ──
  function init() {
    var consent = getConsent();
    if (consent) {
      applyConsent(consent);
    } else {
      showPopup(false);
    }
    bindManageLinks();
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
