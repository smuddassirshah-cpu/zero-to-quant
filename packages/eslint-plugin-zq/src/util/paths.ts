// Repository-relative paths for scoped rules. The root is fixed by this file's own location
// (packages/eslint-plugin-zq/src/util/), not by the linting process's working directory, so a
// path-scoped check holds whichever directory ESLint is started from.
import path from 'node:path';
import type { Rule } from 'eslint';

export const REPO_ROOT = path.resolve(import.meta.dirname, '../../../..');

/** The linted file's path relative to the repository root, with forward slashes. */
export function repoPath(context: Rule.RuleContext): string {
  const file = path.resolve(context.cwd, context.physicalFilename);
  return path.relative(REPO_ROOT, file).split(path.sep).join('/');
}
