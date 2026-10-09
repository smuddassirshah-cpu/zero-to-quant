// docs/ARCHITECTURE.md 5.1 to 5.3 against src: every exported declaration of the listings headed
// `// @zq/contracts/src/<module>.ts` must equal src's once both are printed without comments and with each
// run of whitespace as one space, each interface member compared on its own (its overloads together), and
// must live in the module the listing names. The type tests check meaning; this test stops the
// transcription drifting. A departure is allowed only where it is recorded below with its reason; when the
// doc adopts one, its row goes in the same pull request. The fixture cases pin the comparison itself.
import { readFileSync } from 'node:fs';
import ts from 'typescript';
import { describe, expect, test } from 'vitest';

const recorded: Record<string, string> = {
  'WidgetServices.tex': 'missing', // TexService is declared in src/engine/render (widget-api.ts)
  'WidgetServices.python': 'missing', // 5.9's types, with the second contracts unit
  'WidgetServices.sql': 'missing',
  WidgetSchemaModule: 'missing', // needs zod (widget.ts)
  CompilerRegistry: 'missing', // the second contracts unit
  Grade: 'added', // CONTENT-FORMAT.md 7.1 with 5.2's amendment (answer.ts)
  ShowStep: 'added', // CONTENT-FORMAT.md 3.2's shape (answer.ts)
};

const print = ts.createPrinter({ removeComments: true });
const listing = /```ts\n\/\/ @zq\/contracts\/src\/([\w-]+)\.ts[^\n]*\n([\s\S]*?)```/g;
type Decls = Map<string, { module: string; text: string }>;

/**
 * Each exported interface (its heading and each member) and type alias, printed without comments and with
 * whitespace collapsed, so a space inside a literal type still counts. A repeated name (an overload, or a
 * merged interface) keeps every text in source order. Returns any other statement but an import or
 * re-export, which this comparison would otherwise skip.
 */
function declarations(module: string, source: string, into: Decls): string[] {
  const skipped: string[] = [];
  const file = ts.createSourceFile(`${module}.ts`, source, ts.ScriptTarget.Latest, true);
  const flat = (node: ts.Node) =>
    print
      .printNode(ts.EmitHint.Unspecified, node, file)
      .replace(/\s+/g, ' ')
      .replace(/,(?= ?[)\]>}])/g, '');
  const add = (key: string, node: ts.Node) => {
    const prior = into.get(key);
    const text = flat(node);
    into.set(key, { module, text: prior ? `${prior.text} | ${text}` : text });
  };
  for (const node of file.statements) {
    const exported =
      ts.canHaveModifiers(node) && ts.getModifiers(node)?.some((m) => m.kind === ts.SyntaxKind.ExportKeyword);
    if (ts.isImportDeclaration(node) || ts.isExportDeclaration(node)) continue;
    if (exported && ts.isTypeAliasDeclaration(node)) {
      add(node.name.text, node);
      continue;
    }
    if (!exported || !ts.isInterfaceDeclaration(node)) {
      skipped.push(`${module}: ${flat(node).slice(0, 40)}`);
      continue;
    }
    const name = node.name.text;
    add(
      name,
      ts.factory.updateInterfaceDeclaration(
        node,
        node.modifiers,
        node.name,
        node.typeParameters,
        node.heritageClauses,
        [],
      ),
    );
    node.members.forEach((member, i) => {
      add(`${name}.${member.name ? member.name.getText(file).replace(/^'(.*)'$/, '$1') : `[${i}]`}`, member);
    });
  }
  return skipped;
}

/** The headed listings of `document` against `read(module)`, each departure keyed by declaration. */
function drift(document: string, read: (module: string) => string) {
  const doc: Decls = new Map();
  const src: Decls = new Map();
  const modules = [...document.matchAll(listing)].map(([, module = '', body = '']) => ({ module, body }));
  const skipped = modules.flatMap(({ module, body }) => [
    ...declarations(module, body, doc),
    ...declarations(module, read(module), src),
  ]);
  const found: Record<string, string> = {};
  for (const key of new Set([...doc.keys(), ...src.keys()])) {
    const [owner = key, member] = key.split('.');
    if (member && !(doc.has(owner) && src.has(owner))) continue; // reported with its interface
    const [d, s] = [doc.get(key), src.get(key)];
    if (!s) found[key] = 'missing';
    else if (!d) found[key] = 'added';
    else if (d.text !== s.text) found[key] = 'changed';
    else if (!member && d.module !== s.module) found[key] = `in ${s.module}.ts`;
  }
  return { modules: modules.map(({ module }) => module), skipped, found };
}

test('src transcribes 5.1 to 5.3, apart from the recorded deviations', () => {
  const architecture = readFileSync(new URL('../../../docs/ARCHITECTURE.md', import.meta.url), 'utf8');
  const { modules, skipped, found } = drift(
    architecture.slice(architecture.indexOf('### 5.1 '), architecture.indexOf('### 5.4 ')),
    (module) => readFileSync(new URL(`../src/${module}.ts`, import.meta.url), 'utf8'),
  );
  expect(modules).toEqual(['base', 'answer', 'widget', 'widget-api']);
  expect(skipped).toEqual([]);
  expect(found).toEqual(recorded);
});

describe('the comparison, on a fixture document', () => {
  const fence = '```';
  const tick = '`';
  const api = [
    'export interface Api {',
    '  // a comment the comparison ignores',
    '  announce(text: string): void;',
    '  pick(',
    '    a: string,',
    '    b: number,',
    '  ): void;',
    `  preset(ref: ${tick}\${string}@\${number}${tick}): boolean;`,
    '}',
  ].join('\n');
  const doc = (body: string) => `${fence}ts\n// @zq/contracts/src/m.ts (5.x)\n${body}\n${fence}\n`;
  const check = (docBody: string, srcBody: string) => drift(doc(docBody), () => srcBody).found;
  const edit = (from: string, to: string) => {
    expect(api).toContain(from);
    return api.replace(from, to);
  };

  test('comments, line breaks and trailing commas are not changes', () => {
    expect(
      check(
        api,
        edit('  pick(\n    a: string,\n    b: number,\n  ): void;', '  pick(a: string, b: number): void;'),
      ),
    ).toEqual({});
  });

  test('an overload is a change before or after the member it joins, in src or in the doc', () => {
    const before = edit(
      '  announce(text: string): void;',
      '  announce(text: string, polite: boolean): void;\n  announce(text: string): void;',
    );
    const after = edit(
      '  announce(text: string): void;',
      '  announce(text: string): void;\n  announce(text: string, polite: boolean): void;',
    );
    expect(check(api, before)).toEqual({ 'Api.announce': 'changed' });
    expect(check(api, after)).toEqual({ 'Api.announce': 'changed' });
    expect(check(before, api)).toEqual({ 'Api.announce': 'changed' });
    expect(check(before, before)).toEqual({});
    expect(check(before, after)).toEqual({ 'Api.announce': 'changed' });
  });

  test('a space inside a template literal type is a change, in src or in the doc', () => {
    const spaced = edit('string}@', 'string} @');
    expect(check(api, spaced)).toEqual({ 'Api.preset': 'changed' });
    expect(check(spaced, api)).toEqual({ 'Api.preset': 'changed' });
  });

  test('a declaration missing, added, moved, or repeated as a type alias', () => {
    const alias = 'export type Ref = string;';
    expect(check(`${api}\n${alias}`, api)).toEqual({ Ref: 'missing' });
    expect(check(api, `${api}\n${alias}`)).toEqual({ Ref: 'added' });
    expect(
      drift(`${doc(api)}${doc(alias).replace('/m.ts', '/n.ts')}`, (m) =>
        m === 'm' ? `${api}\n${alias}` : '',
      ).found,
    ).toEqual({
      Ref: 'in m.ts',
    });
    expect(check(alias, `${alias}\nexport type Ref = number;`)).toEqual({ Ref: 'changed' });
  });
});
