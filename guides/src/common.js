/* Une Femme Divine guides: shared helpers (storage, toast, calendar files, email gate). No dependencies. */
(function () {
  'use strict';

  var C = Object.assign({
    provider: 'none',            // 'shopify' | 'webhook' | 'none'
    shopDomain: '',              // e.g. une-femme-divine.myshopify.com (provider: 'shopify')
    webhookUrl: '',              // e.g. a Klaviyo / Mailchimp / Make / Zapier endpoint (provider: 'webhook')
    tags: 'guide,newsletter',
    guideId: 'guide',
    contactEmail: 'marketing@unefemmedivine.com',
    otherGuideUrl: '',
    shopUrl: ''
  }, window.UFD_CONFIG || {});

  /* ---------- storage that never throws ---------- */
  var mem = {};
  var store = {
    get: function (k, d) {
      try { var v = window.localStorage.getItem('ufd:' + k); return v == null ? (k in mem ? mem[k] : d) : JSON.parse(v); } catch (e) { return k in mem ? mem[k] : d; }
    },
    set: function (k, v) {
      mem[k] = v;
      try { window.localStorage.setItem('ufd:' + k, JSON.stringify(v)); } catch (e) { /* private mode: keep in memory */ }
    },
    del: function (k) {
      delete mem[k];
      try { window.localStorage.removeItem('ufd:' + k); } catch (e) { /* ignore */ }
    }
  };

  /* ---------- dom helpers ---------- */
  function $(s, r) { return (r || document).querySelector(s); }
  function $$(s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); }
  function h(tag, attrs, kids) {
    var el = document.createElement(tag);
    Object.keys(attrs || {}).forEach(function (k) {
      var v = attrs[k];
      if (v == null || v === false) return;
      if (k === 'class') el.className = v;
      else if (k === 'text') el.textContent = v;
      else if (k.slice(0, 2) === 'on') el.addEventListener(k.slice(2), v);
      else el.setAttribute(k, v === true ? '' : v);
    });
    (kids || []).forEach(function (c) { if (c != null) el.appendChild(typeof c === 'string' ? document.createTextNode(c) : c); });
    return el;
  }

  var toastEl, toastT;
  function toast(msg) {
    if (!toastEl) { toastEl = h('div', { class: 'toast', role: 'status', 'aria-live': 'polite' }); document.body.appendChild(toastEl); }
    toastEl.textContent = msg; toastEl.classList.add('on');
    clearTimeout(toastT); toastT = setTimeout(function () { toastEl.classList.remove('on'); }, 2600);
  }

  function copy(text, okMsg, box) {
    function fallback() {
      if (box) { box.hidden = false; box.value = text; box.focus(); box.select(); toast('Select and copy the text below'); }
      else toast('Copy is not available here');
    }
    try {
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).then(function () { toast(okMsg || 'Copied'); }, fallback);
      } else fallback();
    } catch (e) { fallback(); }
  }

  /* ---------- dates ---------- */
  function pad(n) { return (n < 10 ? '0' : '') + n; }
  function ymd(d) { return d.getFullYear() + '-' + pad(d.getMonth() + 1) + '-' + pad(d.getDate()); }
  function compact(d) { return d.getFullYear() + pad(d.getMonth() + 1) + pad(d.getDate()); }
  function parse(s) { var p = String(s).split('-'); return new Date(+p[0], +p[1] - 1, +p[2]); }
  function addDays(d, n) { return new Date(d.getFullYear(), d.getMonth(), d.getDate() + n); }
  function diffDays(a, b) { return Math.round((Date.UTC(b.getFullYear(), b.getMonth(), b.getDate()) - Date.UTC(a.getFullYear(), a.getMonth(), a.getDate())) / 86400000); }
  function stamp() { var n = new Date(); return n.getUTCFullYear() + pad(n.getUTCMonth() + 1) + pad(n.getUTCDate()) + 'T' + pad(n.getUTCHours()) + pad(n.getUTCMinutes()) + pad(n.getUTCSeconds()) + 'Z'; }

  /* ---------- calendar files (.ics) and Google Calendar links ---------- */
  function esc(t) { return String(t).replace(/\\/g, '\\\\').replace(/;/g, '\\;').replace(/,/g, '\\,').replace(/\r?\n/g, '\\n'); }
  function fold(line) {
    var out = [], enc = new TextEncoder(), cur = '', len = 0;
    Array.from(line).forEach(function (ch) {
      var b = enc.encode(ch).length;
      if (len + b > 73) { out.push(cur); cur = ' ' + ch; len = 1 + b; } else { cur += ch; len += b; }
    });
    out.push(cur);
    return out.join('\r\n');
  }
  /* events: [{uid, title, details, allDay:true, start:Date, endExclusive:Date} | {uid, title, details, start:Date, minutes, rrule}] */
  function buildICS(events, calName) {
    var L = ['BEGIN:VCALENDAR', 'VERSION:2.0', 'PRODID:-//Une Femme Divine//Guide//EN', 'CALSCALE:GREGORIAN', 'METHOD:PUBLISH', 'X-WR-CALNAME:' + esc(calName || 'Une Femme Divine')];
    events.forEach(function (e) {
      L.push('BEGIN:VEVENT', 'UID:' + e.uid + '@unefemmedivine', 'DTSTAMP:' + stamp());
      if (e.allDay) {
        L.push('DTSTART;VALUE=DATE:' + compact(e.start), 'DTEND;VALUE=DATE:' + compact(e.endExclusive), 'TRANSP:TRANSPARENT');
      } else {
        var end = new Date(e.start.getTime() + e.minutes * 60000);
        L.push('DTSTART:' + compact(e.start) + 'T' + pad(e.start.getHours()) + pad(e.start.getMinutes()) + '00',
               'DTEND:' + compact(end) + 'T' + pad(end.getHours()) + pad(end.getMinutes()) + '00');
        if (e.rrule) L.push('RRULE:' + e.rrule);
        L.push('BEGIN:VALARM', 'ACTION:DISPLAY', 'DESCRIPTION:' + esc(e.title), 'TRIGGER:PT0M', 'END:VALARM');
      }
      L.push('SUMMARY:' + esc(e.title));
      if (e.details) L.push('DESCRIPTION:' + esc(e.details));
      L.push('END:VEVENT');
    });
    L.push('END:VCALENDAR');
    return L.map(fold).join('\r\n') + '\r\n';
  }
  function downloadFile(name, text, type) {
    try {
      var url = URL.createObjectURL(new Blob([text], { type: type || 'text/calendar;charset=utf-8' }));
      var a = h('a', { href: url, download: name });
      document.body.appendChild(a); a.click(); a.remove();
      setTimeout(function () { URL.revokeObjectURL(url); }, 4000);
      toast('Downloaded: ' + name);
    } catch (e) { toast('Download is not available here. Use Copy instead.'); }
  }
  function googleLink(o) {
    var dates;
    if (o.allDay) dates = compact(o.start) + '/' + compact(o.endExclusive);
    else {
      var end = new Date(o.start.getTime() + o.minutes * 60000);
      dates = compact(o.start) + 'T' + pad(o.start.getHours()) + pad(o.start.getMinutes()) + '00/' + compact(end) + 'T' + pad(end.getHours()) + pad(end.getMinutes()) + '00';
    }
    var q = 'action=TEMPLATE&text=' + encodeURIComponent(o.title) + '&dates=' + dates + '&details=' + encodeURIComponent(o.details || '');
    if (o.rrule) q += '&recur=' + encodeURIComponent('RRULE:' + o.rrule);
    return 'https://calendar.google.com/calendar/render?' + q;
  }

  /* ---------- email gate ---------- */
  var KEY = 'access';
  function unlock(name) {
    $$('[data-locked]').forEach(function (el) { el.hidden = false; });
    var g = $('#gate-wrap'); if (g) g.hidden = true;
    document.body.classList.add('unlocked');
    $$('[data-name]').forEach(function (el) { if (name) el.textContent = name; });
    $$('[data-greet]').forEach(function (el) { if (name) { el.textContent = 'Welcome, ' + name + '.'; el.hidden = false; } });
    document.dispatchEvent(new CustomEvent('ufd:unlocked'));
  }
  function send(payload) {
    try {
      if (C.provider === 'shopify' && C.shopDomain) {
        var fd = new FormData();
        fd.append('form_type', 'customer'); fd.append('utf8', '\u2713');
        fd.append('contact[email]', payload.email);
        if (payload.name) fd.append('contact[first_name]', payload.name);
        fd.append('contact[tags]', C.tags);
        return fetch('https://' + C.shopDomain + '/contact#contact_form', { method: 'POST', mode: 'no-cors', body: fd });
      }
      if (C.provider === 'webhook' && C.webhookUrl) {
        return fetch(C.webhookUrl, { method: 'POST', mode: 'no-cors', headers: { 'Content-Type': 'text/plain' }, body: JSON.stringify(Object.assign({ tags: C.tags, source: C.guideId, consent: true }, payload)) });
      }
    } catch (e) { /* never block the guest */ }
    return Promise.resolve();
  }
  function initGate() {
    var saved = store.get(KEY, null);
    if (saved) { unlock(saved.name); return; }
    var form = $('#gate-form'); if (!form) return;
    var err = $('#gate-err');
    form.addEventListener('submit', function (ev) {
      ev.preventDefault();
      var name = form.elements.name.value.trim(), email = form.elements.email.value.trim();
      if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email)) { err.textContent = 'Please enter a valid email address.'; form.elements.email.focus(); return; }
      if (!form.elements.consent.checked) { err.textContent = 'Please tick the box so we can email you.'; form.elements.consent.focus(); return; }
      err.textContent = '';
      var btn = form.querySelector('button[type=submit]'); btn.disabled = true; btn.textContent = 'Opening your guide...';
      send({ email: email, name: name }).then(function () {}, function () {}).then(function () {
        store.set(KEY, { name: name, at: Date.now() });
        unlock(name);
        var first = $('[data-locked]'); if (first) first.scrollIntoView({ behavior: 'smooth', block: 'start' });
      });
    });
  }

  function initCommon() {
    $$('[data-contact]').forEach(function (el) { el.textContent = C.contactEmail; if (el.tagName === 'A') el.href = 'mailto:' + C.contactEmail; });
    $$('[data-other-guide]').forEach(function (el) { if (C.otherGuideUrl) el.href = C.otherGuideUrl; else el.hidden = true; });
    $$('[data-shop]').forEach(function (el) { if (C.shopUrl) el.href = C.shopUrl; else el.hidden = true; });
    initGate();
  }

  window.UFD = { C: C, store: store, $: $, $$: $$, h: h, toast: toast, copy: copy, pad: pad, ymd: ymd, parse: parse, addDays: addDays, diffDays: diffDays, buildICS: buildICS, downloadFile: downloadFile, googleLink: googleLink };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', initCommon); else initCommon();
})();
