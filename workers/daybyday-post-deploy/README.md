# daybyday-post-deploy

Cloudflare Worker that runs after every Cloudflare Pages deploy.

## What it does

- **On Pages deploy**: fetches the new sitemap, diffs against the previous one stored in KV,
  submits new URLs to [IndexNow](https://www.indexnow.org/), and notifies a Telegram chat.
- **Sunday 06:00 UTC**: re-pings IndexNow with the 50 most recent URLs (catch-up for slow crawlers).
- **Sunday 07:30 UTC**: checks sitemap freshness and reports via Telegram.

## Setup

1. Create a KV namespace:
   ```bash
   wrangler kv:namespace create BLOG_KV
   ```
   Copy the returned `id` into `wrangler.toml` under `[[kv_namespaces]]`.

2. Set the three encrypted secrets:
   ```bash
   wrangler secret put INDEXNOW_KEY         # 32-char hex from indexnow.org
   wrangler secret put TELEGRAM_BOT_TOKEN   # from @BotFather
   wrangler secret put TELEGRAM_CHAT_ID     # your numeric chat id
   ```

3. Deploy:
   ```bash
   npm install
   npm run deploy
   ```

4. In Cloudflare dashboard → Pages project → Settings → Builds → Deploy hooks:
   - Add a deploy hook
   - The hook URL is the public URL of the Worker (e.g. `https://daybyday-post-deploy.<acct>.workers.dev/`)
   - Or simpler: have the Pages build send a POST to the Worker after success.

5. Verify with a manual trigger:
   ```bash
   curl -X POST https://daybyday-post-deploy.<acct>.workers.dev/trigger-indexnow
   curl -X POST https://daybyday-post-deploy.<acct>.workers.dev/notify \
        -H 'content-type: application/json' \
        -d '{"text":"Hello from Pablo"}'
   ```

## IndexNow key file

The Worker expects this file at the site root:
```
https://www.daybydayconsulting.com/indexnow-<KEY>.txt
```
It contains only the key (no HTML). The key must match `INDEXNOW_KEY`.

This file is already in the repo at `/indexnow-7de9e111be6418906030e2ec7be8cb62.txt`.

## Cost

Free tier: 100,000 requests/day, 1,000 cron triggers/month. Plenty for 3 posts/week.

## Why not Vercel/Netlify?

Cloudflare Pages + Workers gives us:
- Static HTML on the global edge (no SSR, no build step).
- Free KV for state.
- Free cron triggers.
- Free 100K Worker requests/day.
- Free unlimited static asset bandwidth on Pages.
