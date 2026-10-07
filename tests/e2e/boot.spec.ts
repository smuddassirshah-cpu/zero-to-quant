// The empty app boots on every path with no console or page errors, and the Artifact page's gate and
// bootstrap behave as tools/release/page.ts writes them. Google Fonts is answered locally, so no test
// needs the network; any other outside request is aborted and so fails the test.
import { expect, test, type Page } from '@playwright/test';

const BOOT_TARGET: Readonly<Record<string, string>> = { dev: 'web', web: 'web', artifact: 'artifact' };
const LOCAL = /^http:\/\/(localhost|127\.0\.0\.1):\d+\//;
const GOOGLE_FONTS = /^https:\/\/fonts\.(googleapis|gstatic)\.com\//;

async function offline(page: Page): Promise<string[]> {
  const errors: string[] = [];
  page.on('console', (message) => {
    if (message.type() === 'error') errors.push(message.text());
  });
  page.on('pageerror', (error) => errors.push(error.message));
  await page.route(
    (url) => !LOCAL.test(url.href),
    (route) =>
      GOOGLE_FONTS.test(route.request().url())
        ? route.fulfill({ status: 200, contentType: 'text/css', body: '' })
        : route.abort(),
  );
  return errors;
}

// Errors are read only once the page has loaded and its network has gone quiet.
async function open(page: Page): Promise<void> {
  await page.goto('/', { waitUntil: 'load' });
  await page.waitForLoadState('networkidle');
}

test('the empty app boots', async ({ page }, testInfo) => {
  const target = BOOT_TARGET[testInfo.project.name];
  if (target === undefined) throw new Error(`No boot target for project ${testInfo.project.name}`);
  const errors = await offline(page);

  await open(page);

  await expect(page.getByRole('heading', { level: 1 })).toHaveText('Zero to Quant');
  await expect(page.locator('#app')).toHaveAttribute('data-zq-boot', target);
  expect(errors).toEqual([]);
});

test.describe('the Artifact page', () => {
  test.beforeEach(() => {
    test.skip(
      test.info().project.name !== 'artifact',
      'the gate and the bootstrap belong to the Artifact page',
    );
  });

  const TOO_OLD = 'This browser is too old for Zero to Quant.';

  test('turns away a browser without structuredClone and never loads the entry', async ({ page }) => {
    const errors = await offline(page);
    const scripts: string[] = [];
    page.on('request', (request) => {
      if (request.resourceType() === 'script') scripts.push(request.url());
    });
    await page.addInitScript(() => Reflect.deleteProperty(globalThis, 'structuredClone'));
    await open(page);
    await expect(page.locator('#app')).toHaveText(TOO_OLD);
    expect(await page.evaluate(() => Reflect.get(window, '__zqOld') as unknown)).toBe(true);
    expect(scripts).toEqual([]);
    expect(errors).toEqual([]);
  });

  // Stands in for an engine that cannot parse import(): the bootstrap fails to parse, the gate still runs.
  test('shows the gate message when the bootstrap cannot be parsed', async ({ page }) => {
    const errors = await offline(page);
    await page.route('/', async (route) => {
      const response = await route.fetch();
      const body = (await response.text()).replace("import('", "import(]'");
      await route.fulfill({ response, body });
    });
    await page.addInitScript(() => Reflect.deleteProperty(globalThis, 'structuredClone'));
    await open(page);
    await expect(page.locator('#app')).toHaveText(TOO_OLD);
    expect(errors).toHaveLength(1);
    expect(errors[0]).toMatch(/Unexpected token/);
  });

  test('says so when the entry script cannot load', async ({ page }) => {
    const errors = await offline(page);
    await page.route('**/assets/app.*.js', (route) => route.fulfill({ status: 404 }));
    await open(page);
    await expect(page.locator('#app')).toHaveText('Zero to Quant could not start. Reload to try again.');
    expect(errors.some((text) => text.includes('dynamically imported module'))).toBe(true);
  });
});
