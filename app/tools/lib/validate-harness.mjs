/* Shared scratch-case harness for the test-validate-*.mjs files (engine pass AC part 2).

   Why: each test used to copy all of app/ (83 MB of content), plant one fault and run the validator over the whole curriculum, once per
   case (14 s a run, about ten minutes a file). The harness copies only tools/fixtures/mini-app instead (about 0.9 MB: four small courses,
   a few lessons, reviews, homework, a Fluency set, a problem set, exams, a drill pack, a bank file, prep.json and the index files the
   validator insists on) and runs validate.mjs on that copy with --root, so a run takes about 0.4 s. Nothing under app/content is read or written.

   Layout of a scratch copy (the same shape as app/, which is what --root expects):
     <tmp>/content/...                  a fresh copy of tools/fixtures/mini-app/content
     <tmp>/tools/fixtures/<name>/...    only the real fixture folders a case asks for (fixtures: ['problems', 'fluency']); none by default
   The mini root validates with 0 errors. Its warnings (51 at the last count) are copied from the real lessons it holds: not-yet-written
   lines for the courses cut down to a few files, O2 voice notes, key-length and so on. A case therefore asserts on the tag or the message of
   its own planted fault, never on "no warnings at all". tools/test-validate-harness.mjs guards the mini root itself.

   API
     const h = openHarness({ name: 'band', fixtures: [] });
     h.dir                      the scratch folder (the old tests called it "copy"); h.dir/content/courses/... are the planted files
     h.path('content/exams/topic-0.7.json')   an absolute path inside the scratch folder
     h.validate(args = ['--no-manifest'])      runs the validator on the scratch root: { out, code, errors, warnings, all }
                                               errors and warnings are the report lines (those beginning "error" or "warning")
                                               pass other flags in args (['--lax-why'], ['--local-cdn', dir]); with no '--no-manifest'
                                               the validator writes <tmp>/content/manifest.json, which a case can read back (h.path)
     h.reset()                  restores the whole scratch folder to the pristine mini root
     h.close()                  removes the scratch folder
   ZQ_VALIDATE=<file> runs another validator script (a mutated copy kept inside tools/, for the mutation spot check in docs/reports/engine-pass-ac-2.md).
   The validator is spawned (not imported) so a case's result is exactly what node tools/validate.mjs prints; the output text is identical
   to a run on the real root apart from the file paths, which read content/... either way. */
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { execFileSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

export const TOOLS = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
export const APP = path.resolve(TOOLS, '..');
export const MINI = path.join(TOOLS, 'fixtures', 'mini-app');

export function openHarness({ name = 'case', fixtures = [] } = {}) {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), `zq-${name}-`));
  const populate = () => {
    fs.rmSync(path.join(dir, 'content'), { recursive: true, force: true });
    fs.rmSync(path.join(dir, 'tools'), { recursive: true, force: true });
    fs.cpSync(path.join(MINI, 'content'), path.join(dir, 'content'), { recursive: true });
    for (const f of fixtures) fs.cpSync(path.join(TOOLS, 'fixtures', f), path.join(dir, 'tools', 'fixtures', f), { recursive: true });
  };
  populate();
  const validate = (args = ['--no-manifest']) => {
    let out, code = 0;
    try { out = execFileSync('node', [process.env.ZQ_VALIDATE || path.join(TOOLS, 'validate.mjs'), '--root', path.join(dir, 'content'), ...args], { cwd: dir, encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe'], maxBuffer: 1 << 28 }); }
    catch (e) { out = String(e.stdout || '') + String(e.stderr || ''); code = e.status || 1; }
    const all = out.split('\n');
    return { out, code, all, errors: all.filter((l) => /^error/.test(l)), warnings: all.filter((l) => /^warning/.test(l)) };
  };
  return {
    dir, validate,
    path: (rel) => path.join(dir, rel),
    reset: populate,
    close: () => fs.rmSync(dir, { recursive: true, force: true }),
  };
}
