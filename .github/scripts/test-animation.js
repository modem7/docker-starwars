// Verifies the asciimation actually plays (frames advance over time) and
// that the transport controls (Stop / Play) work, not just that the page
// returns 200. Playwright is used rather than a curl-only check because
// this behaviour only exists client-side, driven by index.html's own JS.
const { chromium } = require('playwright');

const BASE_URL = process.argv[2] || 'http://localhost:8080';

async function main() {
  const browser = await chromium.launch();
  const page = await browser.newPage();

  const consoleErrors = [];
  page.on('console', (msg) => {
    if (msg.type() === 'error') consoleErrors.push(msg.text());
  });
  page.on('pageerror', (err) => consoleErrors.push(String(err)));

  await page.goto(BASE_URL, { waitUntil: 'load' });
  await page.waitForFunction(
    () => document.querySelector('#screen')?.textContent.trim().length > 0,
    { timeout: 10000 },
  );

  const screenText = () => page.locator('#screen').innerText();

  const frameA = await screenText();
  await page.waitForTimeout(1500);
  const frameB = await screenText();
  if (frameA === frameB) {
    throw new Error('Asciimation did not advance frames within 1.5s of autoplay');
  }

  // Stop() should freeze the current frame.
  await page.click('#buttons a[title="Stop"]');
  await page.waitForTimeout(300);
  const stoppedFrame1 = await screenText();
  await page.waitForTimeout(1000);
  const stoppedFrame2 = await screenText();
  if (stoppedFrame1 !== stoppedFrame2) {
    throw new Error('Frame kept advancing after Stop() was clicked');
  }

  // Play() should resume advancing from wherever Stop() left off.
  await page.click('#buttons a[title="Play"]');
  await page.waitForTimeout(300);
  const resumedFrame1 = await screenText();
  await page.waitForTimeout(1500);
  const resumedFrame2 = await screenText();
  if (resumedFrame1 === resumedFrame2) {
    throw new Error('Asciimation did not resume advancing after Play() was clicked');
  }

  if (consoleErrors.length > 0) {
    throw new Error(`Console errors detected:\n${consoleErrors.join('\n')}`);
  }

  await browser.close();
  console.log('Asciimation playback test passed.');
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
