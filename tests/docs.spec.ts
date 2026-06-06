import { test, expect, type Page } from '@playwright/test';

/**
 * Smoke tests for the SeedSigner docsify site.
 *
 * Docsify renders Markdown client-side, so each test waits for the rendered
 * `.markdown-section` before asserting. The image checks below would have
 * caught the broken homepage hero path (`../images/...` escaping the served
 * root), so they double as a regression guard for relative image links.
 */

/** Returns the list of `src` values for images that failed to load in a section. */
async function brokenImages(page: Page, selector: string): Promise<string[]> {
  return page.locator(`${selector} img`).evaluateAll((imgs) =>
    (imgs as HTMLImageElement[])
      .filter((img) => !(img.complete && img.naturalWidth > 0))
      .map((img) => img.getAttribute('src') ?? '(no src)'),
  );
}

test('homepage renders the documentation title', async ({ page }) => {
  await page.goto('/');
  await expect(page.locator('.markdown-section h1').first()).toHaveText(
    /SeedSigner Documentation/,
  );
});

test('homepage hero image loads (relative path resolves)', async ({ page }) => {
  await page.goto('/');
  const hero = page.locator(
    '.markdown-section img[src*="SeedSigner_Device_and_Components"]',
  );
  await expect(hero).toBeVisible();
  await expect
    .poll(() =>
      hero.evaluate((img: HTMLImageElement) => img.complete && img.naturalWidth > 0),
    )
    .toBe(true);
});

test('no broken images on the homepage', async ({ page }) => {
  await page.goto('/');
  await expect(page.locator('.markdown-section').first()).toBeVisible();
  await page.waitForLoadState('networkidle');
  expect(await brokenImages(page, '.markdown-section')).toEqual([]);
});

test('an internal route renders its content', async ({ page }) => {
  await page.goto('/#/hardware-build/assembly');
  await expect(page.locator('.markdown-section h1').first()).toHaveText(
    /Assembly instructions/,
  );
});

test('sidebar navigation works', async ({ page }) => {
  await page.goto('/');
  // On the homepage the "Home" section is auto-expanded (it holds the active
  // route), so its child links are visible and clickable without expanding a
  // collapsed section first.
  const overviewLink = page.locator('.sidebar-nav a', {
    hasText: 'What is SeedSigner?',
  });
  await overviewLink.first().click();
  await expect(page).toHaveURL(/overview/);
  await expect(page.locator('.markdown-section h1').first()).toHaveText(
    /What is SeedSigner\?/,
  );
});
