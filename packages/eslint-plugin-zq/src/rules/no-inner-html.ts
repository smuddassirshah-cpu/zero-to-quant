// zq/no-inner-html: the engine has exactly two raw-HTML sinks (docs/PLAN.md 7.2, docs/DECISIONS.md
// S1 and S2), and every other way of turning a string into markup is refused.
// Decision notes:
// - The exemptions are hard-coded, not options: a third sink needs a reviewed change to this file
//   and a DECISIONS.md entry, never a line of configuration. Each exemption names the APIs its sink
//   may use, so Tex.tsx still may not call DOMParser and markup.ts may not set innerHTML.
// - Object-literal keys are checked as well as assignments, which catches `Object.assign(el, {
//   innerHTML })` and props objects; `dangerouslySetInnerHTML` is a key here too, for `h()` calls.
// - Names are matched statically (`el.innerHTML`, `el['innerHTML']`). Computed names built at run
//   time and `Reflect.set` are out of reach of a syntactic rule; review catches them.
import type { Rule } from 'eslint';
import { jsxName, propName, staticString, tailName, type ESNode, type NodeOf } from '../util/ast.ts';
import { repoPath } from '../util/paths.ts';

/** Repository path -> the sink APIs that file may use. Exactly two entries (a test holds this). */
export const SINKS: Readonly<Record<string, readonly string[]>> = {
  'src/engine/render/Tex.tsx': ['innerHTML', 'dangerouslySetInnerHTML'],
  'src/ui/bertie/markup.ts': ['DOMParser', 'parseFromString'],
};

const PROPERTIES = new Set(['innerHTML', 'outerHTML']);
const KEYS = new Set([...PROPERTIES, 'dangerouslySetInnerHTML']);
const METHODS = new Set([
  'insertAdjacentHTML',
  'setHTMLUnsafe',
  'parseHTMLUnsafe',
  'createContextualFragment',
  'parseFromString',
]);
const DOCUMENT_METHODS = new Set(['write', 'writeln']);

function keyName(node: NodeOf<'Property'>): string | undefined {
  const { key } = node;
  return !node.computed && key.type === 'Identifier' ? key.name : staticString(key);
}

const rule: Rule.RuleModule = {
  meta: {
    type: 'problem',
    docs: { description: 'Allow raw-HTML sinks only in the two files docs/DECISIONS.md justifies' },
    schema: [],
    messages: {
      sink: "'{{name}}' turns a string into markup; the only raw-HTML sinks are S1 and S2 (docs/DECISIONS.md 2)",
    },
  },
  create(context) {
    const allowed = new Set(SINKS[repoPath(context)]);
    const report = (node: ESNode, name: string) => {
      if (!allowed.has(name)) context.report({ node, messageId: 'sink', data: { name } });
    };
    return {
      AssignmentExpression(node) {
        const name = propName(node.left);
        if (name && PROPERTIES.has(name)) report(node.left, name);
      },
      CallExpression(node) {
        const name = propName(node.callee);
        if (!name || node.callee.type !== 'MemberExpression') return;
        if (METHODS.has(name)) report(node.callee, name);
        else if (DOCUMENT_METHODS.has(name) && tailName(node.callee.object) === 'document') {
          report(node.callee, `document.${name}`);
        }
      },
      NewExpression(node) {
        if (tailName(node.callee) === 'DOMParser') report(node.callee, 'DOMParser');
      },
      Property(node) {
        const name = keyName(node);
        if (name && KEYS.has(name) && node.parent.type === 'ObjectExpression') report(node.key, name);
      },
      JSXAttribute(node: Rule.Node) {
        if (jsxName(node) === 'dangerouslySetInnerHTML') report(node, 'dangerouslySetInnerHTML');
      },
    };
  },
};

export default rule;
