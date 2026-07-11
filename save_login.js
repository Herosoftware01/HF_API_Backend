const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({
    headless: false, // open browser
  });

  const context = await browser.newContext();
  const page = await context.newPage();

  console.log('Opening login page...');

  await page.goto('http://10.1.21.13:3000', {
    waitUntil: 'domcontentloaded',
    timeout: 120000,
  });

  console.log('');
  console.log('========================================');
  console.log('1. Login manually in the browser.');
  console.log('2. Wait until dashboard opens.');
  console.log('3. Come back here and press ENTER.');
  console.log('========================================');
  console.log('');

  process.stdin.resume();

  process.stdin.on('data', async () => {
    try {
      await context.storageState({
        path: 'auth.json',
      });

      console.log('✅ auth.json saved successfully!');
    } catch (err) {
      console.log('❌ Failed to save auth.json');
      console.log(err);
    }

    await browser.close();
    process.exit();
  });
})();