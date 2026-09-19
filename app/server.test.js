// ✅ The checking desk: these tests run on every push (lesson 03).
// Zero dependencies — node:test + node:assert, Node 20 or newer.
const test = require('node:test');
const assert = require('node:assert/strict');
const { createServer } = require('./server');

async function withServer(fn) {
  const server = createServer();
  await new Promise((resolve) => server.listen(0, '127.0.0.1', resolve));   // port 0 = any free port
  const base = `http://127.0.0.1:${server.address().port}`;
  try { await fn(base); } finally { await new Promise((resolve) => server.close(resolve)); }
}

test('GET / says hello with the hostname and version', () =>
  withServer(async (base) => {
    const res = await fetch(`${base}/`);
    assert.equal(res.status, 200);
    assert.match(await res.text(), /hello from \S+ · version /);
  }));

test('GET /healthz answers ok — what the readiness probe asks', () =>
  withServer(async (base) => {
    const res = await fetch(`${base}/healthz`);
    assert.equal(res.status, 200);
    assert.equal(await res.text(), 'ok\n');
  }));

test('unknown paths are a 404, not a crash', () =>
  withServer(async (base) => {
    const res = await fetch(`${base}/nope`);
    assert.equal(res.status, 404);
  }));
