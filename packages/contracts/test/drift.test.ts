// docs/ARCHITECTURE.md 5.1 to 5.3 against src: every exported declaration of the listings headed
// `// @zq/contracts/src/<module>.ts` must equal src's once both are printed without comments or whitespace,
// each interface member compared on its own, and must live in the module the listing names. The type
// tests check meaning; this test stops the transcription drifting. A departure is allowed only where it is
// recorded below with its reason; when the doc adopts one, its row goes in the same pull request.
import { readFileSync } from 'node:fs';
import ts from 'typescript';
import { expect, test } from 'vitest';

const recorded: Record<string, string> = {
  'Scope.listen': 'changed', // AddEventListenerOptions is not a Node global (base.ts)
  'Scope.effect': 'changed', // signals-core's own parameter type; the doc's union fails lint (base.ts)
  ClusterId: 'changed', // 26 clusters, WIDGETS.md decision 19 (widget.ts)
  'WidgetServices.tex': 'missing', // TexService is declared in src/engine/render (widget-api.ts)
  'WidgetServices.python': 'missing', // 5.9's types, with the second contracts unit
  'WidgetServices.sql': 'missing',
  WidgetSchemaModule: 'missing', // needs zod (widget.ts)
  CompilerRegistry: 'missing', // the second contracts unit
  Grade: 'added', // CONTENT-FORMAT.md 7.1 with 5.2's amendment (answer.ts)
  ShowStep: 'added', // CONTENT-FORMAT.md 3.2's shape (answer.ts)
  CasService: 'in answer.ts', // GradeCtx needs it without the DOM lib; widget-api.ts re-exports it
  WidgetViewProps: 'in widget-api.ts', // the view half: preact's types bring the DOM lib (widget.ts)
  WidgetView: 'in widget-api.ts',
  WidgetModule: 'in widget-api.ts',
};

const print = ts.createPrinter({ removeComments: true });
type Decls = Map<string, { module: string; text: string }>;

/**
 * Each exported interface (its heading and each member) and type alias, printed without comments or spaces.
 * Returns any other statement but an import or re-export, which this comparison would otherwise skip.
 */
function declarations(module: string, source: string, into: Decls): string[] {
  const skipped: string[] = [];
  const file = ts.createSourceFile(`${module}.ts`, source, ts.ScriptTarget.Latest, true);
  const flat = (node: ts.Node) =>
    print
      .printNode(ts.EmitHint.Unspecified, node, file)
      .replace(/\s+/g, '')
      .replace(/,(?=[)\]>}])/g, '');
  for (const node of file.statements) {
    const exported =
      ts.canHaveModifiers(node) && ts.getModifiers(node)?.some((m) => m.kind === ts.SyntaxKind.ExportKeyword);
    if (ts.isImportDeclaration(node) || ts.isExportDeclaration(node)) continue;
    if (exported && ts.isTypeAliasDeclaration(node)) {
      into.set(node.name.text, { module, text: flat(node) });
      continue;
    }
    if (!exported || !ts.isInterfaceDeclaration(node)) {
      skipped.push(`${module}: ${flat(node).slice(0, 40)}`);
      continue;
    }
    const name = node.name.text;
    const heading = ts.factory.updateInterfaceDeclaration(
      node,
      node.modifiers,
      node.name,
      node.typeParameters,
      node.heritageClauses,
      [],
    );
    into.set(name, { module, text: flat(heading) });
    node.members.forEach((member, i) => {
      const key = member.name ? member.name.getText(file).replace(/^'(.*)'$/, '$1') : `[${i}]`;
      into.set(`${name}.${key}`, { module, text: flat(member) });
    });
  }
  return skipped;
}

test('src transcribes 5.1 to 5.3, apart from the recorded deviations', () => {
  const architecture = readFileSync(new URL('../../../docs/ARCHITECTURE.md', import.meta.url), 'utf8');
  const sections = architecture.slice(architecture.indexOf('### 5.1 '), architecture.indexOf('### 5.4 '));
  const doc: Decls = new Map();
  const src: Decls = new Map();
  const modules = [
    ...sections.matchAll(/```ts\n\/\/ @zq\/contracts\/src\/([\w-]+)\.ts([^\n]*)\n([\s\S]*?)```/g),
  ].map(([, module = '', , body = '']) => ({ module, body }));
  expect(modules.map(({ module }) => module)).toEqual(['base', 'answer', 'widget', 'widget-api']);
  const skipped = modules.flatMap(({ module, body }) => [
    ...declarations(module, body, doc),
    ...declarations(module, readFileSync(new URL(`../src/${module}.ts`, import.meta.url), 'utf8'), src),
  ]);
  expect(skipped).toEqual([]);
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
  expect(found).toEqual(recorded);
});
