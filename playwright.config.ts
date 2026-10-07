// Boot tests on the three paths (docs/ARCHITECTURE.md 8.1): the dev server, the web build through
// `vite preview` and the Artifact build through tools/artifact-host. Playwright's `webServer` is a
// top-level list, so every run starts all three servers and needs both builds (`npm run build`).
// CI installs the Chromium this Playwright expects; elsewhere ZQ_CHROMIUM may name another binary.
import { defineConfig } from '@playwright/test';

const executablePath = process.env.ZQ_CHROMIUM;
const reuseExistingServer = !process.env.CI;

export default defineConfig({
  testDir: 'tests/e2e',
  forbidOnly: !!process.env.CI,
  reporter: 'list',
  use: { browserName: 'chromium', launchOptions: executablePath ? { executablePath } : {} },
  projects: [
    { name: 'dev', use: { baseURL: 'http://localhost:5173' } },
    { name: 'web', use: { baseURL: 'http://localhost:4173' } },
    { name: 'artifact', use: { baseURL: 'http://127.0.0.1:4174' } },
  ],
  webServer: [
    {
      name: 'dev',
      command: 'npx vite --mode dev --port 5173 --strictPort',
      url: 'http://localhost:5173/html/dev.html',
      reuseExistingServer,
    },
    {
      name: 'web',
      command: 'npx vite preview --mode web --port 4173 --strictPort',
      url: 'http://localhost:4173/',
      reuseExistingServer,
    },
    {
      name: 'artifact',
      command: 'node tools/artifact-host/server.ts dist/artifact --port 4174',
      url: 'http://127.0.0.1:4174/',
      reuseExistingServer,
    },
  ],
});
