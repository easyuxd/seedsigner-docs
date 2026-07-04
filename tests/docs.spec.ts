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

test('homepage renders the merged Home title', async ({ page }) => {
  await page.goto('/');
  await expect(page.locator('.markdown-section h1').first()).toHaveText(
    /^SeedSigner$/,
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
  await page.goto('/#/reference/hardware/assembly');
  await expect(page.locator('.markdown-section h1').first()).toHaveText(
    /^Assembly$/,
  );
});

test('a pre-restructure URL still resolves via alias redirect', async ({ page }) => {
  // Old topic-taxonomy path; the `alias` map in index.html points it at the
  // new reference location so existing bookmarks/inbound links keep working.
  await page.goto('/#/hardware-build/assembly');
  await expect(page.locator('.markdown-section h1').first()).toHaveText(
    /^Assembly$/,
  );
});

test('sidebar navigation works', async ({ page }) => {
  await page.goto('/');
  // Top-level sections start collapsed; expand "Get Started", then click a journey.
  await page
    .locator('.sidebar-nav')
    .getByText('Get Started', { exact: true })
    .click();
  const journey = page.locator('.sidebar-nav a', { hasText: 'Build your device' });
  await journey.first().click();
  await expect(page).toHaveURL(/get-started\/build-device/);
  await expect(page.locator('.markdown-section h1').first()).toHaveText(
    /^Build your device$/,
  );
});
