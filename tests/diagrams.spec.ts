import { test, expect } from '@playwright/test';

/**
 * Tests for the ss-* diagram components (see docs/contribute/docs.md → Diagrams).
 *
 * Every former ASCII diagram is now a semantic-HTML <figure class="ss-diagram">.
 * These tests guard three things: the diagrams render intact on every page that
 * has one, no ASCII art creeps back into code fences, and the responsive
 * layout never causes horizontal overflow on a phone-sized viewport.
 */

const DIAGRAM_PAGES = [
  { route: '/#/README', name: 'homepage architecture' },
  { route: '/#/get-started/build-device', name: 'build phases' },
  { route: '/#/get-started/first-wallet', name: 'first-wallet swimlane' },
  { route: '/#/get-started/receive', name: 'receive swimlane' },
  { route: '/#/get-started/send', name: 'send swimlane' },
  { route: '/#/get-started/multisig', name: 'multisig flow' },
  { route: '/#/get-started/bluewallet', name: 'bluewallet swimlane' },
];

/** Box-drawing / arrow characters used by the old ASCII diagrams. */
const ASCII_ART = /[─-╿◄►◀▶]/;

for (const { route, name } of DIAGRAM_PAGES) {
  test(`${name}: diagram renders and no ASCII art remains`, async ({ page }) => {
    await page.goto(route);
    const diagram = page.locator('.markdown-section .ss-diagram');
    await expect(diagram).toHaveCount(1);
    await expect(diagram).toBeVisible();

    // Accessible: the figure describes itself.
    expect((await diagram.getAttribute('aria-label'))?.length).toBeGreaterThan(10);

    // Parse guard: a blank line inside the HTML block would make marked split
    // the figure and wrap the remainder in <p> tags.
    expect(await diagram.locator('p').count()).toBe(0);

    // The copy-code plugin must not treat diagrams as code.
    expect(await diagram.locator('pre, .docsify-copy-code-button').count()).toBe(0);

    // Regression guard: no box-drawing soup left in any code fence.
    for (const text of await page.locator('.markdown-section pre').allTextContents()) {
      expect(text).not.toMatch(ASCII_ART);
    }
  });
}

test('first-wallet swimlane has two lanes and badges 1–8 on desktop', async ({ page }) => {
  await page.goto('/#/get-started/first-wallet');
  const steps = page.locator('ol.ss-steps');
  await expect(steps).toBeVisible();
  const trackCount = await steps.evaluate(
    (el) => getComputedStyle(el).gridTemplateColumns.split(' ').length,
  );
  expect(trackCount).toBe(2);
  await expect(page.locator('.ss-step-num')).toHaveText(['1', '2', '3', '4', '5', '6', '7', '8']);
  // Lane chips are a mobile-only affordance.
  await expect(page.locator('.ss-lane-tag').first()).toBeHidden();
});

test.describe('mobile (375px)', () => {
  test.use({ viewport: { width: 375, height: 812 } });

  for (const { route, name } of DIAGRAM_PAGES) {
    test(`${name}: no horizontal overflow at 375px`, async ({ page }) => {
      await page.goto(route);
      const diagram = page.locator('.markdown-section .ss-diagram');
      await expect(diagram).toBeVisible();

      const box = await diagram.boundingBox();
      expect(box).not.toBeNull();
      expect(box!.width).toBeLessThanOrEqual(375);

      expect(
        await page.evaluate(
          () => document.documentElement.scrollWidth <= document.documentElement.clientWidth,
        ),
      ).toBe(true);
    });
  }

  test('swimlane stacks to one column with lane chips visible', async ({ page }) => {
    await page.goto('/#/get-started/first-wallet');
    const steps = page.locator('ol.ss-steps');
    await expect(steps).toBeVisible();
    const trackCount = await steps.evaluate(
      (el) => getComputedStyle(el).gridTemplateColumns.split(' ').length,
    );
    expect(trackCount).toBe(1);
    await expect(page.locator('.ss-lane-tag').first()).toBeVisible();
  });
});
