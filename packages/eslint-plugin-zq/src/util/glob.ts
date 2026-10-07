// The glob subset of zq/layering, compiled to anchored regular expressions:
//   `**`    any number of path segments, none included (`a/**` matches `a` itself);
//   `*`     one segment or part of one, captured (the first capture is the importer's `$1`);
//   `$1`    the first `*` capture of the importer's matched `files` glob;
//   `$dir`  the importer's own directory.
// Tokens are substituted as escaped literals, so a captured `.` cannot widen a pattern. Written
// here rather than taken from a glob library: four constructs do not justify a dependency.

export interface Tokens {
  readonly cap?: string | undefined;
  readonly dir?: string | undefined;
}

const PARTS = /(\*\*\/|\/\*\*$|\*\*|\*|\$1|\$dir)/;
const cache = new Map<string, RegExp>();

const escape = (text: string) => text.replace(/[.+?^${}()|[\]\\]/g, '\\$&');

function piece(part: string, tokens: Tokens): string {
  switch (part) {
    case '**/':
      return '(?:.*/)?';
    case '/**':
      return '(?:/.*)?';
    case '**':
      return '.*';
    case '*':
      return '([^/]*)';
    case '$1':
      return escape(tokens.cap ?? '');
    case '$dir':
      return escape(tokens.dir ?? '');
    default:
      return escape(part);
  }
}

/** Compiles `pattern`; patterns without tokens are cached for the life of the process. */
export function glob(pattern: string, tokens: Tokens = {}): RegExp {
  const fixed = !pattern.includes('$');
  const hit = fixed ? cache.get(pattern) : undefined;
  if (hit) return hit;
  const regex = new RegExp(
    `^${pattern
      .split(PARTS)
      .map((part) => piece(part, tokens))
      .join('')}$`,
  );
  if (fixed) cache.set(pattern, regex);
  return regex;
}
