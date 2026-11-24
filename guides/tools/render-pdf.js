// Renders guides/_print/*.html to PDF with Chrome and dumps the position of every fillable field.
// usage: NODE_PATH=$(npm root -g) node guides/tools/render-pdf.js
const { chromium } = require('playwright');
const path = require('path'), fs = require('fs');
const ROOT = path.resolve(__dirname, '..');
(async () => {
  const b = await chromium.launch();
  for (const [src, name] of [['ritual', 'Your-Divine-Ritual'], ['planner', 'Rhythm-of-the-Body'], ['partner', 'Divine-Ritual-Pack-Partner'], ['pitch', 'Une-Femme-Divine-Partner-Pitch']]) {
    const p = await b.newPage({ viewport: { width: 794, height: 1123 } });
    await p.goto('file://' + path.join(ROOT, '_print', src + '.html'));
    await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(800);
    const fields = await p.evaluate(() => {
      const out = [];
      document.querySelectorAll('.sheet').forEach((sh, page) => {
        const sr = sh.getBoundingClientRect();
        sh.querySelectorAll('[data-f]').forEach(f => {
          const r = f.getBoundingClientRect();
          out.push({ page, name: f.dataset.f, type: f.dataset.type, x: r.left - sr.left, y: r.top - sr.top, w: r.width, h: r.height });
        });
      });
      return out;
    });
    fs.writeFileSync(path.join(ROOT, '_print', src + '.fields.json'), JSON.stringify(fields));
    await p.pdf({ path: path.join(ROOT, '_print', name + '.base.pdf'), format: 'A4', printBackground: true, margin: { top: 0, right: 0, bottom: 0, left: 0 }, preferCSSPageSize: true });
    console.log(name, fields.length, 'fields');
    await p.close();
  }
  await b.close();
})();
