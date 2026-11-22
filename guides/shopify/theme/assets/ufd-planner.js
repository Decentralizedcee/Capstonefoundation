(function () {
'use strict';
var U = window.UFD, $ = U.$, $$ = U.$$, h = U.h, store = U.store;
var today = new Date(); today = new Date(today.getFullYear(), today.getMonth(), today.getDate());
var PHASES = [
{ key: 'rest', name: 'Rest', season: 'Inner winter', plain: 'menstrual phase', color: '#4A2A39', ink: '#F7F1EA',
feel: 'You may feel slower and quieter. Your body may be asking for softness.',
move: 'Gentle walks, slow stretching, an early night.',
nourish: 'Warm meals and warm cups, nothing rushed. Eat what comforts you.',
rituals: ['Say no to one extra thing', 'A warm bath or a long, slow shower', 'Phone out of the bedroom tonight', 'One slow morning with your Divine Elixir'],
perm: 'Rest is not a pause in your life. It is part of it.',
what: 'The days of your period. Your cycle begins on the first day of bleeding, so day 1 is where your month starts. This is your season for slowing down.' },
{ key: 'rise', name: 'Rise', season: 'Inner spring', plain: 'follicular phase', color: '#E2C994', ink: '#3B1F2B',
feel: 'You may feel lighter and more curious. New ideas and a little more energy often arrive.',
move: 'Walks outside, a class you have wanted to try, something playful.',
nourish: 'Fresh colours on your plate and plenty of water.',
rituals: ['Begin the thing you have been postponing', 'Plan your week on paper', 'Take your morning ritual outside', 'Try one new thing, however small'],
perm: 'Begin small. Begin now.',
what: 'The days after your period, as you begin to feel lighter. You may notice your energy and curiosity returning.' },
{ key: 'bloom', name: 'Bloom', season: 'Inner summer', plain: 'ovulatory phase', color: '#D8A7A0', ink: '#3B1F2B',
feel: 'You may feel open and warm. Connection and conversation can feel easier.',
move: 'Move with energy: dance, a brisk walk, a longer session, whatever you enjoy.',
nourish: 'Light, colourful food, shared with someone you like.',
rituals: ['Have the conversation that matters', 'Dress entirely for yourself', 'Say yes to a gathering', 'Write down what you are proud of'],
perm: 'Take up space, softly.',
what: 'The middle of your cycle. You may feel more open, social and confident.' },
{ key: 'restore', name: 'Restore', season: 'Inner autumn', plain: 'luteal phase', color: '#B79AA6', ink: '#3B1F2B',
feel: 'You may feel more inward and detail-minded. Order and comfort can matter more to you.',
move: 'Steady strength, pilates, yoga, long unhurried walks.',
nourish: 'Grounding, comforting meals at regular times.',
rituals: ['Tidy one small space', 'Journal what you need right now', 'Protect your evenings', 'Slow your morning ritual down'],
perm: 'You are allowed to need more softness.',
what: 'The days before your next period. A more inward time, when you may want order, comfort and a little extra rest.' }
];
var MOODS = ['Calm', 'Tender', 'Bright', 'Tired', 'Grounded', 'Restless'];
var isApple = /iPhone|iPad|iPod|Macintosh/.test(navigator.userAgent);
var S = Object.assign({ start: U.ymd(U.addDays(today, -9)), L: 28, P: 5, example: true, discreet: true, cycles: 3, tab: null }, store.get('planner.state', {}));
var logs = store.get('planner.logs', {});
var checks = store.get('planner.checks', {});
var view = new Date(today.getFullYear(), today.getMonth(), 1);
var sel = U.ymd(today);
function save() { store.set('planner.state', S); }
function bounds() {
var L = S.L, P = Math.min(S.P, L - 12);
var riseEnd = Math.max(P + 1, Math.floor(L * 0.45));
var bloomEnd = Math.min(riseEnd + 4, L - 2);
return { P: P, riseEnd: riseEnd, bloomEnd: bloomEnd };
}
function cycleDay(d) { var diff = U.diffDays(U.parse(S.start), d); return (((diff % S.L) + S.L) % S.L) + 1; }
function phaseIdx(c) { var b = bounds(); return c <= b.P ? 0 : c <= b.riseEnd ? 1 : c <= b.bloomEnd ? 2 : 3; }
function cycleStart(d) { return U.addDays(d, -(cycleDay(d) - 1)); }
function segments(start) {
var b = bounds(), L = S.L;
return [[0, 1, b.P], [1, b.P + 1, b.riseEnd], [2, b.riseEnd + 1, b.bloomEnd], [3, b.bloomEnd + 1, L]].map(function (s) {
return { idx: s[0], from: s[1], to: s[2], start: U.addDays(start, s[1] - 1), end: U.addDays(start, s[2]) };
});
}
function fmt(d, o) { return d.toLocaleDateString(undefined, o || { day: 'numeric', month: 'short' }); }
function fmtLong(d) { return d.toLocaleDateString(undefined, { weekday: 'long', day: 'numeric', month: 'long' }); }
var sStart = $('#s-start'), sLen = $('#s-len'), sPer = $('#s-per');
sStart.max = U.ymd(today);
function syncInputs() {
sStart.value = S.start; sLen.value = S.L; sPer.value = S.P;
$('#o-len').textContent = S.L; $('#o-per').textContent = S.P;
$('#example-banner').hidden = !S.example;
sPer.max = Math.min(8, S.L - 12);
}
sStart.addEventListener('change', function () { if (!sStart.value) return; S.start = sStart.value; S.example = false; save(); renderAll(); });
$('#s-today').addEventListener('click', function () { S.start = U.ymd(today); S.example = false; save(); renderAll(); });
sLen.addEventListener('input', function () { S.L = +sLen.value; if (S.P > S.L - 12) S.P = S.L - 12; save(); renderAll(); });
sPer.addEventListener('input', function () { S.P = +sPer.value; save(); renderAll(); });
function renderToday() {
var c = cycleDay(today), pi = phaseIdx(c), p = PHASES[pi];
$('#t-day').textContent = c; $('#t-of').textContent = 'of ' + S.L;
$('#t-arc').style.strokeDashoffset = String(289 * (1 - c / S.L));
$('#t-season').textContent = p.season + ' · ' + p.plain;
$('#t-phase').textContent = p.name;
$('#t-feel').textContent = p.feel + ' ' + p.perm;
var segs = segments(cycleStart(today));
var nextStart = pi === 3 ? U.addDays(cycleStart(today), S.L) : segs[pi + 1].start;
var n = U.diffDays(today, nextStart);
$('#t-next').textContent = PHASES[(pi + 1) % 4].name + ' begins ' + fmt(nextStart) + ' (in ' + n + (n === 1 ? ' day' : ' days') + ').';
$('#t-link').onclick = function () { S.tab = p.key; save(); renderTabs(); };
}
$('#t-log').addEventListener('click', function () {
sel = U.ymd(today); view = new Date(today.getFullYear(), today.getMonth(), 1); renderMonth(); renderPanel();
$('#month').scrollIntoView({ behavior: 'smooth', block: 'start' });
});
function renderDow() {
var el = $('#dow'); el.textContent = '';
var mon = new Date(2024, 0, 1);
for (var i = 0; i < 7; i++) el.appendChild(h('span', { text: U.addDays(mon, i).toLocaleDateString(undefined, { weekday: 'short' }) }));
}
function renderLegend() {
var el = $('#legend'); el.textContent = '';
PHASES.forEach(function (p) { el.appendChild(h('span', {}, [h('i', { class: 'swatch', style: 'background:' + p.color }), p.name])); });
}
function renderMonth() {
$('#m-title').textContent = view.toLocaleDateString(undefined, { month: 'long', year: 'numeric' });
var g = $('#grid'); g.textContent = '';
var first = new Date(view.getFullYear(), view.getMonth(), 1);
var offset = (first.getDay() + 6) % 7;
var gridStart = U.addDays(first, -offset);
var rows = Math.ceil((offset + new Date(view.getFullYear(), view.getMonth() + 1, 0).getDate()) / 7);
for (var i = 0; i < rows * 7; i++) {
var d = U.addDays(gridStart, i), key = U.ymd(d), c = cycleDay(d), pi = phaseIdx(c);
var cls = 'cell p' + pi + (d.getMonth() !== view.getMonth() ? ' out' : '') + (key === U.ymd(today) ? ' today' : '') + (key === sel ? ' sel' : '');
var b = h('button', { type: 'button', class: cls, 'data-k': key, 'aria-pressed': String(key === sel),
'aria-label': fmtLong(d) + ', day ' + c + ', ' + PHASES[pi].name + (logs[key] ? ', has a note' : ''), title: PHASES[pi].name + ' · day ' + c }, [String(d.getDate())]);
if (logs[key] && (logs[key].energy || logs[key].mood || logs[key].note)) b.appendChild(h('span', { class: 'dot' }));
b.addEventListener('click', onPick);
g.appendChild(b);
}
}
function onPick(e) {
sel = e.currentTarget.dataset.k; var d = U.parse(sel);
if (d.getMonth() !== view.getMonth()) view = new Date(d.getFullYear(), d.getMonth(), 1);
renderMonth(); renderPanel();
}
$('#m-prev').addEventListener('click', function () { view = new Date(view.getFullYear(), view.getMonth() - 1, 1); renderMonth(); });
$('#m-next').addEventListener('click', function () { view = new Date(view.getFullYear(), view.getMonth() + 1, 1); renderMonth(); });
$('#m-today').addEventListener('click', function () { view = new Date(today.getFullYear(), today.getMonth(), 1); sel = U.ymd(today); renderMonth(); renderPanel(); });
var eBox = $('#d-energy'), mBox = $('#d-mood'), note = $('#d-note');
[1, 2, 3, 4, 5].forEach(function (n) {
var b = h('button', { type: 'button', class: 'chip', 'data-n': n, 'aria-pressed': 'false', 'aria-label': 'Energy ' + n, text: String(n) });
b.addEventListener('click', function () { var l = getLog(); l.energy = l.energy === n ? 0 : n; putLog(l); });
eBox.appendChild(b);
});
MOODS.forEach(function (m) {
var b = h('button', { type: 'button', class: 'chip', 'data-m': m, 'aria-pressed': 'false', text: m });
b.addEventListener('click', function () { var l = getLog(); l.mood = l.mood === m ? '' : m; putLog(l); });
mBox.appendChild(b);
});
note.addEventListener('input', function () { var l = getLog(); l.note = note.value; putLog(l, true); });
function getLog() { return Object.assign({ energy: 0, mood: '', note: '' }, logs[sel] || {}); }
function putLog(l, quiet) {
if (!l.energy && !l.mood && !l.note) delete logs[sel]; else logs[sel] = l;
store.set('planner.logs', logs);
if (!quiet) renderPanel(true);
renderMonth(); renderStrip();
}
function renderPanel(keepNote) {
var d = U.parse(sel), c = cycleDay(d), p = PHASES[phaseIdx(c)], l = getLog();
$('#d-eyebrow').textContent = p.season + ' · ' + p.name;
$('#d-title').textContent = fmtLong(d);
$('#d-sub').textContent = 'Day ' + c + ' of ' + S.L + '. ' + p.perm;
$$('#d-energy .chip').forEach(function (b) { b.setAttribute('aria-pressed', String(+b.dataset.n === l.energy)); });
$$('#d-mood .chip').forEach(function (b) { b.setAttribute('aria-pressed', String(b.dataset.m === l.mood)); });
if (!keepNote) note.value = l.note;
}
function renderStrip() {
var W = 720, padX = 14, barY = 48, barH = 34, plotTop = 150, plotH = 78, H = 262;
var start = cycleStart(today), segs = segments(start), L = S.L, iw = W - padX * 2;
function x(c) { return padX + ((c - 1) / L) * iw; }
var NS = 'http://www.w3.org/2000/svg';
function el(n, a, t) { var e = document.createElementNS(NS, n); Object.keys(a || {}).forEach(function (k) { e.setAttribute(k, a[k]); }); if (t != null) e.textContent = t; return e; }
var svg = el('svg', { viewBox: '0 0 ' + W + ' ' + H, class: 'strip', role: 'img', 'aria-label': 'Your current cycle: ' + segs.map(function (s) { return PHASES[s.idx].name + ' days ' + s.from + ' to ' + s.to; }).join(', ') });
segs.forEach(function (s) {
var p = PHASES[s.idx], x1 = x(s.from), x2 = x(s.to + 1);
svg.appendChild(el('rect', { x: x1 + 1, y: barY, width: Math.max(0, x2 - x1 - 2), height: barH, fill: p.color, rx: 2 }));
if (x2 - x1 > 70) svg.appendChild(el('text', { x: (x1 + x2) / 2, y: barY + barH / 2 + 4, 'text-anchor': 'middle', 'font-size': 13, 'font-weight': 500, style: 'fill:' + p.ink }, p.name));
svg.appendChild(el('text', { x: x1 + 2, y: barY - 10, class: 'axis' }, fmt(s.start)));
});
for (var c = 1; c <= L; c += (c === 1 ? 6 : 7)) { svg.appendChild(el('text', { x: x(c) + (x(c + 1) - x(c)) / 2, y: barY + barH + 16, 'text-anchor': 'middle', class: 'axis' }, String(c))); }
svg.appendChild(el('text', { x: padX, y: barY + barH + 32, class: 'axis' }, 'Cycle day'));
var tc = cycleDay(today), tx = x(tc) + (x(tc + 1) - x(tc)) / 2;
svg.appendChild(el('path', { d: 'M' + (tx - 7) + ' ' + (barY - 26) + ' L' + (tx + 7) + ' ' + (barY - 26) + ' L' + tx + ' ' + (barY - 14) + ' Z', fill: '#3B1F2B' }));
svg.appendChild(el('line', { x1: tx, y1: barY - 14, x2: tx, y2: barY + barH, stroke: '#3B1F2B', 'stroke-width': 2 }));
svg.appendChild(el('text', { x: padX, y: plotTop - 12, class: 'axis' }, 'Energy you have logged'));
[1, 3, 5].forEach(function (v) {
var y = plotTop + plotH - ((v - 1) / 4) * plotH;
svg.appendChild(el('line', { x1: padX, y1: y, x2: W - padX, y2: y, stroke: '#DCCDBA', 'stroke-width': 1, 'stroke-dasharray': '3 4' }));
svg.appendChild(el('text', { x: W - padX, y: y - 4, 'text-anchor': 'end', class: 'axis' }, String(v)));
});
var n = 0, pts = [];
for (var i = 0; i < L; i++) {
var d = U.addDays(start, i), lg = logs[U.ymd(d)];
if (lg && lg.energy) { pts.push([x(i + 1) + (x(i + 2) - x(i + 1)) / 2, plotTop + plotH - ((lg.energy - 1) / 4) * plotH]); n++; }
}
if (pts.length > 1) svg.appendChild(el('polyline', { points: pts.map(function (p) { return p[0] + ',' + p[1]; }).join(' '), fill: 'none', stroke: '#B8975A', 'stroke-width': 1.5 }));
pts.forEach(function (p) { svg.appendChild(el('circle', { cx: p[0], cy: p[1], r: 5, fill: '#3B1F2B' })); });
if (!n) svg.appendChild(el('text', { x: W / 2, y: plotTop + plotH / 2 + 4, 'text-anchor': 'middle', class: 'axis' }, 'Log your energy in the month view and it appears here.'));
var wrap = $('#strip-wrap'); wrap.textContent = ''; wrap.appendChild(svg);
}
function renderTabs() {
var cur = PHASES[phaseIdx(cycleDay(today))].key;
if (!S.tab) S.tab = cur;
var tabs = $('#tabs'); tabs.textContent = '';
PHASES.forEach(function (p) {
var b = h('button', { type: 'button', class: 'tab', role: 'tab', id: 'tab-' + p.key, 'aria-selected': String(S.tab === p.key), 'aria-controls': 'pb-panel' }, [p.name, p.key === cur ? h('span', { class: 'now', text: 'now' }) : null]);
b.addEventListener('click', function () { S.tab = p.key; save(); renderTabs(); });
b.addEventListener('keydown', function (e) {
var i = PHASES.findIndex(function (x) { return x.key === S.tab; });
if (e.key === 'ArrowRight' || e.key === 'ArrowLeft') { e.preventDefault(); i = (i + (e.key === 'ArrowRight' ? 1 : 3)) % 4; S.tab = PHASES[i].key; save(); renderTabs(); $('#tab-' + S.tab).focus(); }
});
tabs.appendChild(b);
});
var p = PHASES.filter(function (x) { return x.key === S.tab; })[0], pi = PHASES.indexOf(p);
var seg = segments(cycleStart(today))[pi];
var panel = $('#pb-panel'); panel.textContent = '';
panel.setAttribute('aria-labelledby', 'tab-' + p.key);
panel.appendChild(h('div', { class: 'stack', style: 'margin-bottom:1.8rem' }, [
h('p', { class: 'eyebrow' }, [h('i', { class: 'swatch', style: 'background:' + p.color }), p.season + ' · ' + p.plain]),
h('h3', { class: 'it gold-it', text: p.name }),
h('p', { class: 'muted small', text: 'This cycle: ' + fmt(seg.start) + ' to ' + fmt(U.addDays(seg.end, -1)) + ' (days ' + seg.from + ' to ' + seg.to + ')' }),
h('p', { text: p.feel })
]));
var ul = h('ul', { class: 'checklist' });
p.rituals.forEach(function (r, i) {
var id = 'ck-' + p.key + i, cb = h('input', { type: 'checkbox', id: id });
cb.checked = !!checks[p.key + i];
cb.addEventListener('change', function () { if (cb.checked) checks[p.key + i] = 1; else delete checks[p.key + i]; store.set('planner.checks', checks); });
ul.appendChild(h('li', {}, [h('label', { class: 'check', for: id }, [cb, h('span', { text: r })])]));
});
panel.appendChild(h('div', { class: 'pb' }, [
h('div', {}, [h('h4', { text: 'Move' }), h('p', { text: p.move })]),
h('div', {}, [h('h4', { text: 'Nourish' }), h('p', { text: p.nourish })]),
h('div', {}, [h('h4', { text: 'Ritual ideas' }), ul])
]));
panel.appendChild(h('p', { class: 'quote', style: 'margin-top:2rem;font-size:1.8rem', text: '“' + p.perm + '”' }));
}
function buildEvents() {
var out = [], start = cycleStart(today);
for (var c = 0; c < S.cycles; c++) {
var cs = U.addDays(start, c * S.L);
segments(cs).forEach(function (s) {
var p = PHASES[s.idx];
out.push({ uid: 'phase-' + U.ymd(s.start) + '-' + p.key, allDay: true, start: s.start, endExclusive: s.end,
title: S.discreet ? 'Une Femme Divine · ' + p.season : p.name + ' · ' + p.plain,
details: p.season + '. ' + p.feel + ' ' + p.perm + ' (Une Femme Divine, Rhythm of the Body)' });
});
}
return out;
}
function renderSync() {
$('#x-cycles').value = String(S.cycles); $('#x-discreet').checked = S.discreet;
var list = $('#x-list'); list.textContent = '';
buildEvents().filter(function (e) { return U.diffDays(today, U.addDays(e.endExclusive, -1)) >= 0; }).slice(0, 6).forEach(function (e) {
var last = U.addDays(e.endExclusive, -1);
list.appendChild(h('li', {}, [
h('span', {}, [h('b', { text: e.title }), h('span', { class: 'when', text: fmt(e.start) + (U.diffDays(e.start, last) ? ' to ' + fmt(last) : '') })]),
h('a', { class: 'btn small' + (isApple ? ' ghost' : ''), href: U.googleLink(e), target: '_blank', rel: 'noopener', 'aria-label': 'Add ' + e.title + ' to Google Calendar', text: 'Add' })
]));
});
}
$('#x-cycles').addEventListener('change', function (e) { S.cycles = +e.target.value; save(); renderSync(); });
$('#x-discreet').addEventListener('change', function (e) { S.discreet = e.target.checked; save(); renderSync(); });
var xi = $('#x-ics');
if (xi) xi.addEventListener('click', function () { U.downloadFile('rhythm-of-the-body.ics', U.buildICS(buildEvents(), 'Une Femme Divine · Rhythm of the Body')); });
$('#x-copy').addEventListener('click', function () { U.copy(U.buildICS(buildEvents(), 'Une Femme Divine · Rhythm of the Body'), 'Calendar file copied. Paste it into a .ics file to import.', $('#x-box')); });
var wipe = $('#wipe'), wt;
wipe.addEventListener('click', function () {
if (!wipe.dataset.sure) {
wipe.dataset.sure = '1'; wipe.textContent = 'Tap again to clear everything';
wt = setTimeout(function () { delete wipe.dataset.sure; wipe.textContent = 'Clear my planner data from this device'; }, 4000); return;
}
clearTimeout(wt);
['planner.state', 'planner.logs', 'planner.checks'].forEach(function (k) { store.del(k); });
S = { start: U.ymd(U.addDays(today, -9)), L: 28, P: 5, example: true, discreet: true, cycles: 3, tab: null }; logs = {}; checks = {};
delete wipe.dataset.sure; wipe.textContent = 'Clear my planner data from this device';
renderAll(); U.toast('Your planner data was cleared');
});
function renderExplain() {
var wrap = $('#explain'); wrap.textContent = '';
segments(cycleStart(today)).forEach(function (s) {
var p = PHASES[s.idx];
wrap.appendChild(h('div', { class: 'xcard' }, [
h('p', { class: 'eyebrow' }, [h('i', { class: 'swatch', style: 'background:' + p.color }), p.season]),
h('h4', { text: p.name }),
h('p', { class: 'small muted', text: 'Days ' + s.from + ' to ' + s.to + ' of your ' + S.L + '-day cycle' }),
h('p', { text: p.what }),
h('p', { class: 'small', text: p.feel })
]));
});
}
function renderDevice() {
var hint = $('#x-hint'), ics = $('#x-ics');
if (hint) hint.textContent = isApple ? 'Tap the button, then choose Add All to put every season in your Apple Calendar.' : 'Tap Add next to a season to put it in your Google Calendar. Using Apple or Outlook? Download the file instead.';
if (ics) ics.className = isApple ? 'btn' : 'btn ghost';
}
function recordRows() {
return Object.keys(logs).sort().map(function (k) {
var c = cycleDay(U.parse(k)), l = logs[k];
return [k, c, PHASES[phaseIdx(c)].name, l.energy || '', l.mood || '', l.note || ''];
});
}
function recordCSV() {
var q = function (v) { return '"' + String(v).replace(/"/g, '""') + '"'; };
var rows = [['Date', 'Cycle day', 'Season', 'Energy (1-5)', 'Mood', 'Notes']].concat(recordRows());
return '\ufeff' + rows.map(function (r) { return r.map(q).join(','); }).join('\r\n');
}
function buildRecord() {
var rec = $('#record');
if (!rec) { rec = h('div', { id: 'record' }); document.body.appendChild(rec); }
rec.textContent = '';
rec.appendChild(h('h1', { text: 'My rhythm record' }));
rec.appendChild(h('p', { text: 'Une Femme Divine \u00B7 Rhythm of the Body. First day of your last period: ' + fmt(U.parse(S.start), { day: 'numeric', month: 'long', year: 'numeric' }) + '. Your cycle: ' + S.L + ' days, period: ' + S.P + ' days.' }));
rec.appendChild(h('h2', { text: 'Your seasons this cycle' }));
var t1 = h('table', {}, [h('tr', {}, ['Season', 'Days', 'Dates'].map(function (x) { return h('th', { text: x }); }))]);
segments(cycleStart(today)).forEach(function (s) {
t1.appendChild(h('tr', {}, [PHASES[s.idx].name + ' (' + PHASES[s.idx].season + ')', s.from + ' to ' + s.to, fmt(s.start) + ' to ' + fmt(U.addDays(s.end, -1))].map(function (x) { return h('td', { text: x }); })));
});
rec.appendChild(t1);
rec.appendChild(h('h2', { text: 'What you logged' }));
var rows = recordRows();
if (!rows.length) rec.appendChild(h('p', { text: 'You have not logged any days yet.' }));
else {
var t2 = h('table', {}, [h('tr', {}, ['Date', 'Day', 'Season', 'Energy', 'Mood', 'Notes'].map(function (x) { return h('th', { text: x }); }))]);
rows.forEach(function (r) { t2.appendChild(h('tr', {}, [fmt(U.parse(r[0]), { day: 'numeric', month: 'short', year: 'numeric' }), r[1], r[2], r[3], r[4], r[5]].map(function (x) { return h('td', { text: String(x) }); }))); });
rec.appendChild(t2);
}
rec.appendChild(h('p', { style: 'margin-top:18pt;color:#555', text: 'This is a lifestyle record for you. It is not medical advice.' }));
}
var rCsv = $('#r-csv'), rPrint = $('#r-print');
if (rCsv) rCsv.addEventListener('click', function () {
if (!recordRows().length) { U.toast('Log a day first, then download your record.'); return; }
U.downloadFile('my-rhythm-record.csv', recordCSV(), 'text/csv;charset=utf-8');
});
if (rPrint) rPrint.addEventListener('click', function () {
buildRecord(); document.body.classList.add('record-print');
try { window.print(); } catch (e) { U.toast('Printing is not available here'); }
setTimeout(function () { document.body.classList.remove('record-print'); }, 1500);
});
window.addEventListener('afterprint', function () { document.body.classList.remove('record-print'); });
function renderAll() { syncInputs(); renderToday(); renderMonth(); renderPanel(); renderStrip(); renderExplain(); renderTabs(); renderSync(); renderDevice(); }
renderDow(); renderLegend(); renderAll();
if ('IntersectionObserver' in window) {
var links = {}; $$('#topnav a').forEach(function (a) { links[a.getAttribute('href').slice(1)] = a; });
var io = new IntersectionObserver(function (es) {
es.forEach(function (e) { if (e.isIntersecting && links[e.target.id]) { $$('#topnav a').forEach(function (a) { a.classList.remove('on'); }); links[e.target.id].classList.add('on'); } });
}, { rootMargin: '-45% 0px -50% 0px' });
Object.keys(links).forEach(function (id) { var s = document.getElementById(id); if (s) io.observe(s); });
}
})();