#!/usr/bin/env node
// Usage: node scripts/optimize-image.mjs <input-file> <output-dir> <base-name>
// Writes <base-name>-480.webp, -800.webp, -1200.webp (never upscales) and prints JSON.
// Requires: npm install --save-dev sharp
import fs from "node:fs";
import path from "node:path";

const [, , input, outDir, baseName] = process.argv;
if (!input || !outDir || !baseName) {
  console.error("Usage: node scripts/optimize-image.mjs <input-file> <output-dir> <base-name>");
  process.exit(1);
}
if (!fs.existsSync(input)) {
  console.error(`Input not found: ${input}`);
  process.exit(1);
}

let sharp;
try {
  sharp = (await import("sharp")).default;
} catch {
  console.error("sharp is not installed. Run: npm install --save-dev sharp");
  process.exit(1);
}

const safe = baseName.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-+|-+$/g, "");
fs.mkdirSync(outDir, { recursive: true });

const meta = await sharp(input).rotate().metadata(); // rotate() applies EXIF orientation
const srcWidth = meta.autoOrient?.width ?? meta.width;
const targets = [480, 800, 1200].filter((w) => w <= srcWidth);
if (targets.length === 0) targets.push(srcWidth); // small image: keep its own width

const files = [];
for (const w of targets) {
  const out = path.join(outDir, `${safe}-${w}.webp`);
  const info = await sharp(input).rotate().resize({ width: w, withoutEnlargement: true }).webp({ quality: 78 }).toFile(out);
  files.push({ width: info.width, height: info.height, bytes: info.size, path: out });
}

console.log(JSON.stringify({ original: input, base: safe, files }, null, 2));
