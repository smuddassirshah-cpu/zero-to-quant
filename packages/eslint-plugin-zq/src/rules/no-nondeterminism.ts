// zq/no-nondeterminism (scope in eslint.config.js, ARCHITECTURE.md 10.4): code whose numbers are shown
// or graded gives the same bits on every engine and every run, so it reads no clock, no unseeded
// randomness and nothing of the host; seeded draws come from @zq/mathcore's Philox (ARCHITECTURE.md
// decision 14).
// Decision notes:
// - Refused on any value use (`new Date(0)`, `Date.UTC`, an alias, `instanceof Date`): `Date`,
//   `Temporal`, `performance`, all of whose members read the clock, and Node's `process`, whose `hrtime`
//   reads the clock and whose `env` differs between runs [our choice: 10.4 names `performance.now`].
//   Refused as members: `Math.random`, `crypto.getRandomValues`, `crypto.randomUUID` and `crypto.subtle`,
//   whose `generateKey` is unseeded (hash32 does the hashing here). Type positions are fine (`d: Date`).
// - Each is found as a global by scope analysis (a local `Date` is fine), as a member or destructured
//   key of a global object, and, with the type checker (`.ts`), on anything typed `Math`, `Crypto`,
//   `SubtleCrypto`, `Performance`, `DateConstructor` or the global object: an alias, a parameter.
// - A global object is `globalThis`, `window`, `self`, `frames`, `top`, `parent`, `opener` or Node's
//   `global`, read as a global or as a static member of a global object (`globalThis.self`, `window.top`),
//   since `.js` has no types to see the second. HTML's Window gives `window`, `self`, `frames`, `top` and
//   `parent` as a WindowProxy, and `opener`'s getter returns one or null [sourced: w3c/webref
//   ed/idl/html.idl at aee967b; whatwg/html source at efc54f7].
// - `Math`, `crypto` and the global objects are usable only through static members or a destructuring
//   with static keys and no rest, so the rule sees every member taken: `Math[k]`, `Reflect.get(Math, k)`,
//   `const M = Math`, `const g = globalThis.self`, `{ Math } = globalThis` and passing one on are refused.
// - Option `transcendental` refuses the Math functions that the NOTE of ECMA-262 21.3.2 leaves
//   implementation-approximated, and `**` on numbers, since Number::exponentiate returns "an
//   implementation-approximated value" [sourced: tc39/ecma262 spec.html at 6db9135]; `dmath` replaces
//   them. The other Math functions are exact (`sqrt` returns the Number of the real root) and pass, and
//   so does `**` with a bigint operand (a literal, a `BigInt()` call, or typed so). The option is set for
//   dmath, @zq/gen and the whole generator module, not only `accept`, `level` and `answer` as
//   CONTENT-FORMAT.md 5.3 words it: `build` must be byte-identical on every device (5.4), `diagnoses` is
//   compared point by point with the Python twin (5.6), and a per-function check would miss the helpers
//   and module constants those functions read [our choice, reported as a deviation].
// - Accepted residue, left to review and the cross-engine tests: a source received from outside the
//   scope and used other than by a member or a call (`Reflect.construct(D, [])` for `D: DateConstructor`),
//   or a received `NodeJS.Process`, not matched by type since a generator's own `Process` type would be;
//   in `.js`, a window reached by a call or the DOM (`open()`, `document.defaultView`); `Intl` and the
//   `toLocale*` methods (locale data differs between engines; 10.4 does not list them); Node's `crypto`
//   and `perf_hooks` modules, which zq/layering keeps out of mathcore and logic.ts only.
import type { Rule, Scope } from 'eslint';
import {
  hasType,
  isGlobal,
  keyName,
  patternSource,
  propName,
  tailName,
  unwrap,
  type ESNode,
  type NodeOf,
} from '../util/ast.ts';

// The globals refused on any value use, with the message each gets.
const REFUSED: ReadonlyMap<string, string> = new Map([
  ['Date', 'clock'],
  ['Temporal', 'clock'],
  ['performance', 'clock'],
  ['process', 'host'],
]);
const RANDOM: ReadonlyMap<string, ReadonlySet<string>> = new Map([
  ['Math', new Set(['random'])],
  ['crypto', new Set(['getRandomValues', 'randomUUID', 'subtle'])],
]);
const KINDS = new Set([...REFUSED.keys(), ...RANDOM.keys()]);
const GLOBAL_OBJECTS = new Set([
  'globalThis',
  'window',
  'self',
  'frames',
  'top',
  'parent',
  'opener',
  'global',
]);
const GUARDED = new Set([...RANDOM.keys(), ...GLOBAL_OBJECTS]);
// The kind of a typed `SubtleCrypto`: refused on any member, since `crypto.subtle` is.
const SUBTLE = 'crypto.subtle';
const TRANSCENDENTAL = new Set(
  [
    'acos acosh asin asinh atan atan2 atanh cbrt cos cosh exp',
    'expm1 hypot log log10 log1p log2 pow sin sinh tan tanh',
  ].flatMap((line) => line.split(' ')),
);
// The type of each watched global, and the global it names; the global object's is `typeof globalThis`.
const TYPES: readonly (readonly [ReadonlySet<string>, string])[] = [
  [new Set(['Math']), 'Math'],
  [new Set(['Crypto']), 'crypto'],
  [new Set(['SubtleCrypto']), SUBTLE],
  [new Set(['Performance']), 'performance'],
  [new Set(['DateConstructor']), 'Date'],
];
const TYPED = new Set(TYPES.flatMap(([types]) => [...types]));
const GLOBAL_TYPES = new Set(['globalThis', 'Window']);
const DATE_TYPES = new Set(['DateConstructor']);
// TypeScript's expression wrappers and an optional chain's end (`self?.Math`): `strip` removes them
// from an owner, `outermost` climbs them from a use.
const WRAPPERS = new Set([
  'TSAsExpression',
  'TSNonNullExpression',
  'TSSatisfiesExpression',
  'TSTypeAssertion',
  'ChainExpression',
]);

/** `node` without its wrappers: util/ast.ts's `unwrap`, and an optional chain's end too. */
function strip(node: ESNode): ESNode {
  let current = unwrap(node);
  while (current.type === 'ChainExpression') current = unwrap(current.expression);
  return current;
}

interface Checker {
  getBigIntType(): unknown;
  getNumberType(): unknown;
  isTypeAssignableTo(source: unknown, target: unknown): boolean;
}

/**
 * True when the type checker sees `node` as a bigint (a literal, a union of them): assignable to
 * `bigint` and not to `number`, so `any` and `never` do not pass. False without type information.
 */
function typedBigInt(sourceCode: Rule.RuleContext['sourceCode'], node: ESNode): boolean {
  const services = sourceCode.parserServices as
    { program?: { getTypeChecker(): Checker }; getTypeAtLocation?: (node: ESNode) => unknown } | undefined;
  if (!services?.program || !services.getTypeAtLocation) return false;
  const checker = services.program.getTypeChecker();
  const type = services.getTypeAtLocation(node);
  return (
    checker.isTypeAssignableTo(type, checker.getBigIntType()) &&
    !checker.isTypeAssignableTo(type, checker.getNumberType())
  );
}

/** `node` with the wrappers around it climbed (`Math as Math` for the `Math`). */
function outermost(node: Rule.Node): Rule.Node {
  let current = node;
  while (current.parent && WRAPPERS.has(current.parent.type)) current = current.parent;
  return current;
}

/**
 * True when a guarded value is used other than as the object of a member access (judged by
 * `member`, dynamic keys included) or as the source of an object pattern (judged per key).
 */
function escapes(node: Rule.Node): boolean {
  const use = outermost(node);
  const { parent } = use;
  if (parent?.type === 'MemberExpression' && parent.object === use) return false;
  if (parent?.type === 'VariableDeclarator' && parent.init === use) return parent.id.type !== 'ObjectPattern';
  if (parent?.type === 'AssignmentExpression' && parent.right === use)
    return parent.left.type !== 'ObjectPattern';
  return true;
}

const rule: Rule.RuleModule = {
  meta: {
    type: 'problem',
    docs: {
      description: 'Refuse clocks, unseeded randomness, the host process and, where set, transcendental Math',
    },
    schema: [
      {
        type: 'object',
        properties: { transcendental: { type: 'boolean' } },
        additionalProperties: false,
      },
    ],
    messages: {
      clock: "'{{name}}' reads the clock, which deterministic code may not (ARCHITECTURE.md 10.4)",
      host: "'{{name}}' reads the host process, whose clock and environment differ between runs (ARCHITECTURE.md 10.4)",
      random:
        "'{{name}}' is not seeded: draw from @zq/mathcore's Philox by (seed, stream, index) (ARCHITECTURE.md 10.4)",
      transcendental:
        "'{{name}}' may differ between engines in the last bit: use @zq/mathcore's dmath (CONTENT-FORMAT.md 5.3)",
      escape:
        "'{{name}}' may be used here only through static members, so that each member taken is checked (ARCHITECTURE.md 10.4)",
    },
  },
  create(context) {
    const { sourceCode } = context;
    const transcendental =
      (context.options[0] as { transcendental?: boolean } | undefined)?.transcendental === true;
    const report = (node: ESNode, messageId: string, name: string) => {
      context.report({ node, messageId, data: { name } });
    };
    // A global object's name read as a global or as a static member of a global object, or, with
    // types, anything typed as one. It recurses only through those names (`globalThis.self.top`).
    const globalObject = (node: ESNode): boolean => {
      const target = strip(node);
      const named =
        target.type === 'Identifier'
          ? GLOBAL_OBJECTS.has(target.name) && isGlobal(sourceCode, target)
          : target.type === 'MemberExpression' &&
            GLOBAL_OBJECTS.has(propName(target) ?? '') &&
            globalObject(target.object);
      return named || hasType(sourceCode, target, GLOBAL_TYPES);
    };
    // The watched global a node names syntactically: `Math`, `globalThis.Math`, `window['Date']`.
    const globalName = (node: ESNode): string | undefined => {
      const target = strip(node);
      const name =
        target.type === 'Identifier'
          ? isGlobal(sourceCode, target) && target.name
          : target.type === 'MemberExpression' && globalObject(target.object) && propName(target);
      return name && KINDS.has(name) ? name : undefined;
    };
    // How a global object is named in a report: as written (`self`, `window.top`'s `top`, an alias `g`),
    // or `globalThis` for a pattern.
    const objectName = (node: ESNode) => tailName(strip(node)) ?? 'globalThis';
    const typedKind = (node: ESNode): string | undefined =>
      hasType(sourceCode, node, TYPED)
        ? TYPES.find(([types]) => hasType(sourceCode, node, types))?.[1]
        : undefined;
    // `crypto.subtle` written out, which is reported where the member is taken.
    const subtleOfCrypto = (node: ESNode) => {
      const target = strip(node);
      return (
        target.type === 'MemberExpression' &&
        propName(target) === 'subtle' &&
        (globalName(target.object) ?? typedKind(target.object)) === 'crypto'
      );
    };
    // `owner.name` (`name` undefined for a dynamic key or a rest), read by a member access or a pattern.
    const member = (node: ESNode, name: string | undefined, owner: ESNode) => {
      if (globalObject(owner)) {
        const refused = name === undefined ? 'escape' : REFUSED.get(name);
        if (refused !== undefined) report(node, refused, name ?? objectName(owner));
        return;
      }
      const named = globalName(owner);
      const kind = named ?? typedKind(owner);
      // A refused global named outright is reported where it is named: by `Program`, or as a global's
      // member; so is `crypto.subtle`.
      if (kind === undefined || (named !== undefined && REFUSED.has(named))) return;
      if (kind === SUBTLE && subtleOfCrypto(owner)) return;
      const refused = kind === SUBTLE ? 'random' : REFUSED.get(kind);
      if (refused !== undefined) report(node, refused, name === undefined ? kind : `${kind}.${name}`);
      else if (name === undefined) report(node, 'escape', kind);
      else if (RANDOM.get(kind)?.has(name)) report(node, 'random', `${kind}.${name}`);
      else if (transcendental && kind === 'Math' && TRANSCENDENTAL.has(name)) {
        report(node, 'transcendental', `Math.${name}`);
      }
    };
    const bigint = (node: ESNode): boolean => {
      const target = strip(node);
      if (target.type === 'Literal' && 'bigint' in target) return true;
      const { callee } = target.type === 'CallExpression' ? target : { callee: undefined };
      if (callee?.type === 'Identifier' && callee.name === 'BigInt' && isGlobal(sourceCode, callee))
        return true;
      return typedBigInt(sourceCode, target);
    };
    const power = (node: ESNode, left: ESNode, right: ESNode, operator: string) => {
      if (transcendental && !bigint(left) && !bigint(right)) report(node, 'transcendental', operator);
    };
    // A `DateConstructor` from elsewhere (a parameter) called or constructed without a member.
    const construct = (node: NodeOf<'CallExpression' | 'NewExpression'>) => {
      if (globalName(node.callee) === undefined && hasType(sourceCode, node.callee, DATE_TYPES)) {
        report(node, 'clock', 'Date');
      }
    };
    // Value references to a global nobody in this file declares; `typeof X` in a type is not one.
    const globalRefs = (name: string): Rule.Node[] => {
      const scope = sourceCode.scopeManager.globalScope;
      const variable = scope?.set.get(name);
      const refs: Scope.Reference[] = [
        ...(variable?.defs.length === 0 ? variable.references : []),
        ...(scope?.through.filter((ref) => ref.identifier.name === name) ?? []),
      ];
      return refs
        .filter((ref) => (ref as { isValueReference?: boolean }).isValueReference !== false)
        .map((ref) => ref.identifier as Rule.Node)
        .filter((id) => {
          const parent = id.parent?.type as string | undefined;
          return parent !== 'TSTypeQuery' && parent !== 'TSQualifiedName';
        });
    };

    return {
      Program() {
        for (const [name, refused] of REFUSED) for (const id of globalRefs(name)) report(id, refused, name);
        for (const name of GUARDED)
          for (const id of globalRefs(name)) if (escapes(id)) report(id, 'escape', name);
      },
      MemberExpression(node) {
        const name = propName(node);
        member(node, name, node.object);
        // `globalThis.Math` or `window.self` itself, taken as a value.
        if (name !== undefined && GUARDED.has(name) && globalObject(node.object) && escapes(node)) {
          report(node, 'escape', name);
        }
      },
      Property(node) {
        if (node.parent.type !== 'ObjectPattern') return;
        const owner = patternSource(node.parent) ?? node.parent;
        const name = keyName(node);
        if (name !== undefined && GUARDED.has(name) && globalObject(owner)) report(node, 'escape', name);
        else member(node, name, owner);
      },
      // A rest takes every key not named, so it is judged as a dynamic key.
      RestElement(node) {
        if (node.parent.type === 'ObjectPattern')
          member(node, undefined, patternSource(node.parent) ?? node.parent);
      },
      BinaryExpression(node) {
        if (node.operator === '**') power(node, node.left, node.right, '**');
      },
      AssignmentExpression(node) {
        if (node.operator === '**=') power(node, node.left, node.right, '**=');
      },
      CallExpression: construct,
      NewExpression: construct,
    };
  },
};

export default rule;
