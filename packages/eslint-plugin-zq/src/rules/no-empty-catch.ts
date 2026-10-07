// zq/no-empty-catch: errors are handled or propagated, never swallowed (CLAUDE.md security floor).
// A handler (a `catch` clause, or an inline function passed to `.catch(fn)` or as the second
// argument of `.then(a, fn)`) passes when it throws, calls a logger, or reads its error binding.
// Decision notes:
// - One pass. A stack holds the open handlers, with a `null` at every function boundary; a `throw`
//   or logger call marks the open handlers down to the nearest boundary, so one inside a nested
//   function counts for that function's handler only. Marking stops at the first handler already
//   marked (everything below it was marked by the same earlier walk), which keeps the pass O(n).
// - Reading the binding is a scope question (`getDeclaredVariables`), so shadowing is exact and a
//   reference inside a nested function counts: a callback that receives the error propagates it.
// - A logger call is `<logger>.<method>(...)` where `<logger>` is an identifier or the last
//   property of a member access (`this.log.warn`), so injected loggers count.
import type { Rule, Scope } from 'eslint';
import { propName, tailName, type ESNode, type NodeOf } from '../util/ast.ts';

interface Handler {
  readonly node: Rule.Node;
  readonly binding: (variable: Scope.Variable) => boolean;
  handled: boolean;
}

const METHODS = new Set(['error', 'warn', 'info', 'log']);
const DEFAULT_LOGGERS = ['log', 'logger', 'console'];

/** The inline handler function of a `.catch(fn)` or `.then(a, fn)` call, if there is one. */
function handlerOf(node: NodeOf<'CallExpression'>) {
  const method = propName(node.callee);
  const fn = method === 'catch' ? node.arguments[0] : method === 'then' ? node.arguments[1] : undefined;
  return fn?.type === 'FunctionExpression' || fn?.type === 'ArrowFunctionExpression' ? fn : undefined;
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
    const stack: (Handler | null)[] = [];
    // Handler function -> whether a variable is its error binding (declared by its first parameter).
    const handlers = new Map<ESNode, (variable: Scope.Variable) => boolean>();

    const mark = () => {
      for (let i = stack.length - 1; i >= 0; i--) {
        const open = stack[i];
        if (!open || open.handled) return;
        open.handled = true;
      }
    };
    const close = () => {
      const open = stack.pop();
      if (!open || open.handled) return;
      const read = sourceCode
        .getDeclaredVariables(open.node)
        .some((v) => open.binding(v) && v.references.some((r) => r.isRead()));
      if (!read) context.report({ node: open.node, messageId: 'swallowed' });
    };

    return {
      CatchClause(node) {
        stack.push({ node, binding: () => true, handled: false });
      },
      'CatchClause:exit': close,
      ThrowStatement: mark,
      CallExpression(node) {
        const { callee } = node;
        if (callee.type === 'MemberExpression' && METHODS.has(propName(callee) ?? '')) {
          if (loggerNames.has(tailName(callee.object) ?? '')) mark();
        }
        const fn = handlerOf(node);
        if (!fn) return;
        const [lo, hi] = fn.params[0] ? sourceCode.getRange(fn.params[0]) : [0, 0];
        const inFirst = (name: ESNode) => {
          const [start, end] = sourceCode.getRange(name);
          return start >= lo && end <= hi;
        };
        handlers.set(fn, (v) => v.defs.some((d) => d.type === 'Parameter' && inFirst(d.name)));
      },
      ':function'(node: Rule.Node) {
        stack.push(null);
        const binding = handlers.get(node);
        if (binding) stack.push({ node, binding, handled: false });
      },
      ':function:exit'(node: Rule.Node) {
        if (handlers.has(node)) close();
        stack.pop();
      },
    };
  },
};

export default rule;
