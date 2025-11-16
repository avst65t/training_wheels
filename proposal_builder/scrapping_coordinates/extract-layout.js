const puppeteer = require('puppeteer'); // use 'puppeteer-core' only if you manage your own Chromium
const fs = require('fs');
const path = require('path');

(async () => {
  const browser = await puppeteer.launch({
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });

  const page = await browser.newPage();

  const filePath = `file:${path.resolve(__dirname, 'improve.html')}`;
  await page.goto(filePath, { waitUntil: 'networkidle0' });

  const result = await page.evaluate(() => {
    const PADDING = 60;

    const containers = Array.from(document.querySelectorAll('.container')).map(el => {
      const rect = el.getBoundingClientRect();
      return {
        id: el.id || null,
        x: rect.left,
        y: rect.top,
        width: rect.width,
        height: rect.height
      };
    });

    if (containers.length === 0) {
      throw new Error("❌ No containers found with class='container'");
    }

    // Find the outer bounds of the layout
    const minX = Math.min(...containers.map(c => c.x));
    const minY = Math.min(...containers.map(c => c.y));
    const maxX = Math.max(...containers.map(c => c.x + c.width));
    const maxY = Math.max(...containers.map(c => c.y + c.height));

    // Normalize positions and apply padding
    const normalizedContainers = containers.map(c => ({
      id: c.id,
      x: c.x - minX + PADDING,
      y: c.y - minY + PADDING,
      width: c.width,
      height: c.height
    }));

    const canvas = {
      width: (maxX - minX) + PADDING * 2,
      height: (maxY - minY) + PADDING * 2,
      padding: PADDING
    };

    return {
      canvas,
      containers: normalizedContainers
    };
  });

  fs.writeFileSync('layout.json', JSON.stringify(result, null, 2));
  console.log('✅ layout.json saved with padded canvas and normalized coordinates.');

  await browser.close();
})();
