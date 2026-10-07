// zq/no-forbidden-apis (scope `src/`, ARCHITECTURE.md 10.4): new windows, printing, iframes and
// code from strings are refused, and the service worker is reached only by the web platform.
// Decision notes:
// - A bare `open()`, `print()`, `eval()` or `Function()` is refused only when scope analysis finds
//   no declaration for it in the file, so a local `open` or an imported `print` is fine. The same
//   holds for the `window`, `self` and `globalThis` objects of a member access.
// - Member accesses are refused whether or not they are called (`const o = window.open` too).
// - `createElement` and `createElementNS` are matched on any object, so `doc.createElement` and
//   `el.ownerDocument.createElement` are covered; the tag literal is compared case-insensitively.
import type { Rule } from 'eslint';
import { isGlobal, jsxName, propName, staticString, type ESNode, type NodeOf } from '../util/ast.ts';
import { repoPath } from '../util/paths.ts';

const GLOBAL_OBJECTS = new Set(['window', 'self', 'globalThis']);
const MEMBERS = new Set(['open', 'print', 'eval', 'Function']);
const SERVICE_WORKER_DIRS = ['src/platform/web/', 'src/sw/'];

const rule: Rule.RuleModule = {
  meta: {
    type: 'problem',
    docs: {
      description: 'Refuse window.open, print, iframes, eval, new Function and stray service-worker use',
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
      node.type === 'Identifier' && GLOBAL_OBJECTS.has(node.name) && isGlobal(sourceCode, node)
        ? node.name
        : undefined;
    const isNavigator = (node: ESNode) =>
      node.type === 'Identifier'
        ? node.name === 'navigator' && isGlobal(sourceCode, node)
        : node.type === 'MemberExpression' && propName(node) === 'navigator' && !!globalObject(node.object);
    const forbid = (node: ESNode, name: string) => {
      context.report({ node, messageId: 'forbidden', data: { name } });
    };
    const bare = (node: NodeOf<'CallExpression' | 'NewExpression'>, prefix: string) => {
      const { callee } = node;
      if (callee.type === 'Identifier' && MEMBERS.has(callee.name) && isGlobal(sourceCode, callee)) {
        forbid(node, `${prefix}${callee.name}`);
      }
    };

    return {
      MemberExpression(node) {
        const name = propName(node);
        if (name === undefined) return;
        const owner = globalObject(node.object);
        if (owner && MEMBERS.has(name)) forbid(node, `${owner}.${name}`);
        else if (name === 'serviceWorker' && !workerAllowed && isNavigator(node.object)) {
          context.report({ node, messageId: 'serviceWorker' });
        }
      },
      CallExpression(node) {
        bare(node, '');
        const method = propName(node.callee);
        const tag =
          method === 'createElement'
            ? node.arguments[0]
            : method === 'createElementNS'
              ? node.arguments[1]
              : undefined;
        if (tag && staticString(tag)?.toLowerCase() === 'iframe') forbid(node, 'iframe');
      },
      NewExpression(node) {
        bare(node, 'new ');
      },
      JSXOpeningElement(node: Rule.Node) {
        if (jsxName(node) === 'iframe') forbid(node, 'iframe');
      },
    };
  },
};

export default rule;
