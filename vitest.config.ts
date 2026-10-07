// Unit tests run in Node (ARCHITECTURE.md 8.1); browser projects arrive with the widget runtime.
import { fileURLToPath } from 'node:url';
import { defineConfig } from 'vitest/config';

export default defineConfig({
  resolve: { alias: { '@': fileURLToPath(new URL('./src', import.meta.url)) } },
  test: {
    include: ['{src,packages,tools}/**/*.test.ts'],
    environment: 'node',
    coverage: {
      provider: 'v8',
      include: ['src/**/*.ts', 'packages/*/src/**/*.ts', 'tools/**/*.ts'],
      exclude: ['**/*.test.ts', 'src/entries/**', 'src/env.d.ts'],
      // ARCHITECTURE.md 8.3: 90% for packages; tools at 80% [our choice].
      thresholds: {
        'packages/*/src/**': { lines: 90, branches: 90 },
        'tools/**': { lines: 80, branches: 80 },
      },
    },
  },
});
