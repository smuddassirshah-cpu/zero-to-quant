// zq/layering: who may import whom (ARCHITECTURE.md 4.5), configured in eslint.config.js.
// The importing file's layer is the first whose `files` glob matches its repository path. Every
// import is resolved to a normalised repository path (relative, `@/x` for `src/x`, or a mapped
// workspace package) or else to `npm:<specifier>`. A repository target must match an `allow` glob
// (or, for a type-only import, an `allowTypes` glob) and must not be denied; an `npm:` target is
// refused only when denied.
// Decision notes:
// - A `deny` list reads in order and its last match wins; a `!` prefix re-allows, so
//   `['npm:**', '!npm:zod']` refuses every package but zod.
// - Globs (util/glob.ts) take two tokens: `$1`, the importer's first `*` capture in its `files`
//   glob (a screen imports only `src/screens/$1/**`), and `$dir`, the importer's directory (a
//   widget's logic.ts imports its own folder as `$dir/**` at any depth of the widget tree).
// - Extensions (`.ts .tsx .mts .cts .js .mjs .cjs`) are stripped from the importer, the target and
//   every pattern; a trailing `/index` from targets and their patterns only, so `src/engine/rpc`
//   covers `rpc.ts` and `rpc/index.ts` while `src/screens/index.ts` still matches its layer.
// - Refused outright, each with its own message: a specifier that is absolute or normalises outside
//   the repository, a package subpath that leaves its package through `..`, and an `@zq/` name the
//   `packages` map does not know.
// - Type-only imports (`import type`, `export type`, every specifier `type`, TypeScript's
//   `import('x').T`) are checked too: they may also reach `allowTypes`, and `deny` still applies.
// - Dynamic `import()`: a template literal or `+` with a static prefix is checked as `<prefix>**`,
//   matched as a string, so it passes only where the whole directory would; one with no static
//   prefix is refused in a layer that has a deny list. Vite queries (`?raw`) are dropped.
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
  readonly allowTypes?: readonly string[];
  readonly deny?: readonly string[];
  readonly note?: string;
}

interface Options {
  readonly layers: readonly Layer[];
  readonly packages: Readonly<Record<string, string>>;
}

type Target = { readonly path: string } | { readonly problem: 'outside' | 'escape' | 'unmapped' };

interface Kinded {
  readonly importKind?: string;
  readonly exportKind?: string;
  readonly specifiers?: readonly { readonly importKind?: string; readonly exportKind?: string }[];
}

const stripExt = (p: string) => p.replace(/\.(?:[mc]?ts|tsx|[mc]?js)$/, '');
const stripAll = (p: string) => stripExt(p).replace(/(?:^|\/)index$/, '');
const patterns = { type: 'array', items: { type: 'string' } } as const;

/** The normalised repository path a specifier names, `npm:<specifier>`, or why it is refused. */
function resolveTarget(specifier: string, importer: string, packages: Options['packages']): Target {
  const spec = specifier.replace(/\?.*$/, '');
  if (spec.startsWith('/')) return { problem: 'outside' };
  let target: string;
  if (spec === '.' || spec === '..' || spec.startsWith('./') || spec.startsWith('../')) {
    target = path.posix.join(path.posix.dirname(importer), spec);
  } else if (spec.startsWith('@/')) {
    target = path.posix.normalize(`src/${spec.slice(2)}`);
  } else {
    const name = spec.split('/', spec.startsWith('@') ? 2 : 1).join('/');
    const dir = Object.hasOwn(packages, name) ? packages[name] : undefined;
    if (dir === undefined) return name.startsWith('@zq/') ? { problem: 'unmapped' } : { path: `npm:${spec}` };
    target = path.posix.normalize(dir + spec.slice(name.length));
    if (target !== dir && !target.startsWith(`${dir}/`)) return { problem: 'escape' };
  }
  return target === '..' || target.startsWith('../') ? { problem: 'outside' } : { path: target };
}

/** The static start of a computed specifier: a template's first quasi or the left of a `+`. */
function staticPrefix(node: ESNode): string | undefined {
  if (node.type === 'TemplateLiteral') return node.quasis[0]?.value.cooked ?? undefined;
  if (node.type === 'BinaryExpression' && node.operator === '+') {
    return staticString(node.left) ?? staticPrefix(node.left);
  }
  return undefined;
}

function typeOnly(node: ESNode): boolean {
  const { importKind, exportKind, specifiers = [] } = node as unknown as Kinded;
  if (importKind === 'type' || exportKind === 'type') return true;
  return specifiers.length > 0 && specifiers.every((s) => s.importKind === 'type' || s.exportKind === 'type');
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
              properties: {
                name: { type: 'string' },
                files: patterns,
                allow: patterns,
                allowTypes: patterns,
                deny: patterns,
                note: { type: 'string' },
              },
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
    messages: {
      layer: '{{layer}} may not import {{target}} (ARCHITECTURE.md 4.5)',
      layerNote: '{{layer}} may not import {{target}} (ARCHITECTURE.md 4.5): {{note}}',
      dynamic: '{{layer}} may not import a computed specifier; name the module (ARCHITECTURE.md 4.5)',
      outside: "'{{specifier}}' resolves outside the repository (ARCHITECTURE.md 4.5)",
      escape: "'{{specifier}}' leaves its package's directory through '..' (ARCHITECTURE.md 4.5)",
      unmapped: "'{{specifier}}' is not in zq/layering's packages map; add the package in eslint.config.js",
    },
  },
  create(context) {
    const [{ layers, packages }] = context.options as [Options];
    const file = repoPath(context);
    const self = stripExt(file);
    let layer: Layer | undefined;
    let cap: string | undefined;
    for (const candidate of layers) {
      const match = candidate.files.map((f) => glob(stripExt(f)).exec(self)).find(Boolean);
      if (match) {
        layer = candidate;
        cap = match[1];
        break;
      }
    }
    if (!layer) return {};
    const { name, note } = layer;
    const tokens = { cap, dir: path.posix.dirname(file) };
    const compile = (list: readonly string[] = []) => list.map((p) => glob(stripAll(p), tokens));
    const allow = compile(layer.allow);
    const allowTypes = compile(layer.allowTypes);
    const deny = (layer.deny ?? []).map((p) => ({
      negate: p.startsWith('!'),
      regex: glob(stripAll(p.replace(/^!/, '')), tokens),
    }));
    const denied = (key: string) =>
      deny.reduce((hit, { negate, regex }) => (regex.test(key) ? !negate : hit), false);

    const check = (source: ESNode | null | undefined, types: boolean, dynamic: boolean) => {
      if (!source) return;
      const exact = staticString(source);
      const specifier = exact ?? staticPrefix(source);
      if (!specifier) {
        if (dynamic && deny.length > 0)
          context.report({ node: source, messageId: 'dynamic', data: { layer: name } });
        return;
      }
      const resolved = resolveTarget(specifier, file, packages);
      if ('problem' in resolved) {
        context.report({ node: source, messageId: resolved.problem, data: { specifier } });
        return;
      }
      const target = exact === undefined ? `${resolved.path}**` : resolved.path;
      const key = exact === undefined ? target : stripAll(target);
      const reached = (list: RegExp[]) => list.some((r) => r.test(key));
      const refused =
        denied(key) || (!target.startsWith('npm:') && !reached(allow) && !(types && reached(allowTypes)));
      if (!refused) return;
      const data = { layer: name, target, note: note ?? '' };
      context.report({ node: source, messageId: note ? 'layerNote' : 'layer', data });
    };

    return {
      ImportDeclaration: (node) => {
        check(node.source, typeOnly(node), false);
      },
      ExportNamedDeclaration: (node) => {
        check(node.source, typeOnly(node), false);
      },
      ExportAllDeclaration: (node) => {
        check(node.source, typeOnly(node), false);
      },
      ImportExpression: (node) => {
        check(node.source, false, true);
      },
      TSImportType: (node: Rule.Node) => {
        check((node as unknown as { source: ESNode }).source, true, false);
      },
    };
  },
};

export default rule;
