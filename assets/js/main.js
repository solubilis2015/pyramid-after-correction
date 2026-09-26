/* Pyramid Engineering — site behaviour. Vanilla JS, no dependencies. */
(function () {
  'use strict';

  /* ---- Sticky header shadow ------------------------------------------- */
  var header = document.querySelector('.site-header');
  var toTop = document.querySelector('.fl-top');
  function onScroll() {
    var y = window.scrollY || document.documentElement.scrollTop;
    if (header) header.classList.toggle('is-stuck', y > 12);
    if (toTop) toTop.classList.toggle('show', y > 640);
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  if (toTop) {
    toTop.addEventListener('click', function () {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

  /* ---- Mobile navigation ---------------------------------------------- */
  var drawer = document.getElementById('mobile-nav');
  var openers = document.querySelectorAll('[data-nav-toggle]');
  var lastFocused = null;

  function setNav(open) {
    if (!drawer) return;
    drawer.classList.toggle('is-open', open);
    document.body.classList.toggle('nav-open', open);
    openers.forEach(function (b) { b.setAttribute('aria-expanded', String(open)); });
    if (open) {
      lastFocused = document.activeElement;
      var first = drawer.querySelector('a, button');
      if (first) first.focus();
    } else if (lastFocused) {
      lastFocused.focus();
    }
  }
  openers.forEach(function (btn) {
    btn.addEventListener('click', function () {
      setNav(!drawer.classList.contains('is-open'));
    });
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && drawer && drawer.classList.contains('is-open')) setNav(false);
  });
  if (drawer) {
    drawer.addEventListener('click', function (e) {
      if (e.target.tagName === 'A') setNav(false);
    });
    // Trap focus inside the drawer while open
    drawer.addEventListener('keydown', function (e) {
      if (e.key !== 'Tab' || !drawer.classList.contains('is-open')) return;
      var f = drawer.querySelectorAll('a[href], button:not([disabled])');
      if (!f.length) return;
      var first = f[0], last = f[f.length - 1];
      if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
      else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
    });
  }

  /* ---- Scroll reveal --------------------------------------------------- */
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var revealables = document.querySelectorAll('.reveal');
  if (reduce || !('IntersectionObserver' in window)) {
    revealables.forEach(function (el) { el.classList.add('in'); });
  } else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    revealables.forEach(function (el) { io.observe(el); });
  }

  /* ---- Animated counters ---------------------------------------------- */
  var counters = document.querySelectorAll('[data-count]');
  if (counters.length) {
    var run = function (el) {
      var target = parseFloat(el.getAttribute('data-count'));
      var suffix = el.getAttribute('data-suffix') || '';
      var prefix = el.getAttribute('data-prefix') || '';
      if (reduce) { el.textContent = prefix + target + suffix; return; }
      var dur = 1300, t0 = null;
      function step(ts) {
        if (!t0) t0 = ts;
        var p = Math.min((ts - t0) / dur, 1);
        var eased = 1 - Math.pow(1 - p, 3);
        el.textContent = prefix + Math.round(target * eased) + suffix;
        if (p < 1) requestAnimationFrame(step);
      }
      requestAnimationFrame(step);
    };
    if ('IntersectionObserver' in window) {
      var cio = new IntersectionObserver(function (es) {
        es.forEach(function (e) { if (e.isIntersecting) { run(e.target); cio.unobserve(e.target); } });
      }, { threshold: 0.4 });
      counters.forEach(function (c) { cio.observe(c); });
    } else {
      counters.forEach(run);
    }
  }

  /* ---- Project portfolio filter ---------------------------------------- */
  var filterBar = document.querySelector('[data-filters]');
  if (filterBar) {
    var items = Array.prototype.slice.call(document.querySelectorAll('[data-sector]'));
    var empty = document.querySelector('[data-no-results]');
    var countEl = document.querySelector('[data-result-count]');

    function apply(key) {
      var shown = 0;
      items.forEach(function (item) {
        var match = key === 'all' || (item.getAttribute('data-sector') || '').split(' ').indexOf(key) > -1;
        item.hidden = !match;
        if (match) shown++;
      });
      if (empty) empty.hidden = shown !== 0;
      if (countEl) countEl.textContent = shown;
    }

    filterBar.addEventListener('click', function (e) {
      var btn = e.target.closest('button[data-filter]');
      if (!btn) return;
      filterBar.querySelectorAll('button[data-filter]').forEach(function (b) {
        b.setAttribute('aria-pressed', String(b === btn));
      });
      apply(btn.getAttribute('data-filter'));
    });

    // Deep link: projects.html?sector=power
    var q = new URLSearchParams(window.location.search).get('sector');
    if (q) {
      var pre = filterBar.querySelector('button[data-filter="' + q.replace(/"/g, '') + '"]');
      if (pre) pre.click();
    } else {
      apply('all');
    }
  }

  /* ---- Enquiry form: validation, spam guard, Google Sheets submit ------ */
  var form = document.querySelector('[data-enquiry-form]');
  if (form) {
    var status = form.querySelector('[data-form-status]');
    var submitBtn = form.querySelector('[data-submit]');
    var endpoint = (form.getAttribute('data-sheet-endpoint') || '').trim();
    var hasEndpoint = /^https:\/\/script\.google\.com\/macros\/s\/.+\/exec$/.test(endpoint);
    var ENQUIRY_EMAIL = 'enquiry@pyramid-groups.com';
    var SENT_FIELDS = ['name', 'company', 'email', 'phone', 'service', 'sector', 'location', 'message'];

    var val = function (n) { var f = form.elements[n]; return f && f.value ? f.value.trim() : ''; };

    function showStatus(kind, html) {
      if (!status) return;
      status.className = 'form-status form-status--' + kind;
      status.innerHTML = html;
      status.hidden = false;
      status.focus({ preventScroll: true });
      status.scrollIntoView({ behavior: reduce ? 'auto' : 'smooth', block: 'nearest' });
    }

    function mailtoLink(subject, body) {
      return 'mailto:' + ENQUIRY_EMAIL + '?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(body);
    }

    // Mark invalid fields as the visitor fixes them
    form.addEventListener('input', function (e) {
      if (e.target.getAttribute('aria-invalid') === 'true' && e.target.checkValidity()) {
        e.target.removeAttribute('aria-invalid');
      }
    });
    form.addEventListener('change', function (e) {
      if (e.target.type === 'checkbox' && e.target.checked) e.target.removeAttribute('aria-invalid');
    });

    form.addEventListener('submit', function (e) {
      e.preventDefault();

      // Honeypot — silently drop bot submissions
      var hp = form.querySelector('.hp input');
      if (hp && hp.value) return;

      // Time trap — a human takes more than 3 seconds to fill the form
      var started = parseInt(form.getAttribute('data-started') || '0', 10);
      if (started && Date.now() - started < 3000) return;

      // Required fields, email format and consent
      var invalid = Array.prototype.filter.call(form.elements, function (el) {
        return el.willValidate && !el.checkValidity();
      });
      Array.prototype.forEach.call(form.elements, function (el) { el.removeAttribute('aria-invalid'); });
      if (invalid.length) {
        invalid.forEach(function (el) { el.setAttribute('aria-invalid', 'true'); });
        showStatus('error', '<strong>Please check the highlighted fields.</strong> Name, company, a valid email, the scope of work and your consent are required.');
        invalid[0].focus();
        invalid[0].reportValidity();
        return;
      }

      var files = form.elements.drawings && form.elements.drawings.files ? form.elements.drawings.files : [];
      var fileNote = '';
      if (files.length) {
        var names = Array.prototype.map.call(files, function (f) { return f.name; }).join(', ');
        fileNote = '<p>Your drawings or specifications (' + names.replace(/</g, '&lt;') + ') were not uploaded with the form. '
          + '<a href="' + mailtoLink('Drawings — ' + val('company'), 'Please find attached drawings/specifications for our enquiry.\n\nCompany: ' + val('company') + '\nName: ' + val('name')) + '">'
          + 'Email them to ' + ENQUIRY_EMAIL + '</a> and attach the files, quoting your company name.</p>';
      }

      // No Apps Script URL configured yet: fall back to the visitor's email app
      if (!hasEndpoint) {
        var body = [
          'Name: ' + val('name'), 'Company: ' + val('company'), 'Email: ' + val('email'),
          'Phone: ' + val('phone'), 'Service required: ' + val('service'), 'Sector: ' + val('sector'),
          'Site location: ' + val('location'), '', 'Enquiry:', val('message')
        ].join('\n');
        window.location.href = mailtoLink('Website enquiry — ' + (val('service') || 'General') + ' — ' + val('company'), body);
        showStatus('success', 'Opening your email application with the enquiry ready to send. If nothing happens, please email ' + ENQUIRY_EMAIL + ' directly.' + fileNote);
        return;
      }

      // Send as URL-encoded form data (a "simple" request, so no CORS preflight)
      var params = new URLSearchParams();
      SENT_FIELDS.forEach(function (n) { params.append(n, val(n)); });
      params.append('consent', form.elements.consent.checked ? 'yes' : '');
      params.append('website_url', hp ? hp.value : '');
      params.append('page', location.pathname);

      var label = submitBtn ? submitBtn.textContent : '';
      if (submitBtn) { submitBtn.disabled = true; submitBtn.textContent = 'Sending…'; }
      form.setAttribute('aria-busy', 'true');

      fetch(endpoint, { method: 'POST', body: params })
        .then(function (res) { return res.json(); })
        .then(function (data) {
          if (!data || !data.ok) throw new Error((data && data.error) || 'Unknown error');
          form.reset();
          form.setAttribute('data-started', String(Date.now()));
          showStatus('success', '<strong>Thank you — your enquiry has been sent.</strong> We usually reply within one working day.' + fileNote);
        })
        .catch(function () {
          showStatus('error', '<strong>Sorry, your enquiry could not be sent.</strong> Please try again, or email '
            + '<a href="mailto:' + ENQUIRY_EMAIL + '">' + ENQUIRY_EMAIL + '</a> or call <a href="tel:+6562599046">+65 6259 9046</a>.');
        })
        .then(function () {
          if (submitBtn) { submitBtn.disabled = false; submitBtn.textContent = label; }
          form.removeAttribute('aria-busy');
        });
    });

    form.setAttribute('data-started', String(Date.now()));
  }
  /* ---- Services page: banner buttons open + scroll to a service card --- */
  function setService(card, open) {
    var btn = card.querySelector('.svc-acc__btn');
    card.classList.toggle('is-open', open);
    if (btn) btn.setAttribute('aria-expanded', String(open));
  }
  document.querySelectorAll('.svc-acc__btn').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var card = btn.closest('.svc-acc');
      setService(card, !card.classList.contains('is-open'));
    });
  });
  function openService(id, smooth) {
    var card = id && document.getElementById(id);
    if (!card || !card.classList.contains('svc-acc')) return false;
    setService(card, true);
    card.classList.add('in');
    card.scrollIntoView({ behavior: smooth && !reduce ? 'smooth' : 'auto', block: 'start' });
    return true;
  }
  document.querySelectorAll('[data-svc-open]').forEach(function (a) {
    a.addEventListener('click', function (e) {
      var id = a.getAttribute('href').slice(1);
      if (openService(id, true)) {
        e.preventDefault();
        if (history.replaceState) history.replaceState(null, '', '#' + id);
      }
    });
  });
  if (location.hash) openService(location.hash.slice(1), false);

  /* ---- Current year ---------------------------------------------------- */
  document.querySelectorAll('[data-year]').forEach(function (el) {
    el.textContent = new Date().getFullYear();
  });
})();
