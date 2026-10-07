// zq/no-inner-html: the engine has exactly two raw-HTML sinks (docs/PLAN.md 7.2, docs/DECISIONS.md
// S1 and S2), and every other way of turning a string into markup is refused.
// Decision notes:
// - The exemptions are hard-coded, not options: a third sink needs a reviewed change to this file
//   and a DECISIONS.md entry, never a line of configuration. Each exemption names the APIs its sink
//   may use, so Tex.tsx still may not call DOMParser and markup.ts may not set innerHTML; and S2
//   parses SVG only, so its `parseFromString` must take the literal `'image/svg+xml'`.
// - `innerHTML` and `outerHTML` are refused in every write position (assignment, compound
//   assignment, destructuring target, `for ... of` left side) and as object-literal keys, which
//   catches `Object.assign(el, { innerHTML })`, props objects and `Object.defineProperties`; also
//   as the key argument of `Reflect.set`, `Reflect.defineProperty` and `Object.defineProperty`.
// - A sink method is refused on any access, called or not, so `.call`, `.apply`, `.bind` and
//   destructuring are covered. `write` and `writeln` count on a document: `document` itself, or
//   any expression the type checker types as `Document` (`el.ownerDocument`, an alias).
// - Names are matched statically, `+` of literals folded (`el['inner' + 'HTML']`). Accepted
//   residue, out of reach of a static rule and left to review: names built at run time, a key
//   template with expressions (`` el[`inner${'HTML'}`] ``), and the setter reached through
//   `Object.getOwnPropertyDescriptor(Element.prototype, 'innerHTML').set.call(el, s)`.
import type { Rule } from 'eslint';
import {
  hasType,
  jsxName,
  keyName,
  patternSource,
  propName,
  staticString,
  tailName,
  type ESNode,
} from '../util/ast.ts';
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
const DOCUMENT_TYPES = new Set(['Document']);
const KEY_SETTERS = new Set(['Reflect.set', 'Reflect.defineProperty', 'Object.defineProperty']);

/** True when `node` is written to, not read. */
function isWriteTarget(node: Rule.Node): boolean {
  const { parent } = node;
  switch (parent?.type) {
    case 'AssignmentExpression':
    case 'AssignmentPattern':
    case 'ForOfStatement':
    case 'ForInStatement':
      return parent.left === node;
    case 'ArrayPattern':
    case 'RestElement':
    case 'UpdateExpression':
      return true;
    case 'Property':
      return parent.value === node && parent.parent.type === 'ObjectPattern';
    default:
      return false;
  }
}

/** True for `parser.parseFromString(text, 'image/svg+xml')`, the only call sink S2 makes. */
function parsesSvg(member: Rule.Node): boolean {
  const call = member.parent;
  return (
    call?.type === 'CallExpression' &&
    call.callee === member &&
    staticString(call.arguments[1]) === 'image/svg+xml'
  );
}

const rule: Rule.RuleModule = {
  meta: {
    type: 'problem',
    docs: { description: 'Allow raw-HTML sinks only in the two files docs/DECISIONS.md justifies' },
    schema: [],
    messages: {
      sink: "'{{name}}' turns a string into markup; the only raw-HTML sinks are S1 and S2 (docs/DECISIONS.md 2)",
      svgOnly: "Sink S2 parses SVG only: call parseFromString with 'image/svg+xml' (docs/DECISIONS.md S2)",
    },
  },
  create(context) {
    const { sourceCode } = context;
    const allowed = new Set(SINKS[repoPath(context)]);
    const report = (node: ESNode, name: string) => {
      if (!allowed.has(name)) context.report({ node, messageId: 'sink', data: { name } });
    };
    const isDocument = (node: ESNode) =>
      tailName(node) === 'document' || hasType(sourceCode, node, DOCUMENT_TYPES);
    const method = (node: ESNode, name: string, owner: ESNode | undefined) => {
      if (METHODS.has(name)) report(node, name);
      else if (DOCUMENT_METHODS.has(name) && owner && isDocument(owner)) report(node, `document.${name}`);
    };

    return {
      MemberExpression(node) {
        const name = propName(node);
        if (name === undefined) return;
        if (PROPERTIES.has(name) && isWriteTarget(node)) report(node, name);
        else if (name === 'parseFromString' && allowed.has(name) && !parsesSvg(node)) {
          context.report({ node, messageId: 'svgOnly' });
        } else method(node, name, node.object);
      },
      CallExpression(node) {
        const [, key] = node.arguments;
        const callee = node.callee.type === 'MemberExpression' ? node.callee : undefined;
        const setter = callee && `${tailName(callee.object) ?? ''}.${propName(callee) ?? ''}`;
        const name = setter && KEY_SETTERS.has(setter) ? staticString(key) : undefined;
        if (key && name && KEYS.has(name)) report(key, name);
      },
      NewExpression(node) {
        if (tailName(node.callee) === 'DOMParser') report(node.callee, 'DOMParser');
      },
      Property(node) {
        const name = keyName(node);
        if (name === undefined) return;
        if (node.parent.type === 'ObjectExpression') {
          if (KEYS.has(name)) report(node.key, name);
        } else if (name === 'parseFromString' && allowed.has(name)) {
          context.report({ node: node.key, messageId: 'svgOnly' });
        } else {
          method(node.key, name, patternSource(node.parent));
        }
      },
      JSXAttribute(node: Rule.Node) {
        if (jsxName(node) === 'dangerouslySetInnerHTML') report(node, 'dangerouslySetInnerHTML');
      },
    };
  },
};

export default rule;
