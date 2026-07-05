const puppeteer = require('puppeteer');
const path = require('path');
const fs = require('fs');

(async () => {
  const baseDir = 'C:\\Users\\LOQ\\Downloads\\VITA Presentation\\VITA_Web_Presentation';
  const outputDir = path.join(baseDir, 'slide_screenshots');
  if (!fs.existsSync(outputDir)) fs.mkdirSync(outputDir, { recursive: true });

  const browser = await puppeteer.launch({
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-web-security']
  });
  const page = await browser.newPage();
  await page.setViewport({ width: 1280, height: 720 });

  const filePath = 'file:///C:/Users/LOQ/Downloads/VITA%20Presentation/VITA_Web_Presentation/index.html';
  await page.goto(filePath, { waitUntil: 'networkidle0', timeout: 30000 });
  await new Promise(r => setTimeout(r, 2000));

  // Enable Light Mode
  await page.evaluate(() => {
    document.body.classList.add('light-mode');
  });
  await new Promise(r => setTimeout(r, 500));

  // Get total slide count
  const slideCount = await page.evaluate(() => {
    return document.querySelectorAll('.swiper-slide:not(.swiper-slide-duplicate)').length;
  });
  console.log('Total slides: ' + slideCount);

  // Go to slide 0 first
  await page.evaluate(() => {
    if (window.swiper) window.swiper.slideTo(0, 0, false);
  });
  await new Promise(r => setTimeout(r, 1000));

  for (let i = 0; i < slideCount; i++) {
    // Navigate to slide i
    await page.evaluate((idx) => {
      if (window.swiper) {
        window.swiper.slideTo(idx, 0, false);
      }
    }, i);

    await new Promise(r => setTimeout(r, 1000));

    // Verify current slide
    const currentIdx = await page.evaluate(() => {
      return window.swiper ? window.swiper.activeIndex : -1;
    });
    console.log(`  Swiper activeIndex: ${currentIdx}`);

    const slideNum = String(i + 1).padStart(2, '0');
    const outPath = path.join(outputDir, 'slide_' + slideNum + '.png');
    await page.screenshot({ path: outPath, type: 'png' });
    console.log('Saved slide ' + (i + 1) + '/' + slideCount);
  }

  await browser.close();
  console.log('All done!');
})();
