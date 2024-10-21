const puppeteer = require('puppeteer');

describe('Blocks Page', () => {
  let browser;
  let page;

  beforeAll(async () => {
    browser = await puppeteer.launch();
    page = await browser.newPage();
    await page.goto('http://localhost:3000/blocks.html');
  });

  afterAll(async () => {
    await browser.close();
  });

  test('page title is correct', async () => {
    const title = await page.title();
    expect(title).toBe('Repository Manager - Drag and Drop');
  });

  test('organization select lists are populated', async () => {
    await page.waitForSelector('select');
    const selectCount = await page.$$eval('select', selects => selects.length);
    expect(selectCount).toBe(3);

    const firstSelectOptions = await page.$eval('select', select => select.options.length);
    expect(firstSelectOptions).toBeGreaterThan(1);
  });

  test('repositories are loaded when an organization is selected', async () => {
    await page.select('select:first-of-type', 'org1');
    await page.waitForSelector('.repo-block');
    const repoBlocks = await page.$$('.repo-block');
    expect(repoBlocks.length).toBeGreaterThan(0);
  });

  test('error is displayed when API fails', async () => {
    await page.evaluate(() => {
      window.fetch = () => Promise.reject(new Error('API Error'));
    });
    await page.reload();
    await page.waitForSelector('#error-container');
    const errorText = await page.$eval('#error-container', el => el.textContent);
    expect(errorText).toContain('Error');
  });
});
