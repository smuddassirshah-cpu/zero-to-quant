// docs/DECISIONS.md B43: a contracts module that @zq/mathcore imports names no DOM type. base.ts, answer.ts and
// keys.ts are compiled with packages/mathcore/tsconfig.json's options (Node's libraries, no DOM), and must
// produce no diagnostic and pull in no other contracts module.
import { fileURLToPath } from 'node:url';
import ts from 'typescript';
import { expect, test } from 'vitest';

const here = (path: string) => fileURLToPath(new URL(path, import.meta.url));

test('base.ts, answer.ts and keys.ts compile without the DOM lib', { timeout: 60_000 }, () => {
  const tsconfig = here('../../mathcore/tsconfig.json');
  const read = ts.readConfigFile(tsconfig, (path) => ts.sys.readFile(path));
  expect(read.error).toBeUndefined();
  const parsed = ts.parseJsonConfigFileContent(read.config, ts.sys, here('../../mathcore/'));
  expect(parsed.options.lib).not.toContain('lib.dom.d.ts');
  const rootNames = ['base.ts', 'answer.ts', 'keys.ts'].map((name) => here(`../src/${name}`));
  const program = ts.createProgram({
    rootNames,
    options: { ...parsed.options, composite: false, incremental: false, noEmit: true },
  });
  const messages = ts
    .getPreEmitDiagnostics(program)
    .map((d) => ts.flattenDiagnosticMessageText(d.messageText, '\n'));
  expect(messages).toEqual([]);
  const contracts = program
    .getSourceFiles()
    .map((file) => file.fileName)
    .filter((name) => name.includes('/packages/contracts/'));
  expect(contracts.sort()).toEqual([...rootNames].sort());
});
