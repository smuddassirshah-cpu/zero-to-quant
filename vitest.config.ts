// Unit tests run in Node (ARCHITECTURE.md 8.1); browser projects arrive with the widget runtime.
import { fileURLToPath } from 'node:url';
import { defineConfig } from 'vitest/config';

export default defineConfig({
  resolve: { alias: { '@': fileURLToPath(new URL('./src', import.meta.url)) } },
  // The build-time constants of vite.config.ts, at their web values.
  define: { __TARGET__: JSON.stringify('web'), __DEV_ROUTES__: 'false' },
  test: {
    include: ['{src,packages,tools}/**/*.test.{ts,tsx}'],
    environment: 'node',
    coverage: {
      provider: 'v8',
      include: ['src/**/*.{ts,tsx}', 'packages/*/src/**/*.ts', 'tools/**/*.ts'],
      exclude: ['**/*.test.{ts,tsx}', 'src/entries/**', 'src/env.d.ts'],
      // ARCHITECTURE.md 8.3; tools/ at 80% is our choice (8.3 names no floor for them).
      thresholds: {
        'packages/*/src/**': { lines: 90, branches: 90 },
        'src/engine/{player,progress,widgets}/**': { lines: 90, branches: 90 },
        'src/engine/**': { lines: 80, branches: 80 },
        'tools/**': { lines: 80, branches: 80 },
      },
    },
  },
});
