(function () {
  var U = window.UFD, $ = U.$, $$ = U.$$, C = U.C;
  $$('[data-planner-link]').forEach(function (a) { a.href = C.plannerUrl; });
  $$('[data-planner-pdf]').forEach(function (a) { a.href = C.plannerPdf; });
  $$('[data-email-note]').forEach(function (el) { el.hidden = !C.emailFollowUp; });
  document.addEventListener('ufd:unlocked', function () { var t = $('#top-cta'); if (t) { t.textContent = 'Your planner'; t.href = '#get'; } });
})();
