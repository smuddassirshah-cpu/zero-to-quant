#!/usr/bin/env node
/* Prints the whole item that holds a widget, for reading: node show.mjs <file under app/> <path> [maxChars] */
import path from 'node:path';
import { APP, resolve, readJson } from './lib.mjs';
const [file, where, max = '1800'] = process.argv.slice(2);
const { chain } = resolve(readJson(path.join(APP, file)), where.replace(/\.wrong\[\d+\]$/, ''));
/* the item: the outermost ancestor that is an element of a list (quiz[i], items[i], screens[i]) */
let item = chain[chain.length - 2];
for (let i = 1; i < chain.length; i++) if (Array.isArray(chain[i - 1]) && chain[i] && typeof chain[i] === 'object' && (chain[i].widget || chain[i].parts || chain[i].question || chain[i].prose)) { item = chain[i]; break; }
const strip = (k, v) => (k === 'canvas' || k === 'hints' || k === 'tags' ? undefined : v);
console.log(JSON.stringify(item, strip).slice(0, +max));
