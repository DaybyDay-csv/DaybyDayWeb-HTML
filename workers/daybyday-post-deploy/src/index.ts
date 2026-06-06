// daybyday-post-deploy — Cloudflare Worker
// Triggers: Pages deployment webhook + cron (Sun 06/07/08 UTC)
//
// Functions:
//   1. On Pages deploy: fetch sitemap, diff with KV, submit new URLs to IndexNow,
//      notify Telegram.
//   2. Cron Sun 06:00 UTC: re-ping IndexNow with the 50 most recent URLs
//      (catch-up for crawlers that missed the first push).
//   3. Cron Sun 07:00 UTC: optional Lighthouse spot-check via Lighthouse CI API.
//
// Setup:
//   - Deploy this Worker:  wrangler deploy
//   - In Pages project settings, add a deploy hook URL
//   - Set env vars: INDEXNOW_KEY, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, SITE
//   - Create a KV namespace "BLOG_KV" and bind it as BLOG_KV
//
// Env vars (encrypted secrets):
//   INDEXNOW_KEY          - 32-char hex from https://www.indexnow.org/
//   TELEGRAM_BOT_TOKEN    - from @BotFather
//   TELEGRAM_CHAT_ID      - your chat id (numeric)
//
// Env vars (plaintext):
//   SITE                  - https://www.daybydayconsulting.com

export interface Env {
  INDEXNOW_KEY: string;
  TELEGRAM_BOT_TOKEN: string;
  TELEGRAM_CHAT_ID: string;
  SITE: string;
  BLOG_KV: KVNamespace;
}

const KEY = "last_seen_urls"; // KV key storing last seen URL list (JSON array)

export default {
  // 1. Pages deployment webhook
  async fetch(request: Request, env: Env, ctx: ExecutionContext): Promise<Response> {
    const url = new URL(request.url);

    // Health
    if (url.pathname === "/health") {
      return new Response(JSON.stringify({ ok: true, time: new Date().toISOString() }), {
        headers: { "content-type": "application/json" },
      });
    }

    // Manual trigger for testing: POST /trigger-indexnow
    if (url.pathname === "/trigger-indexnow" && request.method === "POST") {
      const result = await runIndexNowDiff(env);
      return new Response(JSON.stringify(result, null, 2), {
        headers: { "content-type": "application/json" },
      });
    }

    // Manual trigger for Telegram: POST /notify
    if (url.pathname === "/notify" && request.method === "POST") {
      const body = await request.json().catch(() => ({}));
      const text = body.text || "Test message from daybyday-post-deploy worker.";
      const ok = await telegram(env, text);
      return new Response(JSON.stringify({ ok }), {
        headers: { "content-type": "application/json" },
      });
    }

    // Pages deploy webhook sends POST. We accept the request, log it, and trigger.
    // Pages webhook payload is just a notification — we re-fetch sitemap to be sure.
    if (request.method === "POST") {
      ctx.waitUntil(runIndexNowDiff(env));
      return new Response(JSON.stringify({ accepted: true }), {
        headers: { "content-type": "application/json" },
      });
    }

    return new Response("daybyday-post-deploy worker", { status: 200 });
  },

  // 2-3. Cron triggers
  async scheduled(event: ScheduledEvent, env: Env, ctx: ExecutionContext): Promise<void> {
    const cron = event.cron; // e.g. "0 6 * * 0"
    console.log(`[cron ${cron}] ${new Date().toISOString()}`);

    if (cron === "0 6 * * 0") {
      // Sunday 06:00 UTC: re-ping IndexNow with last 50 URLs
      ctx.waitUntil(repingRecent(env));
    } else if (cron === "30 7 * * 0") {
      // Sunday 07:30 UTC: weekly sitemap freshness check
      ctx.waitUntil(checkSitemapFreshness(env));
    }
  },
};

// ---------------------------------------------------------------------------
// IndexNow diff
// ---------------------------------------------------------------------------

async function runIndexNowDiff(env: Env): Promise<{ new_urls: string[]; submitted: number; telegram_ok: boolean }> {
  const current = await fetchSitemapUrls(env.SITE);
  const previous = await readSeen(env);

  const newOnes = current.filter((u) => !previous.has(u));
  if (newOnes.length === 0) {
    console.log("[indexnow] no new URLs");
    return { new_urls: [], submitted: 0, telegram_ok: true };
  }

  const submitted = await submitIndexNow(env, newOnes);
  await writeSeen(env, current);

  const sample = newOnes.slice(0, 5).map((u) => "• " + u).join("\n");
  const extra = newOnes.length > 5 ? `\n… y ${newOnes.length - 5} más` : "";
  const text = `✅ ${newOnes.length} URL(s) nuevas enviadas a IndexNow:\n${sample}${extra}`;
  const telegram_ok = await telegram(env, text);

  return { new_urls: newOnes, submitted, telegram_ok };
}

async function repingRecent(env: Env): Promise<void> {
  const all = await fetchSitemapUrls(env.SITE);
  const recent = all.slice(0, 50);
  const submitted = await submitIndexNow(env, recent);
  console.log(`[reping] submitted ${submitted} of ${recent.length}`);
  await telegram(env, `🔁 Re-ping semanal IndexNow: ${submitted} URLs (top 50 recientes)`);
}

async function checkSitemapFreshness(env: Env): Promise<void> {
  const r = await fetch(`${env.SITE}/sitemap.xml`);
  const text = await r.text();
  const lastmod = (text.match(/<lastmod>(.*?)<\/lastmod>/) || [])[1];
  const ok = !!lastmod;
  await telegram(env, `📋 Sitemap check: ${ok ? "OK" : "MISSING"} · lastmod: ${lastmod || "n/a"}`);
}

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

async function fetchSitemapUrls(site: string): Promise<string[]> {
  const r = await fetch(`${site}/sitemap.xml`);
  if (!r.ok) throw new Error(`sitemap fetch failed: ${r.status}`);
  const text = await r.text();
  const urls: string[] = [];
  for (const m of text.matchAll(/<loc>(.*?)<\/loc>/g)) {
    urls.push(m[1].trim());
  }
  return urls;
}

async function submitIndexNow(env: Env, urls: string[]): Promise<number> {
  if (urls.length === 0) return 0;
  // IndexNow accepts up to 10,000 URLs per submission.
  // We send at most 10,000 per call.
  const batch = urls.slice(0, 10000);
  const body = {
    host: new URL(env.SITE).host,
    key: env.INDEXNOW_KEY,
    keyLocation: `${env.SITE}/indexnow-${env.INDEXNOW_KEY}.txt`,
    urlList: batch,
  };
  const r = await fetch("https://api.indexnow.org/indexnow", {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify(body),
  });
  if (!r.ok) {
    console.error(`[indexnow] failed ${r.status}: ${await r.text()}`);
    return 0;
  }
  return batch.length;
}

async function readSeen(env: Env): Promise<Set<string>> {
  const raw = await env.BLOG_KV.get(KEY);
  if (!raw) return new Set();
  try {
    return new Set(JSON.parse(raw) as string[]);
  } catch {
    return new Set();
  }
}

async function writeSeen(env: Env, urls: string[]): Promise<void> {
  await env.BLOG_KV.put(KEY, JSON.stringify(urls), { expirationTtl: 60 * 60 * 24 * 30 });
}

async function telegram(env: Env, text: string): Promise<boolean> {
  if (!env.TELEGRAM_BOT_TOKEN || !env.TELEGRAM_CHAT_ID) {
    console.warn("[telegram] missing token/chat_id; skipping");
    return false;
  }
  const url = `https://api.telegram.org/bot${env.TELEGRAM_BOT_TOKEN}/sendMessage`;
  try {
    const r = await fetch(url, {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({
        chat_id: env.TELEGRAM_CHAT_ID,
        text,
        parse_mode: "HTML",
        disable_web_page_preview: true,
      }),
    });
    if (!r.ok) {
      console.error(`[telegram] ${r.status}: ${await r.text()}`);
      return false;
    }
    return true;
  } catch (e) {
    console.error(`[telegram] error: ${e}`);
    return false;
  }
}
