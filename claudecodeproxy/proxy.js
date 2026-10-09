// Claude Code 模型路由器
// 按请求体中的 model 字段分流：
//   - 命中本地 omlx 模型列表 -> LOCAL_UPSTREAM (http://127.0.0.1:28000)
//   - 其余（glm 系列等）    -> REMOTE_UPSTREAM (https://open.bigmodel.cn/api/anthropic)
// 两端均为 Anthropic /v1/messages 格式，纯转发，支持 SSE 流式透传。
const http = require('http');
const https = require('https');
const { URL } = require('url');

const PORT = parseInt(process.env.PORT || '28001', 10);
const LOCAL = new URL(process.env.LOCAL_UPSTREAM || 'http://127.0.0.1:28000');
const LOCAL_KEY = process.env.LOCAL_API_KEY || '';
const REMOTE = new URL(process.env.REMOTE_UPSTREAM || 'https://open.bigmodel.cn/api/anthropic');

let localModels = new Set();
let lastRefresh = 0;

async function refreshModels() {
  if (Date.now() - lastRefresh < 60000) return;
  lastRefresh = Date.now();
  try {
    const res = await fetch(new URL('/v1/models', LOCAL), {
      headers: { Authorization: `Bearer ${LOCAL_KEY}` },
      signal: AbortSignal.timeout(10000),
    });
    const j = await res.json();
    if (Array.isArray(j.data)) {
      localModels = new Set(j.data.map((m) => m.id));
      console.log(`[router] 本地模型: ${[...localModels].join(', ')}`);
    } else {
      console.error(`[router] 模型列表响应异常: HTTP ${res.status} ${JSON.stringify(j).slice(0, 200)}`);
    }
  } catch (e) {
    console.error(`[router] 模型列表刷新失败: ${e.message}`);
  }
}

function joinPath(base, url) {
  return base.pathname.replace(/\/+$/, '') + url;
}

function pickTarget(bodyStr) {
  try {
    const m = JSON.parse(bodyStr).model;
    return Boolean(m && localModels.has(m));
  } catch {}
  return false;
}

const server = http.createServer(async (req, res) => {
  const chunks = [];
  for await (const c of req) chunks.push(c);
  const body = Buffer.concat(chunks);
  await refreshModels();

  const isLocal = pickTarget(body.toString('utf8'));
  const up = isLocal ? LOCAL : REMOTE;
  const mod = up.protocol === 'https:' ? https : http;

  const headers = { ...req.headers, host: up.host };
  if (isLocal) {
    headers['x-api-key'] = LOCAL_KEY;
    headers.authorization = `Bearer ${LOCAL_KEY}`;
  }

  let model = '';
  try { model = JSON.parse(body.toString('utf8')).model || ''; } catch {}
  console.log(`[router] ${req.method} ${req.url} model=${model} -> ${isLocal ? 'local' : 'remote'}`);

  const upReq = mod.request(
    {
      protocol: up.protocol,
      hostname: up.hostname,
      port: up.port,
      method: req.method,
      path: joinPath(up, req.url),
      headers,
    },
    (upRes) => {
      console.log(`[router] 上游响应 ${upRes.statusCode}`);
      res.writeHead(upRes.statusCode, upRes.headers);
      upRes.pipe(res);
    }
  );

  upReq.on('error', (e) => {
    console.error(`[router] 上游(${isLocal ? 'local' : 'remote'})错误: ${e.message}`);
    if (!res.headersSent) {
      res.writeHead(502, { 'content-type': 'application/json' });
      res.end(JSON.stringify({ type: 'error', error: { type: 'api_error', message: `router: upstream ${isLocal ? 'local' : 'remote'} unreachable: ${e.message}` } }));
    } else res.destroy();
  });

  upReq.end(body);
});

// 长会话/长流式输出：放宽超时
server.requestTimeout = 0;
server.headersTimeout = 60000;

server.listen(PORT, '127.0.0.1', () => {
  console.log(`[router] 监听 127.0.0.1:${PORT}`);
  console.log(`[router] local=${LOCAL.href} remote=${REMOTE.href}`);
  refreshModels();
});
