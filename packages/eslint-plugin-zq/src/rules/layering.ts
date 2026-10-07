// zq/layering: who may import whom (ARCHITECTURE.md 4.5), configured in eslint.config.js.
// The importing file's layer is the first whose `files` glob matches its repository path. Every
// import is resolved to a repository path (relative, `@/x` for `src/x`, or a mapped workspace
// package) or else to `npm:<specifier>`. A repository target must match an `allow` glob and no
// `deny` glob; an `npm:` target is refused only by `deny`.
// Decision notes:
// - Globs (util/glob.ts) take two tokens: `$1`, the importer's first `*` capture in its `files`
//   glob (a screen imports only `src/screens/$1/**`), and `$dir`, the importer's directory (a
//   widget's logic.ts imports its own folder as `$dir/**` at any depth of the widget tree).
//   `$dir` was chosen over one `files` glob per depth because widget folders sit two or three
//   levels below src/widgets.
// - Extensions `.ts .tsx .js .mjs .cjs` and a trailing `/index` are stripped from importer, target
//   and every pattern before matching, so `src/engine/rpc` covers `rpc.ts` and `rpc/index.ts`.
// - Vite query suffixes (`./icon.svg?raw`) are dropped before resolving.
// - Type-only imports are checked like any other: a layer that may not import a module may not
//   import its types either. Covered: import, export from, export * from, literal import(), and
//   TypeScript's `import('x').T` types.
// - Per file, each pattern compiles once; each import is then O(patterns of the layer).
import path from 'node:path';
import type { Rule } from 'eslint';
import { staticString, type ESNode } from '../util/ast.ts';
import { glob } from '../util/glob.ts';
import { repoPath } from '../util/paths.ts';

interface Layer {
  readonly name: string;
  readonly files: readonly string[];
  readonly allow: readonly string[];
  readonly deny?: readonly string[];
}

interface Options {
  readonly layers: readonly Layer[];
  readonly packages: Readonly<Record<string, string>>;
}

const strip = (p: string) => p.replace(/\.(?:tsx?|[mc]?js)$/, '').replace(/(?:^|\/)index$/, '');
const patterns = { type: 'array', items: { type: 'string' } } as const;

/** The repository path an import specifier names, or `npm:<specifier>` for a bare package. */
function resolveTarget(specifier: string, importer: string, packages: Options['packages']): string {
  const spec = specifier.replace(/\?.*$/, '');
  if (spec === '.' || spec === '..' || spec.startsWith('./') || spec.startsWith('../')) {
    return path.posix.join(path.posix.dirname(importer), spec);
  }
  if (spec.startsWith('@/')) return `src/${spec.slice(2)}`;
  const name = spec.split('/', spec.startsWith('@') ? 2 : 1).join('/');
  const dir = Object.hasOwn(packages, name) ? packages[name] : undefined;
  return dir === undefined ? `npm:${spec}` : dir + spec.slice(name.length);
}

const rule: Rule.RuleModule = {
  meta: {
    type: 'problem',
    docs: { description: 'Enforce the layering of docs/ARCHITECTURE.md 4.5' },
    schema: [
      {
        type: 'object',
        properties: {
          layers: {
            type: 'array',
            items: {
              type: 'object',
              properties: { name: { type: 'string' }, files: patterns, allow: patterns, deny: patterns },
              required: ['name', 'files', 'allow'],
              additionalProperties: false,
            },
          },
          packages: { type: 'object', additionalProperties: { type: 'string' } },
        },
        required: ['layers', 'packages'],
        additionalProperties: false,
      },
    ],
    messages: { layer: '{{layer}} may not import {{target}} (ARCHITECTURE.md 4.5)' },
  },
  create(context) {
    const [{ layers, packages }] = context.options as [Options];
    const file = repoPath(context);
    const self = strip(file);
    let layer: Layer | undefined;
    let cap: string | undefined;
    for (const candidate of layers) {
      const match = candidate.files.map((f) => glob(strip(f)).exec(self)).find(Boolean);
      if (match) {
        layer = candidate;
        cap = match[1];
        break;
      }
    }
    if (!layer) return {};
    const { name } = layer;
    const tokens = { cap, dir: path.posix.dirname(file) };
    const allow = layer.allow.map((p) => glob(strip(p), tokens));
    const deny = (layer.deny ?? []).map((p) => glob(strip(p), tokens));

    const check = (source: ESNode | null | undefined) => {
      const specifier = staticString(source);
      if (!source || specifier === undefined) return;
      const target = resolveTarget(specifier, file, packages);
      const key = strip(target);
      const refused =
        deny.some((r) => r.test(key)) || (!target.startsWith('npm:') && !allow.some((r) => r.test(key)));
      if (refused) context.report({ node: source, messageId: 'layer', data: { layer: name, target } });
    };

    return {
      ImportDeclaration: (node) => {
        check(node.source);
      },
      ExportNamedDeclaration: (node) => {
        check(node.source);
      },
      ExportAllDeclaration: (node) => {
        check(node.source);
      },
      ImportExpression: (node) => {
        check(node.source);
      },
      TSImportType: (node: Rule.Node) => {
        check((node as unknown as { source: ESNode }).source);
      },
    };
  },
};

export default rule;
