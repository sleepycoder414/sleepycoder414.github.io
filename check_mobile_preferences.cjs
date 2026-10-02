const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');
const {chromium} = require('C:/Users/tlam/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');

(async () => {
  const browser = await chromium.launch({channel: 'msedge', headless: true});
  const context = await browser.newContext({viewport: {width: 390, height: 844}, isMobile: true, hasTouch: true});
  const page = await context.newPage();
  const errors = [], staleRequests = [], assetRequests = [];
  page.on('pageerror', e => errors.push(e.message));
  const origin = 'https://condo.test';
  // Simulate an origin that still serves old cached assets at unversioned URLs.
  await context.route(origin + '/**', async route => {
    const url = new URL(route.request().url());
    if (/style-pages\.(css|js)$/.test(url.pathname)) {
      assetRequests.push(url.href);
      if (!url.searchParams.has('v')) {
        staleRequests.push(url.href);
        return route.fulfill({contentType: url.pathname.endsWith('.css') ? 'text/css' : 'text/javascript', body: '/* Older asset without the new button */'});
      }
      const extension = url.pathname.split('.').pop();
      const bytes = fs.readFileSync(path.join(__dirname, 'style-pages.' + extension));
      assert.equal(url.searchParams.get('v'), crypto.createHash('sha256').update(bytes).digest('hex').slice(0, 12));
    }
    const file = path.join(__dirname, decodeURIComponent(url.pathname).replace(/^\//, ''));
    const contentType = file.endsWith('.html') ? 'text/html' : file.endsWith('.css') ? 'text/css' : file.endsWith('.js') ? 'text/javascript' : 'image/png';
    await route.fulfill({contentType, body: fs.readFileSync(file)});
  });
  await page.goto(origin + '/index.html');
  const card = id => page.locator(`.card[data-id="${id}"]`);
  const metrics = await card('01').locator('.style-actions button').evaluateAll(buttons => buttons.map(b => ({height: b.getBoundingClientRect().height, font: getComputedStyle(b).fontSize, appearance: getComputedStyle(b).appearance})));
  assert.equal(metrics.length, 2);
  assert.equal(metrics[0].height, metrics[1].height);
  assert.equal(metrics[0].font, metrics[1].font);
  metrics.forEach(m => {assert.ok(m.height >= 44); assert.equal(m.appearance, 'none');});
  await card('01').locator('.not-for-me').tap();
  assert.equal(await page.locator('#excluded-styles .card[data-id="01"]').count(), 1);
  await page.reload();
  assert.equal(await page.locator('#excluded-styles .card[data-id="01"]').count(), 1);
  await card('01').locator('.card-link').tap();
  assert.equal(await page.locator('.not-for-me').textContent(), 'Restore to main list');
  await page.locator('.not-for-me').tap();
  assert.equal(await page.locator('.not-for-me').getAttribute('aria-pressed'), 'false');
  await page.locator('.favorite').tap();
  assert.equal(await page.locator('.favorite').getAttribute('aria-pressed'), 'true');
  await Promise.all([page.waitForURL(origin + '/index.html'), page.locator('header a').last().tap()]);
  assert.equal(await page.locator('#main-styles .card[data-id="01"]').count(), 1);
  assert.equal(await card('01').locator('.favorite').getAttribute('aria-pressed'), 'true');
  assert.equal(await page.evaluate(() => document.documentElement.scrollWidth > innerWidth), false);
  await card('01').locator('.style-actions').scrollIntoViewIfNeeded();
  await page.screenshot({path: path.join(__dirname, 'review', 'mobile-button-fix.png')});
  assert.deepEqual(staleRequests, [], 'Updated pages must never request the unversioned stale assets');
  assert.ok(assetRequests.length >= 4);
  assert.deepEqual(errors, []);
  await browser.close();
  console.log('Mobile touch, equal 44px targets, matching asset hashes, stale-asset avoidance, reload and cross-page preferences passed (Chromium emulation; not an actual iOS device)');
})().catch(error => {console.error(error); process.exit(1);});
