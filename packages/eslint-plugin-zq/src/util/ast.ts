// AST and type helpers shared by the rules. ESTree types come from eslint's own signatures, and
// the TypeScript checker is reached through typescript-eslint's parser services, typed here
// structurally, so the plugin needs no dependency beyond its eslint peer.
import type { Rule, Scope, SourceCode } from 'eslint';

export type ESNode = Parameters<SourceCode['getAncestors']>[0];
export type NodeOf<T extends ESNode['type']> = Extract<ESNode, { type: T }>;

/** The value of a string literal, a template literal without expressions, or a `+` of those. */
export function staticString(node: ESNode | null | undefined): string | undefined {
  if (node?.type === 'Literal') return typeof node.value === 'string' ? node.value : undefined;
  if (node?.type === 'TemplateLiteral' && node.expressions.length === 0) {
    return node.quasis[0]?.value.cooked ?? undefined;
  }
  if (node?.type === 'BinaryExpression' && node.operator === '+') {
    const left = staticString(node.left);
    const right = staticString(node.right);
    return left === undefined || right === undefined ? undefined : left + right;
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

/** The static key of an object literal or pattern property. */
export function keyName(node: NodeOf<'Property'>): string | undefined {
  return !node.computed && node.key.type === 'Identifier' ? node.key.name : staticString(node.key);
}

const WRAPPERS = new Set([
  'TSAsExpression',
  'TSNonNullExpression',
  'TSSatisfiesExpression',
  'TSTypeAssertion',
]);

/** `node` without TypeScript's expression wrappers (`as`, `!`, `satisfies`, `<T>`). */
export function unwrap(node: ESNode): ESNode {
  let current = node;
  while (WRAPPERS.has(current.type)) current = (current as unknown as { expression: ESNode }).expression;
  return current;
}

/** The variable an identifier resolves to in this file, if it is declared or a known global. */
export function findVariable(sourceCode: SourceCode, node: NodeOf<'Identifier'>): Scope.Variable | undefined {
  for (let scope: Scope.Scope | null = sourceCode.getScope(node); scope; scope = scope.upper) {
    const variable = scope.set.get(node.name);
    if (variable) return variable;
  }
  return undefined;
}

/** True when `node` names a variable nobody declared in this file: a global of the platform. */
export function isGlobal(sourceCode: SourceCode, node: ESNode): boolean {
  return node.type === 'Identifier' && !findVariable(sourceCode, node)?.defs.length;
}

/** The expression an object pattern destructures, when it is written beside the pattern. */
export function patternSource(pattern: Rule.Node): ESNode | undefined {
  const { parent } = pattern;
  if (parent?.type === 'VariableDeclarator' && parent.id === pattern) return parent.init ?? undefined;
  if (parent?.type === 'AssignmentExpression' && parent.left === pattern) return parent.right;
  return undefined;
}

interface JsxName {
  readonly type: string;
  readonly name?: unknown;
}

/** The plain name of a JSX element or attribute, without a namespace; JSX is outside ESTree. */
export function jsxName(node: Rule.Node): string | undefined {
  let { name } = node as unknown as { name?: JsxName };
  if (name?.type === 'JSXNamespacedName') name = name.name as JsxName;
  return name?.type === 'JSXIdentifier' && typeof name.name === 'string' ? name.name : undefined;
}

interface TsType {
  getSymbol(): { getName(): string } | undefined;
  isUnionOrIntersection(): boolean;
  readonly types?: readonly TsType[];
  getBaseTypes(): readonly TsType[] | undefined;
}

interface TypeServices {
  readonly program: unknown;
  getTypeAtLocation(node: ESNode): TsType;
}

/**
 * True when the type checker sees `node` as one of `names`, or as a union, intersection or subtype
 * of one (`Window & typeof globalThis`, `Document | null`, `HTMLDocument`). Always false without
 * type information, as in `.js` files, so the callers keep their syntactic checks as well.
 */
export function hasType(sourceCode: SourceCode, node: ESNode, names: ReadonlySet<string>): boolean {
  const services = sourceCode.parserServices as Partial<TypeServices> | undefined;
  if (!services?.program || !services.getTypeAtLocation) return false;
  const seen = new Set<TsType>();
  const visit = (type: TsType): boolean => {
    if (seen.has(type)) return false;
    seen.add(type);
    const name = type.getSymbol()?.getName();
    if (name !== undefined && names.has(name)) return true;
    return ((type.isUnionOrIntersection() ? type.types : type.getBaseTypes()) ?? []).some(visit);
  };
  return visit(services.getTypeAtLocation(node));
}
