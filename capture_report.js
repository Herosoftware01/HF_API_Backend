const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

(async () => {
  try {
    const unit = process.argv[2];
    const date = process.argv[3];

    if (!unit || !date) {
      console.log(
        JSON.stringify({
          success: false,
          message:
            'Usage: node capture_report.js <unit> <date>',
        })
      );
      process.exit(0);
    }

    const browser = await chromium.launch({
      headless: true,
    });

    const context = await browser.newContext({
      storageState: 'auth.json',
      viewport: {
        width: 2600,
        height: 2000,
      },
    });

    const page = await context.newPage();

    const url =
      `http://10.1.21.13:3000/#/qc_reports/roving_qc_whatsapp?unit=${unit}&date=${date}`;

    console.log('Opening:', url);

    try {
      await page.goto(url, {
        waitUntil: 'domcontentloaded',
        timeout: 120000,
      });
    } catch (err) {
      console.log(
        JSON.stringify({
          success: false,
          message: err.message,
        })
      );

      await browser.close();
      process.exit(0);
    }

    try {
      await page.waitForSelector('#report-ready', {
        timeout: 30000,
      });
    } catch (err) {
      console.log('Report ready timeout.');
    }

    await page.evaluate(() => {
      const el =
        document.getElementById('report-table');

      if (el) {
        el.style.overflow = 'visible';
        el.style.maxWidth = 'none';
        el.style.width = 'fit-content';
      }
    });

    await page.waitForTimeout(1000);

    // --- Clone the real header panel into every report page ---
    await page.evaluate(() => {
      const reportTable = document.getElementById('report-table');
      if (!reportTable) return;

      // The header panel is the first child div, before the
      // .report-page blocks (the "Roving QC Report" title +
      // Date/Unit line panel).
      const existingHeader = reportTable.querySelector(':scope > div:first-child');
      const pages = document.querySelectorAll('.report-page');

      if (!existingHeader) return;

      pages.forEach((pageEl) => {
        const headerClone = existingHeader.cloneNode(true);
        headerClone.classList.add('injected-report-header');
        headerClone.style.marginBottom = '20px';

        // Make the title bigger
        const titleEl = headerClone.querySelector('h1');
        if (titleEl) {
          titleEl.style.fontSize = '36px';
          titleEl.style.lineHeight = '1.2';
        }

        // Make the subtitle line bigger too
        const subtitleEl = headerClone.querySelector('p.text-sm.text-slate-500');
        if (subtitleEl) {
          subtitleEl.style.fontSize = '18px';
        }

        // Make the Date / Unit line bigger
        const dateUnitEl = headerClone.querySelector('.text-sm.font-medium.text-slate-600');
        if (dateUnitEl) {
          dateUnitEl.style.fontSize = '20px';
          dateUnitEl.style.padding = '10px 20px';
        }

        pageEl.prepend(headerClone);
      });
    });

    await page.waitForTimeout(300);
    // --- End header injection ---

    const reports =
      page.locator('.report-page');

    const count = await reports.count();

    console.log(`Found ${count} page(s)`);

    if (count === 0) {
      console.log(
        JSON.stringify({
          success: false,
          message: 'No report data',
        })
      );

      await browser.close();
      process.exit(0);
    }

    const saveDir =
      'D:\\Qc Report Image';

    if (!fs.existsSync(saveDir)) {
      fs.mkdirSync(saveDir, {
        recursive: true,
      });
    }

    const files = [];

    for (let i = 0; i < count; i++) {
      const report = reports.nth(i);

      const fileName =
        `roving_${unit}_${date}_${i + 1}.png`;

      const filePath = path.join(
        saveDir,
        fileName
      );

      await report.screenshot({
        path: filePath,
      });

      files.push(filePath);

      console.log('Saved:', filePath);
    }

    await browser.close();

    console.log(
      JSON.stringify({
        success: true,
        unit,
        date,
        files,
      })
    );

    process.exit(0);
  } catch (err) {
    console.log(
      JSON.stringify({
        success: false,
        message: err.message,
      })
    );

    process.exit(0);
  }
})();