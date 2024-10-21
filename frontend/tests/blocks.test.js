const path = require('path');

describe('Blocks HTML Page', () => {
  beforeAll(async () => {
    await page.goto('http://localhost:8080/blocks.html');
  });

  it('should load the page', async () => {
    const title = await page.title();
    expect(title).toBe('Repository Manager - Drag and Drop');
  });

  it('should have three columns', async () => {
    const columns = await page.$$('.column');
    expect(columns.length).toBe(3);
  });

  it('should have three select elements', async () => {
    const selects = await page.$$('select');
    expect(selects.length).toBe(3);
  });

  it('should populate select elements with organizations', async () => {
    // Mock the API response
    await page.setRequestInterception(true);
    page.on('request', (request) => {
      if (request.url().endsWith('/api/organizations')) {
        request.respond({
          status: 200,
          contentType: 'application/json',
          body: JSON.stringify([
            { id: 'org1', name: 'Organization 1' },
            { id: 'org2', name: 'Organization 2' },
            { id: 'org3', name: 'Organization 3' }
          ])
        });
      } else {
        request.continue();
      }
    });

    // Reload the page to trigger the API call
    await page.reload();

    // Wait for the select elements to be populated
    await page.waitForFunction(() => {
      const selects = document.querySelectorAll('select');
      return Array.from(selects).every(select => select.options.length > 0);
    });

    // Check if all select elements have the correct number of options
    const selectsContent = await page.$$eval('select', (selects) => 
      selects.map(select => select.options.length)
    );

    expect(selectsContent).toEqual([4, 4, 4]); // 3 organizations + 1 default option
  });

  it('should load repositories when an organization is selected', async () => {
    // Mock the API response for repositories
    await page.setRequestInterception(true);
    page.on('request', (request) => {
      if (request.url().includes('/api/repositories')) {
        request.respond({
          status: 200,
          contentType: 'application/json',
          body: JSON.stringify([
            { id: 'repo1', name: 'Repository 1' },
            { id: 'repo2', name: 'Repository 2' }
          ])
        });
      } else {
        request.continue();
      }
    });

    // Select an organization in the first column
    await page.select('#org-select1', 'org1');

    // Wait for the repositories to be loaded
    await page.waitForSelector('#column1 .repo-block');

    // Check if the repositories are displayed
    const repoBlocks = await page.$$('#column1 .repo-block');
    expect(repoBlocks.length).toBe(2);

    const repoNames = await page.$$eval('#column1 .repo-block', blocks => 
      blocks.map(block => block.textContent)
    );
    expect(repoNames).toEqual(['Repository 1', 'Repository 2']);
  });
});
