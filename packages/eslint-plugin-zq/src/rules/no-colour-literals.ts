// zq/no-colour-literals (scope `src/**/*.{ts,tsx}`): colours come from the design tokens, never
// from a literal in code (stylelint holds the same line in CSS).
// Decision notes:
// - A hex colour is `#` and 3, 4, 6 or 8 hex digits, at the start of the string or after
//   whitespace, `:`, `(` or `,`, and not followed by a word character or `-`; so `'#/system'` and
//   `'#app'` pass while `'#abc'` and `'border: 1px solid #FFF'` fail. A hash route spelt only in
//   hex digits (`'#add'`) reads as a colour; the app's routes start `#/`, so none does. So does
//   an issue number of three, four, six or eight digits (`'Issue #123'`): name it `issue 123`.
// - Colour functions match on a word boundary, case-insensitively, `color-mix(` before `color(`;
//   the message quotes the call up to its first `)`.
// - Named colours are not matched: they read as English in copy, and stylelint bans them in CSS.
// - Template literals are checked quasi by quasi, so `` `rgb(${r}, 0, 0)` `` fails on `rgb(`.
// - Module specifiers are not checked (`import '#abc'`): they name modules, not colours.
import type { Rule } from 'eslint';
import type { ESNode } from '../util/ast.ts';

const COLOUR =
  /(?:^|[\s:(,])(#(?:[0-9a-f]{8}|[0-9a-f]{6}|[0-9a-f]{3,4})(?![\w-]))|\b((?:rgba?|hsla?|hwb|oklab|oklch|lab|lch|color-mix|color)\([^)]*\)?)/i;
const SPECIFIER_PARENTS = new Set([
  'ImportDeclaration',
  'ExportNamedDeclaration',
  'ExportAllDeclaration',
  'ImportExpression',
  'TSImportType',
  'TSExternalModuleReference',
  'TSModuleDeclaration',
]);

const rule: Rule.RuleModule = {
  meta: {
    type: 'problem',
    docs: { description: 'Refuse hex and colour-function literals; colours come from the design tokens' },
    schema: [],
    messages: { colour: "'{{colour}}' is a colour literal; colours come from the design tokens" },
  },
  create(context) {
    const check = (node: ESNode, text: string | null | undefined) => {
      const match = text ? COLOUR.exec(text) : null;
      const colour = match?.[1] ?? match?.[2];
      if (colour) context.report({ node, messageId: 'colour', data: { colour } });
    };
    return {
      Literal(node) {
        if (typeof node.value === 'string' && !SPECIFIER_PARENTS.has(node.parent.type))
          check(node, node.value);
      },
      TemplateElement(node) {
        check(node, node.value.cooked ?? node.value.raw);
      },
    };
  },
};

export default rule;
