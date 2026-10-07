// zq/no-forbidden-apis (scope `src/`, ARCHITECTURE.md 10.4): new windows, printing, embedded
// documents and code from strings are refused, and the service worker is reached only by the web
// platform.
// Decision notes:
// - Two checks run side by side. The syntactic one works everywhere, `.js` included: `window`,
//   `self` and `globalThis` when nothing in the file declares them, and a bare `open()`, `print()`
//   or `eval()` that scope analysis resolves to the global (a local or imported `open` is fine).
//   Where the type checker is available (`.ts`, `.tsx`) it also refuses `open`, `print`, `eval` and
//   `Function` on any `Window` (`parent`, `top`, `document.defaultView`, an alias), `serviceWorker`
//   on any `Navigator`, and calling or constructing anything typed `FunctionConstructor`, checked
//   with and without TypeScript wrappers, so `new (f.constructor as FunctionConstructor)()` fails.
// - The global `Function` is refused as a value wherever it appears, called or not
//   (`Reflect.construct(Function, args)`, passing it on); type positions are fine. Calling an
//   untyped `f.constructor(...)` is refused by typescript-eslint's `no-unsafe-call`.
// - Member accesses are refused whether or not they are called, and so is destructuring them.
// - Embedding elements (`iframe`, `object`, `embed`) are refused in JSX and as the literal tag of
//   `createElement`, `createElementNS`, `h`, `jsx` or `jsxs` on any receiver, case-insensitively
//   and with any namespace prefix (`'html:iframe'`) removed.
import type { Rule } from 'eslint';
import {
  hasType,
  isGlobal,
  jsxName,
  keyName,
  patternSource,
  propName,
  staticString,
  tailName,
  unwrap,
  type ESNode,
  type NodeOf,
} from '../util/ast.ts';
import { repoPath } from '../util/paths.ts';

const GLOBAL_OBJECTS = new Set(['window', 'self', 'globalThis']);
const BARE = new Set(['open', 'print', 'eval']);
const WINDOW_MEMBERS = new Set([...BARE, 'Function']);
const WINDOW_TYPES = new Set(['Window']);
const NAVIGATOR_TYPES = new Set(['Navigator', 'WorkerNavigator']);
const FUNCTION_TYPES = new Set(['FunctionConstructor']);
const EMBEDS = new Set(['iframe', 'object', 'embed']);
const FACTORIES = new Map([
  ['createElement', 0],
  ['createElementNS', 1],
  ['h', 0],
  ['jsx', 0],
  ['jsxs', 0],
]);
const SERVICE_WORKER_DIRS = ['src/platform/web/', 'src/sw/'];

const rule: Rule.RuleModule = {
  meta: {
    type: 'problem',
    docs: {
      description: 'Refuse window.open, print, embedded documents, eval, Function and stray service workers',
    },
    schema: [],
    messages: {
      forbidden: "'{{name}}' is forbidden in src/ (ARCHITECTURE.md 10.4)",
      serviceWorker:
        'navigator.serviceWorker is used only in src/platform/web/ and src/sw/ (ARCHITECTURE.md 10.4)',
    },
  },
  create(context) {
    const { sourceCode } = context;
    const file = repoPath(context);
    const workerAllowed = SERVICE_WORKER_DIRS.some((dir) => file.startsWith(dir));
    const globalObject = (node: ESNode) =>
      node.type === 'Identifier' && GLOBAL_OBJECTS.has(node.name) && isGlobal(sourceCode, node);
    const isWindow = (node: ESNode) => globalObject(node) || hasType(sourceCode, node, WINDOW_TYPES);
    const isNavigator = (node: ESNode) =>
      (node.type === 'Identifier' && node.name === 'navigator' && isGlobal(sourceCode, node)) ||
      (node.type === 'MemberExpression' && propName(node) === 'navigator' && globalObject(node.object)) ||
      hasType(sourceCode, node, NAVIGATOR_TYPES);
    // The global `Function` itself, or `Function` on a window: refused as values, see `Program`.
    const functionValue = (node: ESNode) =>
      (node.type === 'Identifier' && node.name === 'Function' && isGlobal(sourceCode, node)) ||
      (node.type === 'MemberExpression' && propName(node) === 'Function' && isWindow(node.object));
    const forbid = (node: ESNode, name: string) => {
      context.report({ node, messageId: 'forbidden', data: { name } });
    };
    // `owner.name`, read from `owner` by a member access or a destructuring pattern.
    const access = (node: ESNode, name: string, owner: ESNode) => {
      if (WINDOW_MEMBERS.has(name) && isWindow(owner)) forbid(node, `${sourceCode.getText(owner)}.${name}`);
      else if (name === 'serviceWorker' && !workerAllowed && isNavigator(owner)) {
        context.report({ node, messageId: 'serviceWorker' });
      }
    };
    const invoke = (node: NodeOf<'CallExpression' | 'NewExpression'>) => {
      const callee = unwrap(node.callee);
      const prefix = node.type === 'NewExpression' ? 'new ' : '';
      if (callee.type === 'Identifier' && BARE.has(callee.name) && isGlobal(sourceCode, callee)) {
        forbid(node, `${prefix}${callee.name}`);
      } else if (
        !functionValue(callee) &&
        (hasType(sourceCode, node.callee, FUNCTION_TYPES) || hasType(sourceCode, callee, FUNCTION_TYPES))
      ) {
        forbid(node, `${prefix}Function`);
      }
    };

    return {
      Program() {
        const scope = sourceCode.scopeManager.globalScope;
        const global = scope?.set.get('Function');
        const refs = [
          ...(global?.defs.length === 0 ? global.references : []),
          ...(scope?.through.filter((r) => r.identifier.name === 'Function') ?? []),
        ];
        for (const ref of refs) {
          const id = ref.identifier as Rule.Node;
          const typeOnly = (ref as { isValueReference?: boolean }).isValueReference === false;
          if (typeOnly || (id.parent?.type as string) === 'TSTypeQuery') continue;
          const constructed = id.parent?.type === 'NewExpression' && id.parent.callee === id;
          forbid(id, constructed ? 'new Function' : 'Function');
        }
      },
      MemberExpression(node) {
        const name = propName(node);
        if (name !== undefined) access(node, name, node.object);
      },
      Property(node) {
        const name = keyName(node);
        const owner = node.parent.type === 'ObjectPattern' ? patternSource(node.parent) : undefined;
        if (name !== undefined && owner) access(node, name, owner);
      },
      CallExpression(node) {
        invoke(node);
        const index = FACTORIES.get(tailName(node.callee) ?? '');
        const tag = index === undefined ? undefined : staticString(node.arguments[index]);
        const element = tag?.toLowerCase().replace(/^[^:]*:/, '');
        if (element && EMBEDS.has(element)) forbid(node, element);
      },
      NewExpression: invoke,
      JSXOpeningElement(node: Rule.Node) {
        const element = jsxName(node);
        if (element && EMBEDS.has(element)) forbid(node, element);
      },
    };
  },
};

export default rule;
