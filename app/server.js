// 📮 The demo app for the whole course — zero dependencies, plain Node.
// It answers with its hostname and version so you can SEE which copy replied
// (the same trick the Docker and Kubernetes schools use).
const http = require('node:http');
const os = require('node:os');

const PORT = Number(process.env.PORT || 3000);
const VERSION = process.env.APP_VERSION || 'dev';

function handler(req, res) {
  if (req.url === '/healthz') {                 // "are you ready?" — the readiness probe asks this
    res.writeHead(200, { 'content-type': 'text/plain' });
    return res.end('ok\n');
  }
  if (req.url === '/') {
    res.writeHead(200, { 'content-type': 'text/plain; charset=utf-8' });
    return res.end(`📮 hello from ${os.hostname()} · version ${VERSION}\n`);
  }
  res.writeHead(404, { 'content-type': 'text/plain' });
  res.end('not found\n');
}

const createServer = () => http.createServer(handler);

if (require.main === module) {
  createServer().listen(PORT, () => console.log(`📮 listening on :${PORT} (version ${VERSION})`));
}

module.exports = { handler, createServer };
