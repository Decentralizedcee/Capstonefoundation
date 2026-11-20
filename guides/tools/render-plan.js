// Renders guides/_print/whatsapp.html to guides/whatsapp/WhatsApp-Community-Plan.pdf
// usage: NODE_PATH=$(npm root -g) node guides/tools/render-plan.js
const { chromium } = require('playwright');
const path = require('path'), fs = require('fs');
const ROOT = path.resolve(__dirname, '..');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 794, height: 1123 } });
  await p.goto('file://' + path.join(ROOT, '_print', 'whatsapp.html'));
  await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(800);
  fs.mkdirSync(path.join(ROOT, 'whatsapp'), { recursive: true });
  // Scale each text page up so it fills the sheet (cover, closing and the dense message page are left alone).
  const zooms = await p.evaluate(() => {
    const out = [];
    document.querySelectorAll('.sheet').forEach((sh, i) => {
      if (sh.classList.contains('frame') || sh.classList.contains('tight')) return;
      const kids = [...sh.children].filter(c => !c.classList.contains('hd') && !c.classList.contains('ft'));
      const sr = sh.getBoundingClientRect(), limit = sr.height - 78;
      const top = () => kids[0].getBoundingClientRect().top - sr.top;
      const bottom = () => Math.max(...kids.map(k => k.getBoundingClientRect().bottom)) - sr.top;
      let z = Math.min(1.5, (limit - top()) / (bottom() - top()));
      if (z <= 1.04) return;
      for (let t = 0; t < 12; t++) { kids.forEach(k => { k.style.zoom = String(z); }); if (bottom() <= limit) break; z *= 0.97; }
      out.push([i + 1, +z.toFixed(2)]);
    });
    return out;
  });
  console.log('zoom per page:', JSON.stringify(zooms));
  const overflow = await p.evaluate(() => [...document.querySelectorAll('.sheet')].map((s, i) => {
    const last = [...s.children].filter(c => !c.classList.contains('ft')).pop();
    return { page: i + 1, bottom: Math.round(last.getBoundingClientRect().bottom - s.getBoundingClientRect().top), limit: Math.round(s.getBoundingClientRect().height - 62) };
  }).filter(x => x.bottom > x.limit));
  console.log('pages running into the footer area:', JSON.stringify(overflow));
  await p.pdf({ path: path.join(ROOT, 'whatsapp', 'WhatsApp-Community-Plan.pdf'), format: 'A4', printBackground: true, margin: { top: 0, right: 0, bottom: 0, left: 0 }, preferCSSPageSize: true });
  await b.close();
})();
