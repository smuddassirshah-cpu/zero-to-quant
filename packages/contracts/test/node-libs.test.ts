// docs/DECISIONS.md B43: a contracts module that a no-DOM package imports (@zq/mathcore, @zq/graders, and
// @zq/compiler through widget.ts, scene.ts and platform.ts's Manifest; the workers through events.ts) names no
// DOM type. They are compiled with packages/mathcore/tsconfig.json's
// options (Node's libraries, no DOM) and must produce no diagnostic, pull in no other contracts module, and
// reach no `/// <reference lib="dom" />` through a dependency's declarations (preact's jsx.d.ts has one).
import { basename } from 'node:path';
import { fileURLToPath } from 'node:url';
import ts from 'typescript';
import { describe, expect, test } from 'vitest';

const here = (path: string) => fileURLToPath(new URL(path, import.meta.url));
const pure = [
  'base.ts',
  'answer.ts',
  'widget.ts',
  'keys.ts',
  'events.ts',
  'platform.ts',
  'render.ts',
  'scene.ts',
];

function compile(names: string[]) {
  const read = ts.readConfigFile(here('../../mathcore/tsconfig.json'), (path) => ts.sys.readFile(path));
  expect(read.error).toBeUndefined();
  const parsed = ts.parseJsonConfigFileContent(read.config, ts.sys, here('../../mathcore/'));
  expect(parsed.options.lib).not.toContain('lib.dom.d.ts');
  const rootNames = names.map((name) => here(`../src/${name}`));
  const program = ts.createProgram({
    rootNames,
    options: { ...parsed.options, composite: false, incremental: false, noEmit: true },
  });
  const files = program.getSourceFiles().map((file) => file.fileName);
  return {
    rootNames,
    messages: ts
      .getPreEmitDiagnostics(program)
      .map((d) => ts.flattenDiagnosticMessageText(d.messageText, '\n')),
    dom: files.map((name) => basename(name)).filter((name) => name.startsWith('lib.dom')),
    contracts: files.filter((name) => name.includes('/packages/contracts/')).sort(),
  };
}

describe('the modules no-DOM packages import (B43)', { timeout: 60_000 }, () => {
  test(`${pure.join(', ')} compile with Node's libraries alone`, () => {
    const { rootNames, messages, dom, contracts } = compile(pure);
    expect(messages).toEqual([]);
    expect(dom).toEqual([]);
    expect(contracts).toEqual([...rootNames].sort());
  });

  test("control: widget-api.ts imports preact's types, which bring the DOM lib", () => {
    expect(compile(['widget-api.ts']).dom).toContain('lib.dom.d.ts');
  });
});
