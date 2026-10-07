import rule from '../src/rules/no-forbidden-apis.ts';
import { at, tester, TYPED, typed } from './tester.ts';

const APP = at('src/app/a.ts');
const forbidden = (name: string) => [{ messageId: 'forbidden', data: { name } }];
const serviceWorker = [{ messageId: 'serviceWorker' }];
const fails = (code: string, name: string) => ({ code, errors: forbidden(name) });

tester.run('no-forbidden-apis', rule, {
  valid: [
    'import { open } from "./files.ts"; open("x")',
    'function f(print: () => void) { print() }',
    'const window = { open() {} }; window.open()',
    'printer.print()',
    'el.open',
    'const { open } = dialogState',
    'function f({ open }) { return open }',
    'let f: Function',
    'type F = typeof Function',
    'const o = { Function: 1 }',
    'x.Function',
    'document.createElement("div")',
    'document.createElement(tag)',
    'h(Component, {})',
    '<div />',
    'const navigator = { serviceWorker: 1 }; navigator.serviceWorker',
    { code: 'navigator.serviceWorker.register("/sw.js")', filename: at('src/platform/web/sw-client.ts') },
    { code: 'self.navigator.serviceWorker', filename: at('src/sw/sw.ts') },
  ],
  invalid: [
    fails('window.open("x")', 'window.open'),
    fails('self.open("x")', 'self.open'),
    fails('globalThis.open("x")', 'globalThis.open'),
    fails('open("x")', 'open'),
    fails('print()', 'print'),
    fails('window.print()', 'window.print'),
    fails('const o = window["open"]', 'window.open'),
    fails('const { open } = window', 'window.open'),
    fails('({ print } = self)', 'self.print'),
    fails('document.createElement("IFRAME")', 'iframe'),
    fails('document.createElement(`iframe`)', 'iframe'),
    fails('document.createElement("html:iframe")', 'iframe'),
    fails('doc.createElementNS(ns, "iframe")', 'iframe'),
    fails('createElement("iframe")', 'iframe'),
    fails('h("iframe", { src })', 'iframe'),
    fails('jsx("embed", {})', 'embed'),
    fails('document.createElement("object")', 'object'),
    fails('<iframe src="x" />', 'iframe'),
    fails('<embed src="x" />', 'embed'),
    fails('<object data="x" />', 'object'),
    fails('<svg:iframe />', 'iframe'),
    { code: 'navigator.serviceWorker.register("/sw.js")', filename: APP, errors: serviceWorker },
    { code: 'window.navigator.serviceWorker', filename: APP, errors: serviceWorker },
    { code: 'const { serviceWorker } = navigator', filename: APP, errors: serviceWorker },
    fails('eval("1")', 'eval'),
    fails('window.eval("1")', 'window.eval'),
    fails('globalThis.eval("1")', 'globalThis.eval'),
    fails('new Function("return 1")', 'new Function'),
    fails('Function("return 1")', 'Function'),
    fails('window.Function("return 1")', 'window.Function'),
    fails('Reflect.construct(Function, ["return 1"])', 'Function'),
    fails('const F = Function', 'Function'),
    fails('register(Function)', 'Function'),
  ],
});

const typedFails = (code: string, name: string) => ({ code, filename: TYPED, errors: forbidden(name) });

typed.run('no-forbidden-apis (typed)', rule, {
  valid: [
    { code: 'declare const dialog: HTMLDialogElement; export const shown = dialog.open;', filename: TYPED },
    { code: 'declare const file: { open(): void }; file.open();', filename: TYPED },
  ],
  invalid: [
    typedFails('parent.open("x");', 'parent.open'),
    typedFails('top?.print();', 'top.print'),
    typedFails('document.defaultView?.open("x");', 'document.defaultView.open'),
    typedFails('const w = window; w.open("x");', 'w.open'),
    typedFails('const { print } = parent;', 'parent.print'),
    {
      code: 'const F = Function; export const f = new F("return 1");',
      filename: TYPED,
      errors: [...forbidden('Function'), ...forbidden('new Function')],
    },
    typedFails(
      'export const f = new ((() => 1).constructor as FunctionConstructor)("return 1");',
      'new Function',
    ),
    typedFails('export const f = ((() => 1).constructor as FunctionConstructor)("return 1");', 'Function'),
    typedFails('parent.Function("return 1");', 'parent.Function'),
    {
      code: 'const nav = navigator; export const s = nav.serviceWorker;',
      filename: TYPED,
      errors: serviceWorker,
    },
  ],
});
