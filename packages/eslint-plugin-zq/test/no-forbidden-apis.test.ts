import rule from '../src/rules/no-forbidden-apis.ts';
import { at, tester } from './tester.ts';

const APP = at('src/app/a.ts');
const forbidden = (name: string) => [{ messageId: 'forbidden', data: { name } }];
const serviceWorker = [{ messageId: 'serviceWorker' }];

tester.run('no-forbidden-apis', rule, {
  valid: [
    'import { open } from "./files.ts"; open("x")',
    'function f(print: () => void) { print() }',
    'const window = { open() {} }; window.open()',
    'printer.print()',
    'el.open',
    'document.createElement("div")',
    'document.createElement(tag)',
    '<div />',
    'const navigator = { serviceWorker: 1 }; navigator.serviceWorker',
    { code: 'navigator.serviceWorker.register("/sw.js")', filename: at('src/platform/web/sw-client.ts') },
    { code: 'self.navigator.serviceWorker', filename: at('src/sw/sw.ts') },
  ],
  invalid: [
    { code: 'window.open("x")', errors: forbidden('window.open') },
    { code: 'self.open("x")', errors: forbidden('self.open') },
    { code: 'globalThis.open("x")', errors: forbidden('globalThis.open') },
    { code: 'open("x")', errors: forbidden('open') },
    { code: 'print()', errors: forbidden('print') },
    { code: 'window.print()', errors: forbidden('window.print') },
    { code: 'const o = window["open"]', errors: forbidden('window.open') },
    { code: 'document.createElement("IFRAME")', errors: forbidden('iframe') },
    { code: 'document.createElement(`iframe`)', errors: forbidden('iframe') },
    { code: 'doc.createElementNS(ns, "iframe")', errors: forbidden('iframe') },
    { code: '<iframe src="x" />', errors: forbidden('iframe') },
    { code: 'navigator.serviceWorker.register("/sw.js")', filename: APP, errors: serviceWorker },
    { code: 'window.navigator.serviceWorker', filename: APP, errors: serviceWorker },
    { code: 'eval("1")', errors: forbidden('eval') },
    { code: 'window.eval("1")', errors: forbidden('window.eval') },
    { code: 'globalThis.eval("1")', errors: forbidden('globalThis.eval') },
    { code: 'new Function("return 1")', errors: forbidden('new Function') },
    { code: 'Function("return 1")', errors: forbidden('Function') },
  ],
});
