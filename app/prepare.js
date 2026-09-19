// ⏳ A deliberately SLOW preparation step — the stand-in for `npm ci`, `pip install`
// or a compile. It exists so lesson 04 can show what a cache HIT vs MISS looks like
// without pulling a single dependency. It writes app/prepared/table.json once.
const { createHash } = require('node:crypto');
const fs = require('node:fs');
const path = require('node:path');

const OUT_DIR = path.join(__dirname, 'prepared');
const OUT = path.join(OUT_DIR, 'table.json');
const ROUNDS = Number(process.env.PREPARE_ROUNDS || 12_000_000);  // ~3 s on a laptop, ~8–10 s on a CI runner

if (fs.existsSync(OUT)) {
  console.log(`⚡ prepared/table.json already exists — nothing to do (this is what a cache hit feels like)`);
  process.exit(0);
}

console.log(`⏳ preparing… (${ROUNDS.toLocaleString()} hash rounds — a cache MISS pays this every time)`);
const started = Date.now();
let digest = 'the-school-courier';
const table = {};
for (let i = 0; i < ROUNDS; i++) {
  digest = createHash('sha256').update(digest).digest('hex');
  if (i % 100_000 === 0) table[i] = digest.slice(0, 12);
}
fs.mkdirSync(OUT_DIR, { recursive: true });
fs.writeFileSync(OUT, JSON.stringify({ rounds: ROUNDS, sample: table }, null, 1));
console.log(`✅ wrote ${path.relative(process.cwd(), OUT)} in ${((Date.now() - started) / 1000).toFixed(1)} s`);
