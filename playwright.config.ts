// Boot tests on the three paths (docs/ARCHITECTURE.md 8.1): the dev server, the web build through
// `vite preview` and the Artifact build through tools/artifact-host. Decision notes:
// - Playwright's `webServer` is a top-level list, so every run starts all three servers and needs both
//   builds (`npm run build`).
// - Servers are never reused: a run must test this worktree's build, not a server another session left
//   on the port. ZQ_PORT_DEV, ZQ_PORT_WEB and ZQ_PORT_ARTIFACT let parallel worktrees choose their own.
// - CI installs the Chromium this Playwright expects; elsewhere ZQ_CHROMIUM may name another binary.
import { defineConfig } from '@playwright/test';

function port(name: string, fallback: number): number {
  const value = process.env[name];
  if (value === undefined || value === '') return fallback;
  if (!/^\d{1,5}$/.test(value) || Number(value) > 65_535) throw new Error(`${name} is not a port: ${value}`);
  return Number(value);
}

const dev = port('ZQ_PORT_DEV', 5173);
const web = port('ZQ_PORT_WEB', 4173);
const artifact = port('ZQ_PORT_ARTIFACT', 4174);
const executablePath = process.env.ZQ_CHROMIUM;

export default defineConfig({
  testDir: 'tests/e2e',
  forbidOnly: !!process.env.CI,
  reporter: 'list',
  use: { browserName: 'chromium', launchOptions: executablePath ? { executablePath } : {} },
  projects: [
    { name: 'dev', use: { baseURL: `http://localhost:${dev}` } },
    { name: 'web', use: { baseURL: `http://localhost:${web}` } },
    { name: 'artifact', use: { baseURL: `http://127.0.0.1:${artifact}` } },
  ],
  webServer: [
    {
      name: 'dev',
      command: `npx vite --mode dev --port ${dev} --strictPort`,
      url: `http://localhost:${dev}/html/dev.html`,
      reuseExistingServer: false,
    },
    {
      name: 'web',
      command: `npx vite preview --mode web --port ${web} --strictPort`,
      url: `http://localhost:${web}/`,
      reuseExistingServer: false,
    },
    {
      name: 'artifact',
      command: `node tools/artifact-host/server.ts dist/artifact --port ${artifact}`,
      url: `http://127.0.0.1:${artifact}/`,
      reuseExistingServer: false,
    },
  ],
});
