// Child processes for the CI tools: argument arrays only, never a shell string (CLAUDE.md security floor).
import { spawn } from 'node:child_process';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

export const repoRoot = resolve(dirname(fileURLToPath(import.meta.url)), '..', '..');

interface RunOptions {
  readonly cwd?: string;
  readonly env?: NodeJS.ProcessEnv;
  /** Collect stdout and stderr instead of passing them through to the terminal. */
  readonly capture?: boolean;
  /** Written to the child's stdin, which is otherwise closed (capture) or inherited. */
  readonly input?: string | undefined;
}

interface RunResult {
  /** Exit status: 127 when the command is not installed, 1 when a signal ended it. */
  readonly code: number;
  readonly stdout: string;
  readonly stderr: string;
  readonly missing: boolean;
}

export type Log = (line: string) => void;

export type Run = (cmd: string, args: readonly string[], options?: RunOptions) => Promise<RunResult>;

export const run: Run = (cmd, args, options = {}) =>
  new Promise((done, fail) => {
    const stdin = options.input !== undefined ? 'pipe' : options.capture === true ? 'ignore' : 'inherit';
    const child = spawn(cmd, args, {
      cwd: options.cwd ?? repoRoot,
      env: options.env ?? process.env,
      stdio: options.capture === true ? [stdin, 'pipe', 'pipe'] : [stdin, 'inherit', 'inherit'],
    });
    const out: string[] = [];
    const err: string[] = [];
    child.stdout?.setEncoding('utf8').on('data', (chunk: string) => out.push(chunk));
    child.stderr?.setEncoding('utf8').on('data', (chunk: string) => err.push(chunk));
    // A child that exits before reading its input breaks the pipe; its exit status reports why.
    child.stdin?.on('error', (error: NodeJS.ErrnoException) => {
      if (error.code !== 'EPIPE') fail(error);
    });
    child.stdin?.end(options.input);
    child.on('error', (error: NodeJS.ErrnoException) => {
      if (error.code === 'ENOENT') done({ code: 127, stdout: '', stderr: '', missing: true });
      else fail(error);
    });
    child.on('close', (code) => {
      done({ code: code ?? 1, stdout: out.join(''), stderr: err.join(''), missing: false });
    });
  });
