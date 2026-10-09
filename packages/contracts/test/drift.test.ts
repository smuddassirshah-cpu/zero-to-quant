// docs/ARCHITECTURE.md 5.1 to 5.14 against src: every exported declaration of the listings headed
// `// @zq/contracts/src/<module>.ts` must equal src's once both are printed without comments and with each
// run of whitespace as one space, each interface member compared on its own (its overloads together), and
// must live in the module the listing names. So must the listings src transcribes from elsewhere: 5.11's
// TexService (render.ts), ASSESSMENT.md 13.2 and 13.5 (events.ts), and AI-TUTOR.md 4.1 and 6.1 (platform.ts).
// The type tests check meaning; this test stops the transcription drifting. A departure is allowed only where
// it is recorded below with its reason; when the doc adopts one, its row goes in the same pull request. The
// fixture cases pin the comparison itself.
import { readFileSync } from 'node:fs';
import ts from 'typescript';
import { describe, expect, test } from 'vitest';

const recorded: Record<string, string> = {
  'Scope.listen': 'changed', // AddEventListenerOptions is not a Node global (base.ts)
  'Scope.effect': 'changed', // signals-core's own parameter type; the doc's union fails lint (base.ts)
  ClusterId: 'changed', // 26 clusters, WIDGETS.md decision 19 (widget.ts)
  WidgetState: 'changed', // a Readonly alias, so a state is Json (widget.ts); its members are the alias's
  'WidgetState.a': 'missing',
  'WidgetState.v': 'missing',
  'CompilerRegistry.widget': 'changed', // the erased types accept no concrete widget (widget.ts)
  'CompilerRegistry.preset': 'changed',
  'WidgetRegistry.load': 'changed',
  PresetRuntime: 'changed',
  AnyWidgetLogic: 'added',
  AnyPresetDef: 'added',
  AnyWidgetModule: 'added',
  Grade: 'added', // CONTENT-FORMAT.md 7.1 with 5.2's amendment (answer.ts)
  ShowStep: 'added', // CONTENT-FORMAT.md 3.2's shape (answer.ts)
  CasService: 'in answer.ts', // GradeCtx needs it without the DOM lib; widget-api.ts re-exports it
  WidgetViewProps: 'in widget-api.ts', // the view half: preact's types bring the DOM lib (widget.ts)
  WidgetView: 'in widget-api.ts',
  WidgetModule: 'in widget-api.ts',
  'KeyValue.get': 'changed', // returns Json: the doc's generic fails lint (platform.ts)
  CourseBundle: 'added', // @zq/content-schema's outputs, opaque here (platform.ts)
  ItemBody: 'added',
  Glossary: 'added',
  NotebookCards: 'added',
  TutorErrorCode: 'added', // AI-TUTOR.md 6.4's table (platform.ts)
  EventKind: 'added', // ASSESSMENT.md 13.2's table (events.ts)
  AttemptContext: 'added',
  EventDraft: 'added',
  Ev: 'added',
  Snapshot: 'added', // no paper defines these three: opaque (events.ts)
  DraftHandle: 'added',
  ImportReport: 'added',
  PrimType: 'added', // 5.14's comment, from WIDGETS.md 4.1 and 4.2 (scene.ts)
  Bindable: 'added', // no paper defines these four (scene.ts)
  MarkType: 'added',
  SpaceToken: 'added',
  DeclarativeRecipe: 'added',
  PathOf: 'changed', // the doc's listing writes `string` with a comment (scene.ts)
  defineScene: 'missing', // a function: src/widgets/scene/define.ts (scene.ts)
};

const print = ts.createPrinter({ removeComments: true });
const fenced = /```ts\n([\s\S]*?)```/g;
const headed = (line: string) => /^\/\/ @zq\/contracts\/src\/([\w-]+)\.ts/.exec(line)?.[1];
type Decls = Map<string, { module: string; text: string }>;
interface Listing {
  module: string;
  body: string;
}

/** The ts listings of `text` that `pick` assigns a module by their first line; `exporting` exports a paper's bare declarations. */
function listings(text: string, pick: (line: string) => string | undefined, exporting = false): Listing[] {
  return [...text.matchAll(fenced)].flatMap(([, body = '']) => {
    const module = pick(body.slice(0, body.indexOf('\n')));
    if (module === undefined) return [];
    return [{ module, body: exporting ? body.replace(/^(interface|type) /gm, 'export $1 ') : body }];
  });
}

/**
 * Each exported interface (its heading and each member), type alias and function signature, printed without
 * comments and with whitespace collapsed, so a space inside a literal type still counts. A repeated name (an
 * overload, or a merged interface) keeps every text in source order. Module-private types and `declare`
 * statements are erased and outside the contract. Returns any other statement but an import or re-export,
 * which this comparison would otherwise skip.
 */
function declarations(module: string, source: string, into: Decls): string[] {
  const skipped: string[] = [];
  const file = ts.createSourceFile(`${module}.ts`, source, ts.ScriptTarget.Latest, true);
  const flat = (node: ts.Node) =>
    print
      .printNode(ts.EmitHint.Unspecified, node, file)
      .replace(/\s+/g, ' ')
      .replace(/,(?= ?[)\]>}])/g, ''); // a guard: TypeScript 6.0.3's printer drops trailing commas itself
  const add = (key: string, node: ts.Node) => {
    const prior = into.get(key);
    const text = flat(node);
    into.set(key, { module, text: prior ? `${prior.text} | ${text}` : text });
  };
  const has = (node: ts.Node, kind: ts.SyntaxKind) =>
    ts.canHaveModifiers(node) && (ts.getModifiers(node)?.some((m) => m.kind === kind) ?? false);
  for (const node of file.statements) {
    const exported = has(node, ts.SyntaxKind.ExportKeyword);
    const erased =
      ts.isTypeAliasDeclaration(node) ||
      ts.isInterfaceDeclaration(node) ||
      has(node, ts.SyntaxKind.DeclareKeyword);
    if (ts.isImportDeclaration(node) || ts.isExportDeclaration(node) || (!exported && erased)) continue;
    const alias =
      ts.isTypeAliasDeclaration(node) || (ts.isFunctionDeclaration(node) && !node.body)
        ? node.name
        : undefined;
    if (exported && alias) {
      add(alias.text, node);
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

/** `all` against `read(module)` for each module they name, each departure keyed by declaration. */
function drift(all: Listing[], read: (module: string) => string) {
  const doc: Decls = new Map();
  const src: Decls = new Map();
  const modules = [...new Set(all.map(({ module }) => module))];
  const skipped = [
    ...all.flatMap(({ module, body }) => declarations(module, body, doc)),
    ...modules.flatMap((module) => declarations(module, read(module), src)),
  ];
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
  return { modules, skipped, found };
}

test('src transcribes 5.1 to 5.14 and the papers it cites, apart from the recorded deviations', () => {
  const read = (path: string) => readFileSync(new URL(path, import.meta.url), 'utf8');
  const [architecture, assessment, tutor] = ['ARCHITECTURE', 'ASSESSMENT', 'AI-TUTOR'].map((name) =>
    read(`../../../docs/${name}.md`),
  ) as [string, string, string];
  const section = (text: string, from: string, to: string) => {
    const [start, end] = [text.indexOf(from), text.indexOf(to, text.indexOf(from))];
    expect([start, end].every((i) => i >= 0)).toBe(true);
    return text.slice(start, end);
  };
  const { modules, skipped, found } = drift(
    [
      ...listings(section(architecture, '### 5.1 ', '\n## 6. '), (line) =>
        line === '// src/engine/render' ? 'render' : headed(line),
      ),
      ...listings(section(assessment, '### 13.2 ', '### 13.6 '), () => 'events', true),
      ...listings(section(tutor, '### 6.1 ', '### 6.2 '), () => 'platform', true),
      ...listings(section(tutor, '### 4.1 ', '### 4.2 '), () => 'platform', true),
    ],
    (module) => read(`../src/${module}.ts`),
  );
  expect(modules).toEqual([
    'base',
    'answer',
    'widget',
    'widget-api',
    'platform',
    'render',
    'scene',
    'events',
  ]);
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
  const check = (docBody: string, srcBody: string) =>
    drift(listings(doc(docBody), headed), () => srcBody).found;
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
      drift(listings(`${doc(api)}${doc(alias).replace('/m.ts', '/n.ts')}`, headed), (m) =>
        m === 'm' ? `${api}\n${alias}` : '',
      ).found,
    ).toEqual({
      Ref: 'in m.ts',
    });
    expect(check(alias, `${alias}\nexport type Ref = number;`)).toEqual({ Ref: 'changed' });
  });
  test('a function signature is compared; runtime code is skipped, private types are not', () => {
    const fn = 'export function f(a: string): number;';
    expect(check(fn, '')).toEqual({ f: 'missing' });
    expect(check(fn, `${fn}\ntype Private = string;\ndeclare const brand: unique symbol;`)).toEqual({});
    expect(drift(listings(doc('export const x = 1;'), headed), () => fn).skipped).toEqual([
      'm: export const x = 1;',
    ]);
    expect(drift(listings(doc(fn), headed), () => 'export function f() { return 1; }').skipped).toEqual([
      'm: export function f() { return 1; }',
    ]);
  });
});
