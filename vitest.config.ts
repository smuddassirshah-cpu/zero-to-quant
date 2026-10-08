// Two projects (ARCHITECTURE.md 4.1 and 8.1). Decision notes:
// - `node` runs every unit test; `browser` runs `packages/**/*.browser.test.ts` in Chromium, Firefox and
//   WebKit, for the determinism checks the stage 3 row needs in all three (dmath bit-identity). Widget
//   browser tests (Chromium only, 8.1) arrive with stage 4 under their own include.
// - Coverage is v8 and comes from the `node` project only: `npm run test:coverage` selects it, because v8
//   coverage needs a Chromium engine and the browser files test engines, not lines.
// - Each package has its own 90% floor (8.3): one pooled row let a 33-line untested mathcore module pass
//   while eslint-plugin-zq carried the total [measured, adversarial review of 8 October 2026]. The rows
//   come from the folders under packages/, so a new package gets its floor without an edit here.
// - CI's Playwright image has all three engines at the pinned revisions; elsewhere ZQ_CHROMIUM may name
//   another Chromium binary (as in playwright.config.ts) and `--project 'browser (chromium)'` runs that leg.
import { readdirSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { playwright } from '@vitest/browser-playwright';
import { configDefaults, defineConfig } from 'vitest/config';

const BROWSER_TESTS = '**/*.browser.test.ts';
const floor = { lines: 90, branches: 90 };
const packageFloors = Object.fromEntries(
  readdirSync(new URL('./packages', import.meta.url), { withFileTypes: true })
    .filter((entry) => entry.isDirectory())
    .map((entry) => [`packages/${entry.name}/src/**`, floor]),
);
const executablePath = process.env.ZQ_CHROMIUM;

export default defineConfig({
  resolve: { alias: { '@': fileURLToPath(new URL('./src', import.meta.url)) } },
  // The build-time constants of vite.config.ts, at their web values.
  define: { __TARGET__: JSON.stringify('web'), __DEV_ROUTES__: 'false' },
  test: {
    // Failure screenshots and other attachments go to the ignored .zq/, never to a tracked folder.
    attachmentsDir: '.zq/vitest/attachments',
    projects: [
      {
        extends: true,
        test: {
          name: 'node',
          include: ['{src,packages,tools}/**/*.test.{ts,tsx}'],
          exclude: [...configDefaults.exclude, BROWSER_TESTS],
          environment: 'node',
        },
      },
      {
        extends: true,
        test: {
          name: 'browser',
          include: [`packages/${BROWSER_TESTS}`],
          browser: {
            enabled: true,
            headless: true,
            provider: playwright(),
            instances: [
              {
                browser: 'chromium',
                provider: playwright({ launchOptions: executablePath ? { executablePath } : {} }),
              },
              { browser: 'firefox' },
              { browser: 'webkit' },
            ],
          },
        },
      },
    ],
    coverage: {
      provider: 'v8',
      include: ['src/**/*.{ts,tsx}', 'packages/*/src/**/*.ts', 'tools/**/*.ts'],
      exclude: ['**/*.test.{ts,tsx}', 'src/entries/**', 'src/env.d.ts'],
      // ARCHITECTURE.md 8.3; tools/ at 80% is our choice (8.3 names no floor for them).
      thresholds: {
        ...packageFloors,
        'src/engine/{player,progress,widgets}/**': floor,
        'src/engine/**': { lines: 80, branches: 80 },
        'tools/**': { lines: 80, branches: 80 },
      },
    },
  },
});
