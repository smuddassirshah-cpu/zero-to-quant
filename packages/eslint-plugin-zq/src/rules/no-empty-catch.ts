// zq/no-empty-catch: errors are handled or propagated, never swallowed (CLAUDE.md security floor).
// A handler is a `catch` clause, or the function passed to `.catch(fn)` or as the second argument
// of `.then(a, fn)`: inline, behind TypeScript wrappers (`as`, `!`, `satisfies`), or a local
// function or `const` arrow named by an identifier. Imported or unknown handlers pass: they
// cannot be seen. A handler passes when it throws, calls a logger, or lets its error leave.
// Decision notes:
// - The error leaves when a read of its binding reaches `return`, `throw`, `yield`, an arrow's
//   implicit return, an argument of a call other than a pure conversion (`String`, `Number`,
//   `Boolean`, `JSON.stringify`), a JSX expression, or an assignment to a variable or property
//   declared outside the handler. Member access (`e.message`), conversions, templates, `+`, `?:`
//   branches, `??` and `||`, spreads, TypeScript wrappers and object and array literals carry it
//   on the way. A read in a test, under `void` or in a discarded statement does not count. One
//   level of local `const` is traced: `const text = String(e); show(text)` passes, while a `let`,
//   or a `const` copied into another, is not followed.
// - Accepted residue: a call carries the error even into a function that drops it
//   (`Math.max(Number(e))`), an immediately called arrow counts as its implicit return
//   (`(() => e)()`), and `&&` carries it to a `return` that does not return it
//   (`return e && undefined`). Telling these apart needs data flow; review catches them.
// - One pass collects the facts. A stack holds the open frames (catch clauses and every function);
//   a `throw` or logger call marks frames down to and including the nearest function, so one
//   inside a nested function counts for that function only. Marking stops at a frame already
//   marked (everything below it was marked by the same earlier walk), which keeps the pass O(n).
//   Function handlers are judged at `Program:exit`, since a named one may be declared later.
// - A logger call is `<logger>.<method>(...)` where `<logger>` is an identifier or the last
//   property of a member access (`this.log.warn`), so injected loggers count.
import type { Rule, Scope, SourceCode } from 'eslint';
import { findVariable, propName, tailName, unwrap, type ESNode, type NodeOf } from '../util/ast.ts';

type Fn = NodeOf<'FunctionDeclaration' | 'FunctionExpression' | 'ArrowFunctionExpression'>;

interface Frame {
  readonly node: ESNode;
  readonly fn: boolean;
  handled: boolean;
}

const METHODS = new Set(['error', 'warn', 'info', 'log']);
const DEFAULT_LOGGERS = ['log', 'logger', 'console'];
const CONVERSIONS = new Set(['String', 'Number', 'Boolean', 'JSON.stringify']);
const CARRIERS = new Set([
  'ArrayExpression',
  'AwaitExpression',
  'ChainExpression',
  'LogicalExpression',
  'ObjectExpression',
  'SpreadElement',
  'TemplateLiteral',
  'TSAsExpression',
  'TSNonNullExpression',
  'TSSatisfiesExpression',
  'TSTypeAssertion',
]);

const isFn = (node: ESNode | null | undefined): node is Fn =>
  node?.type === 'FunctionDeclaration' ||
  node?.type === 'FunctionExpression' ||
  node?.type === 'ArrowFunctionExpression';

function calleeName(callee: ESNode): string | undefined {
  if (callee.type === 'Identifier') return callee.name;
  const method = propName(callee);
  return callee.type === 'MemberExpression' && callee.object.type === 'Identifier' && method
    ? `${callee.object.name}.${method}`
    : undefined;
}

/** The function a handler argument names: inline, wrapped, or a local function or `const` arrow. */
function handlerFn(sourceCode: SourceCode, arg: ESNode): Fn | undefined {
  const node = unwrap(arg);
  if (isFn(node)) return node;
  if (node.type !== 'Identifier') return undefined;
  const defs = findVariable(sourceCode, node)?.defs ?? [];
  const def = defs.length === 1 ? defs[0] : undefined;
  if (def?.type === 'FunctionName') return def.node;
  if (def?.type !== 'Variable' || def.parent.kind !== 'const' || !def.node.init) return undefined;
  const init = unwrap(def.node.init);
  return isFn(init) ? init : undefined;
}

/** True when this read of the error carries it out of `handler` (see the decision notes). */
function leaves(sourceCode: SourceCode, read: Rule.Node, handler: ESNode, traced = false): boolean {
  const [lo, hi] = sourceCode.getRange(handler);
  const outside = (target: ESNode): boolean => {
    let root = target;
    while (root.type === 'MemberExpression') root = root.object;
    if (root.type === 'ThisExpression') return true;
    if (root.type !== 'Identifier') return false;
    const def = findVariable(sourceCode, root)?.defs[0];
    const start = def ? sourceCode.getRange(def.name)[0] : -1;
    return start < lo || start >= hi;
  };
  for (let node = read, parent = node.parent; parent; node = parent, parent = node.parent) {
    if ((parent.type as string) === 'JSXExpressionContainer') return true;
    switch (parent.type) {
      case 'ReturnStatement':
      case 'ThrowStatement':
      case 'YieldExpression':
        return true;
      case 'ArrowFunctionExpression':
        return parent.body === node;
      case 'CallExpression':
      case 'NewExpression':
        if (parent.callee !== node && !CONVERSIONS.has(calleeName(parent.callee) ?? '')) return true;
        break;
      case 'TaggedTemplateExpression':
        return parent.quasi === node;
      case 'MemberExpression':
        if (parent.object !== node) return false;
        break;
      case 'Property':
        if (parent.value !== node || parent.parent.type !== 'ObjectExpression') return false;
        break;
      case 'ConditionalExpression':
        if (parent.test === node) return false;
        break;
      case 'BinaryExpression':
        if (parent.operator !== '+') return false;
        break;
      case 'AssignmentExpression':
        return parent.right === node && outside(parent.left);
      case 'VariableDeclarator': {
        const declaration = parent.parent;
        if (traced || parent.init !== node || parent.id.type !== 'Identifier') return false;
        if (declaration.type !== 'VariableDeclaration' || declaration.kind !== 'const') return false;
        return sourceCode
          .getDeclaredVariables(parent)
          .some((v) =>
            v.references.some(
              (r) => r.isRead() && leaves(sourceCode, r.identifier as Rule.Node, handler, true),
            ),
          );
      }
      default:
        if (!CARRIERS.has(parent.type)) return false;
    }
  }
  return false;
}

const rule: Rule.RuleModule = {
  meta: {
    type: 'problem',
    docs: { description: 'Require every catch clause and promise rejection handler to handle the error' },
    schema: [
      {
        type: 'object',
        properties: { loggers: { type: 'array', items: { type: 'string' }, uniqueItems: true } },
        additionalProperties: false,
      },
    ],
    defaultOptions: [{ loggers: DEFAULT_LOGGERS }],
    messages: { swallowed: 'Errors are handled or propagated, never swallowed (CLAUDE.md)' },
  },
  create(context) {
    const [{ loggers }] = context.options as [{ loggers: string[] }];
    const loggerNames = new Set(loggers);
    const { sourceCode } = context;
    const stack: Frame[] = [];
    const marked = new WeakSet<ESNode>();
    const uses: { fn: Fn; at: ESNode }[] = [];

    const mark = () => {
      for (let i = stack.length - 1; i >= 0; i--) {
        const frame = stack[i];
        if (!frame || frame.handled) return;
        frame.handled = true;
        if (frame.fn) return;
      }
    };
    const passes = (handler: ESNode, bindings: Scope.Variable[], handled: boolean) =>
      handled ||
      bindings.some((v) =>
        v.references.some((r) => r.isRead() && leaves(sourceCode, r.identifier as Rule.Node, handler)),
      );

    return {
      CatchClause(node) {
        stack.push({ node, fn: false, handled: false });
      },
      'CatchClause:exit'(node) {
        const handled = stack.pop()?.handled ?? false;
        if (!passes(node, sourceCode.getDeclaredVariables(node), handled)) {
          context.report({ node, messageId: 'swallowed' });
        }
      },
      ThrowStatement: mark,
      CallExpression(node) {
        const { callee } = node;
        if (callee.type === 'MemberExpression' && METHODS.has(propName(callee) ?? '')) {
          if (loggerNames.has(tailName(callee.object) ?? '')) mark();
        }
        const method = propName(callee);
        const arg =
          method === 'catch' ? node.arguments[0] : method === 'then' ? node.arguments[1] : undefined;
        const fn = arg && handlerFn(sourceCode, arg);
        if (arg && fn) uses.push({ fn, at: arg });
      },
      ':function'(node: Rule.Node) {
        stack.push({ node, fn: true, handled: false });
      },
      ':function:exit'() {
        const frame = stack.pop();
        if (frame?.handled) marked.add(frame.node);
      },
      'Program:exit'() {
        for (const { fn, at } of uses) {
          const first = fn.params[0];
          const [lo, hi] = first ? sourceCode.getRange(first) : [0, 0];
          const inFirst = (name: ESNode) => {
            const [start, end] = sourceCode.getRange(name);
            return start >= lo && end <= hi;
          };
          const bindings = sourceCode
            .getDeclaredVariables(fn)
            .filter((v) => v.defs.some((d) => d.type === 'Parameter' && inFirst(d.name)));
          if (!passes(fn, bindings, marked.has(fn))) context.report({ node: at, messageId: 'swallowed' });
        }
      },
    };
  },
};

export default rule;
