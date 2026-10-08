import { expect, it } from 'vitest';
import rule, { SINKS } from '../src/rules/no-inner-html.ts';
import { at, tester, TYPED, typed } from './tester.ts';

const TEX = at('src/engine/render/Tex.tsx');
const MARKUP = at('src/ui/bertie/markup.ts');
const sink = (name: string) => [{ messageId: 'sink', data: { name } }];
const fails = (code: string, name: string, filename?: string) => ({
  code,
  errors: sink(name),
  ...(filename ? { filename } : {}),
});
const svgOnly = (code: string) => ({ code, filename: MARKUP, errors: [{ messageId: 'svgOnly' }] });

it('exempts exactly the two sinks of docs/DECISIONS.md 2', () => {
  expect(SINKS).toEqual({
    'src/engine/render/Tex.tsx': ['innerHTML', 'dangerouslySetInnerHTML'],
    'src/ui/bertie/markup.ts': ['DOMParser', 'parseFromString'],
  });
});

tester.run('no-inner-html', rule, {
  valid: [
    'el.textContent = s',
    'const html = el.innerHTML',
    'const { innerHTML } = el',
    'el.insertAdjacentText("beforeend", s)',
    'stream.write(s)',
    'const { write } = stream',
    'el[name] = s',
    'Reflect.set(el, "textContent", s)',
    'Object.defineProperty(el, name, { value: s })',
    { code: 'el.innerHTML = s', filename: TEX },
    { code: '<div dangerouslySetInnerHTML={{ __html: s }} />', filename: TEX },
    { code: 'new DOMParser().parseFromString(s, "image/svg+xml")', filename: MARKUP },
  ],
  invalid: [
    fails('el.innerHTML = s', 'innerHTML'),
    fails('new (window?.DOMParser)()', 'DOMParser'),
    fails('const { write } = window?.document', 'document.write'),
    fails('({ writeln: w } = (self.document as Document))', 'document.writeln'),
    fails('el.outerHTML = s', 'outerHTML'),
    fails('el["innerHTML"] += s', 'innerHTML'),
    fails('el[`outerHTML`] = s', 'outerHTML'),
    fails('el["inner" + "HTML"] = s', 'innerHTML'),
    fails('[el.innerHTML] = [s]', 'innerHTML'),
    fails('({ html: el.outerHTML } = props)', 'outerHTML'),
    fails('[el.innerHTML = s] = []', 'innerHTML'),
    fails('for (el.innerHTML of parts) {}', 'innerHTML'),
    fails('el.insertAdjacentHTML("beforeend", s)', 'insertAdjacentHTML'),
    fails('el.insertAdjacentHTML.call(el, "beforeend", s)', 'insertAdjacentHTML'),
    fails('const make = range.createContextualFragment.bind(range)', 'createContextualFragment'),
    fails('const { insertAdjacentHTML } = el', 'insertAdjacentHTML'),
    fails('const { write } = document', 'document.write'),
    fails('document.write(s)', 'document.write'),
    fails('window.document.writeln(s)', 'document.writeln'),
    fails('el.setHTMLUnsafe(s)', 'setHTMLUnsafe'),
    fails('Document.parseHTMLUnsafe(s)', 'parseHTMLUnsafe'),
    fails('parser.parseFromString(s, "text/html")', 'parseFromString'),
    fails('new window.DOMParser()', 'DOMParser'),
    fails('<div dangerouslySetInnerHTML={{ __html: s }} />', 'dangerouslySetInnerHTML'),
    fails('Object.assign(el, { innerHTML: s })', 'innerHTML'),
    fails('const props = { "outerHTML": s }', 'outerHTML'),
    fails('const props = { ["innerHTML"]: s }', 'innerHTML'),
    fails('h("div", { dangerouslySetInnerHTML: { __html: s } })', 'dangerouslySetInnerHTML'),
    fails('Reflect.set(el, "innerHTML", s)', 'innerHTML'),
    fails('Reflect.defineProperty(el, "outerHTML", { value: s })', 'outerHTML'),
    fails('Object.defineProperty(el, "innerHTML", { value: s })', 'innerHTML'),
    fails('Object.defineProperties(el, { innerHTML: { value: s } })', 'innerHTML'),
    fails('el.outerHTML = s', 'outerHTML', TEX),
    fails('new DOMParser()', 'DOMParser', TEX),
    fails('el.innerHTML = s', 'innerHTML', MARKUP),
    fails('el.innerHTML = s', 'innerHTML', at('src/engine/render/Other.tsx')),
    svgOnly('parser.parseFromString(s, "text/html")'),
    svgOnly('parser.parseFromString(s, type)'),
    svgOnly('const parse = parser.parseFromString'),
    svgOnly('const { parseFromString } = parser'),
  ],
});

typed.run('no-inner-html (typed)', rule, {
  valid: [{ code: 'declare const out: { write(s: string): void }; out.write("x");', filename: TYPED }],
  invalid: [
    { code: 'const d = document; d.write("x");', filename: TYPED, errors: sink('document.write') },
    {
      code: 'declare const el: HTMLElement; el.ownerDocument.writeln("x");',
      filename: TYPED,
      errors: sink('document.writeln'),
    },
    {
      code: 'declare const frame: HTMLIFrameElement; const { write } = frame.contentDocument!;',
      filename: TYPED,
      errors: sink('document.write'),
    },
  ],
});
