import { expect, it } from 'vitest';
import rule, { SINKS } from '../src/rules/no-inner-html.ts';
import { at, tester } from './tester.ts';

const TEX = at('src/engine/render/Tex.tsx');
const MARKUP = at('src/ui/bertie/markup.ts');
const sink = (name: string) => [{ messageId: 'sink', data: { name } }];

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
    'el[name] = s',
    { code: 'el.innerHTML = s', filename: TEX },
    { code: '<div dangerouslySetInnerHTML={{ __html: s }} />', filename: TEX },
    { code: 'new DOMParser().parseFromString(s, "image/svg+xml")', filename: MARKUP },
  ],
  invalid: [
    { code: 'el.innerHTML = s', errors: sink('innerHTML') },
    { code: 'el.outerHTML = s', errors: sink('outerHTML') },
    { code: 'el["innerHTML"] += s', errors: sink('innerHTML') },
    { code: 'el[`outerHTML`] = s', errors: sink('outerHTML') },
    { code: 'el.insertAdjacentHTML("beforeend", s)', errors: sink('insertAdjacentHTML') },
    { code: 'document.write(s)', errors: sink('document.write') },
    { code: 'window.document.writeln(s)', errors: sink('document.writeln') },
    { code: 'el.setHTMLUnsafe(s)', errors: sink('setHTMLUnsafe') },
    { code: 'Document.parseHTMLUnsafe(s)', errors: sink('parseHTMLUnsafe') },
    { code: 'range.createContextualFragment(s)', errors: sink('createContextualFragment') },
    { code: 'parser.parseFromString(s, "text/html")', errors: sink('parseFromString') },
    { code: 'new window.DOMParser()', errors: sink('DOMParser') },
    { code: '<div dangerouslySetInnerHTML={{ __html: s }} />', errors: sink('dangerouslySetInnerHTML') },
    { code: 'Object.assign(el, { innerHTML: s })', errors: sink('innerHTML') },
    { code: 'const props = { "outerHTML": s }', errors: sink('outerHTML') },
    { code: 'const props = { ["innerHTML"]: s }', errors: sink('innerHTML') },
    { code: 'h("div", { dangerouslySetInnerHTML: { __html: s } })', errors: sink('dangerouslySetInnerHTML') },
    { code: 'el.outerHTML = s', filename: TEX, errors: sink('outerHTML') },
    { code: 'new DOMParser()', filename: TEX, errors: sink('DOMParser') },
    { code: 'el.innerHTML = s', filename: MARKUP, errors: sink('innerHTML') },
    { code: 'el.innerHTML = s', filename: at('src/engine/render/Other.tsx'), errors: sink('innerHTML') },
  ],
});
