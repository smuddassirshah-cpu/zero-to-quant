// AST helpers shared by the rules. ESTree types come from eslint's own signatures, so the plugin
// needs no dependency beyond its eslint peer.
import type { Rule, Scope, SourceCode } from 'eslint';

export type ESNode = Parameters<SourceCode['getAncestors']>[0];
export type NodeOf<T extends ESNode['type']> = Extract<ESNode, { type: T }>;

/** The value of a string literal or of a template literal without expressions. */
export function staticString(node: ESNode | null | undefined): string | undefined {
  if (node?.type === 'Literal') return typeof node.value === 'string' ? node.value : undefined;
  if (node?.type === 'TemplateLiteral' && node.expressions.length === 0) {
    return node.quasis[0]?.value.cooked ?? undefined;
  }
  return undefined;
}

/** The static name of a member access: `a.b`, `a['b']` and `` a[`b`] `` all give `b`. */
export function propName(node: ESNode): string | undefined {
  if (node.type !== 'MemberExpression') return undefined;
  if (node.computed) return staticString(node.property);
  return node.property.type === 'Identifier' ? node.property.name : undefined;
}

/** The name of an identifier, or of the last property of a member access. */
export function tailName(node: ESNode): string | undefined {
  return node.type === 'Identifier' ? node.name : propName(node);
}

/** True when `node` names a variable nobody declared in this file: a global of the platform. */
export function isGlobal(sourceCode: SourceCode, node: ESNode): boolean {
  if (node.type !== 'Identifier') return false;
  for (let scope: Scope.Scope | null = sourceCode.getScope(node); scope; scope = scope.upper) {
    const variable = scope.set.get(node.name);
    if (variable) return variable.defs.length === 0;
  }
  return true;
}

/** The plain name of a JSX element or attribute; JSX nodes are outside ESTree's types. */
export function jsxName(node: Rule.Node): string | undefined {
  const { name } = node as unknown as { name?: { type: string; name?: unknown } };
  return name?.type === 'JSXIdentifier' && typeof name.name === 'string' ? name.name : undefined;
}
