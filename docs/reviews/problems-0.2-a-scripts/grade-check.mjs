#!/usr/bin/env node
/* Second read, problems 0.2 (a): what the engine's own graders do with each part of equations 1 to 3 and functions 1 to 3.
   Harness as problems-1.3-c-scripts/grade-check.mjs (app/js/engine/grade.js and the local Compute Engine), with two additions:
     form        the shape check of the expression widget ("simplified", "expanded", "factorised-fully"), copied from
                 app/js/engine/widgets/expression.js formOk, so a typed row is graded as the widget grades it (same && shaped)
     sets        numeric set answers (answers: [..], unordered) through numSetGrade, with each wrong[].value string
   Every answer and accept[] form must grade correct, every wrong[] must grade wrong and land on its own key, and every TYPED
   row must grade as expected. A TYPED row with a 7th field is one the reader holds to be a fault: it prints as FINDING.

   node docs/reviews/problems-0.2-a-scripts/grade-check.mjs --local-cdn <pkgs>      (from the repo root) */
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';

const argv = process.argv.slice(2);
const cdn = argv[argv.indexOf('--local-cdn') + 1];
const ceFile = path.join(cdn, 'cortex-js-compute-engine-0.30.2', 'package', 'dist', 'compute-engine.min.umd.js');
const g = { console, setTimeout, clearTimeout, document: { addEventListener() {}, querySelector() { return null; } }, navigator: {} };
g.window = g; g.globalThis = g; vm.createContext(g);
vm.runInContext(fs.readFileSync(ceFile, 'utf8'), g);
const ce = new (g.ComputeEngine.ComputeEngine || g.ComputeEngine)();
g.ZQ = {}; vm.runInContext(fs.readFileSync('app/js/engine/grade.js', 'utf8'), g);
const G = g.ZQ.grade;

const SETS = [['equations', 1], ['equations', 2], ['equations', 3], ['functions', 1], ['functions', 2], ['functions', 3]];
const T = true, F = false;
const RETYPE = 'retyping the inequality of the question grades correct on a "Solve" part';
const HALF = 'an unfinished line of the working grades correct on a "Solve" part';
const E = 'equations', FN = 'functions';
/* [course, set, item, part (1-based), typed text, expected, finding?]
   Rows that do not parse in a numeric field ("9p", "x=2", "0 to 60") are expected false: the field will not submit them.
   Lower-case letters for F, P, V grade correct (the text fallback lowers case). */
const TYPED = [
  // equations 1
  [E, 1, 'p-family-tickets', 1, 'a-5', T], [E, 1, 'p-family-tickets', 1, '-5+a', T], [E, 1, 'p-family-tickets', 1, 'c=a-5', T],
  [E, 1, 'p-family-tickets', 1, 'a-5.00', T], [E, 1, 'p-family-tickets', 1, '5-a', F], [E, 1, 'p-family-tickets', 1, 'a', F],
  [E, 1, 'p-family-tickets', 2, '5a-15', T], [E, 1, 'p-family-tickets', 2, '-15+5a', T], [E, 1, 'p-family-tickets', 2, '2a+3(a-5)', F],
  [E, 1, 'p-family-tickets', 2, '2a+3a-15', F], [E, 1, 'p-family-tickets', 2, '5(a-3)', T],
  [E, 1, 'p-family-tickets', 3, '5(a-3)', T], [E, 1, 'p-family-tickets', 3, '(a-3)5', T], [E, 1, 'p-family-tickets', 3, '5(-3+a)', T],
  [E, 1, 'p-family-tickets', 3, '5\\left(a-3\\right)', T], [E, 1, 'p-family-tickets', 3, '5\\times(a-3)', T], [E, 1, 'p-family-tickets', 3, '-5(3-a)', T],
  [E, 1, 'p-family-tickets', 3, '5a-15', F], [E, 1, 'p-family-tickets', 3, '5(a-15)', F],
  [E, 1, 'p-family-tickets', 4, '75', T], [E, 1, 'p-family-tickets', 4, '£75', T], [E, 1, 'p-family-tickets', 4, '75.00', T],
  [E, 1, 'p-food-van', 1, '4.2n-45', T], [E, 1, 'p-food-van', 1, '4.20n-45', T], [E, 1, 'p-food-van', 1, '-45+4.2n', T],
  [E, 1, 'p-food-van', 1, '\\frac{21}{5}n-45', T], [E, 1, 'p-food-van', 1, '\\frac{21n}{5}-45', T], [E, 1, 'p-food-van', 1, '4.2n-45.00', T],
  [E, 1, 'p-food-van', 1, '6.5n-2.3n-45', F], [E, 1, 'p-food-van', 1, '6.50n-2.30n-45', F], [E, 1, 'p-food-van', 1, '(6.5-2.3)n-45', F],
  [E, 1, 'p-food-van', 2, '4.2n-129', T], [E, 1, 'p-food-van', 2, '-129+4.2n', T], [E, 1, 'p-food-van', 2, '4.2(n-20)-45', F], [E, 1, 'p-food-van', 2, '4.2n-84-45', F],
  [E, 1, 'p-food-van', 3, '8.4n-174', T], [E, 1, 'p-food-van', 3, '-174+8.4n', T], [E, 1, 'p-food-van', 3, '4.2n-45+4.2n-129', F],
  [E, 1, 'p-food-van', 4, '582', T], [E, 1, 'p-food-van', 4, '£582', T],
  [E, 1, 'p-number-trick', 1, '2n+26', T], [E, 1, 'p-number-trick', 1, '26+2n', T], [E, 1, 'p-number-trick', 1, '5n+20-3n+6', F], [E, 1, 'p-number-trick', 1, '2(n+13)', T],
  [E, 1, 'p-number-trick', 2, '2(n+13)', T], [E, 1, 'p-number-trick', 2, '(n+13)2', T], [E, 1, 'p-number-trick', 2, '2(13+n)', T], [E, 1, 'p-number-trick', 2, '2n+26', F],
  [E, 1, 'p-market-pitch', 1, 's^2+2s', T], [E, 1, 'p-market-pitch', 1, '2s+s^2', T], [E, 1, 'p-market-pitch', 1, 's^{2}+2s', T], [E, 1, 'p-market-pitch', 1, 's\\times s+2s', T],
  [E, 1, 'p-market-pitch', 1, 's(s+2)', F], [E, 1, 'p-market-pitch', 1, 's^2+s2', T],
  [E, 1, 'p-market-pitch', 2, '7s^2+6s', T], [E, 1, 'p-market-pitch', 2, '6s+7s^2', T], [E, 1, 'p-market-pitch', 2, '3s^2+6s+4s^2', F], [E, 1, 'p-market-pitch', 2, 's(7s+6)', T],
  [E, 1, 'p-market-pitch', 3, 's(7s+6)', T], [E, 1, 'p-market-pitch', 3, '(7s+6)s', T], [E, 1, 'p-market-pitch', 3, 's(6+7s)', T], [E, 1, 'p-market-pitch', 3, '7s^2+6s', F],
  // equations 2
  [E, 2, 'p-climbing-wall', 1, '45+8c=213', T], [E, 2, 'p-climbing-wall', 1, '213=8c+45', T], [E, 2, 'p-climbing-wall', 1, '8c=213-45', T],
  [E, 2, 'p-climbing-wall', 1, '8\\times c+45=213', T], [E, 2, 'p-climbing-wall', 1, '45+8c', F], [E, 2, 'p-climbing-wall', 1, 'c=21', T],
  [E, 2, 'p-climbing-wall', 4, '7.28', T], [E, 2, 'p-climbing-wall', 4, '£7.28', T], [E, 2, 'p-climbing-wall', 4, '7.2857', F], [E, 2, 'p-climbing-wall', 4, '7.29', F],
  [E, 2, 'p-climbing-wall', 4, '728', F], [E, 2, 'p-climbing-wall', 3, '31', T], [E, 2, 'p-climbing-wall', 3, '31.875', F],
  [E, 2, 'p-cottage-share', 1, '\\frac{x}{5}-20=\\frac{x+30}{6}', T], [E, 2, 'p-cottage-share', 1, '\\frac{x+30}{6}=\\frac{x}{5}-20', T],
  [E, 2, 'p-cottage-share', 1, '\\frac{x}{5}=\\frac{x+30}{6}+20', T], [E, 2, 'p-cottage-share', 1, '\\frac{x}{5}-\\frac{x+30}{6}=20', T],
  [E, 2, 'p-cottage-share', 1, '\\frac{x+30}{6}+20=\\frac{x}{5}', T], [E, 2, 'p-cottage-share', 1, '6x-600=5x+150', T], [E, 2, 'p-cottage-share', 1, '0.2x-20=\\frac{x+30}{6}', T],
  [E, 2, 'p-cottage-share', 1, '\\frac{x+30}{6}-20=\\frac{x}{5}', F], [E, 2, 'p-cottage-share', 1, '\\frac{x}{5}-\\frac{x+30}{6}', F],
  [E, 2, 'p-cottage-share', 2, '750', T], [E, 2, 'p-cottage-share', 2, '£750', T],
  [E, 2, 'p-cottage-share', 4, '115.71', T], [E, 2, 'p-cottage-share', 4, '£115.71', T], [E, 2, 'p-cottage-share', 4, '115.714', T], [E, 2, 'p-cottage-share', 4, '115.7', F], [E, 2, 'p-cottage-share', 4, '116', F],
  [E, 2, 'p-power-tariffs', 1, '7.2', T], [E, 2, 'p-power-tariffs', 1, '36/5', T], [E, 2, 'p-power-tariffs', 2, '7.5', T], [E, 2, 'p-power-tariffs', 2, '15/2', T], [E, 2, 'p-power-tariffs', 2, '7 1/2', T],
  [E, 2, 'p-power-tariffs', 4, '9', T], [E, 2, 'p-power-tariffs', 4, '9p', F], [E, 2, 'p-power-tariffs', 4, '0.09', F],
  [E, 2, 'p-interest-split', 1, '12000-s', T], [E, 2, 'p-interest-split', 1, '-s+12000', T], [E, 2, 'p-interest-split', 1, '12,000-s', T, 'the prose prints £12,000; with the comma typed the expression does not grade correct'],
  [E, 2, 'p-interest-split', 1, 's-12000', F],
  [E, 2, 'p-interest-split', 2, '0.04s+0.065(12000-s)=660', T], [E, 2, 'p-interest-split', 2, '0.065(12000-s)+0.04s=660', T], [E, 2, 'p-interest-split', 2, '660=0.04s+0.065(12000-s)', T],
  [E, 2, 'p-interest-split', 2, '780-0.025s=660', T], [E, 2, 'p-interest-split', 2, '40s+65(12000-s)=660000', T], [E, 2, 'p-interest-split', 2, '0.04s+0.065\\times(12000-s)=660', T],
  [E, 2, 'p-interest-split', 2, '0.04\\times s+0.065\\times(12000-s)=660', T], [E, 2, 'p-interest-split', 2, '0.04s+0.065(12000-s)', F], [E, 2, 'p-interest-split', 2, '0.04s+0.065(s-12000)=660', F],
  [E, 2, 'p-interest-split', 2, '0.04s+0.065(12,000-s)=660', T, 'the comma of £12,000 typed inside the equation'],
  [E, 2, 'p-interest-split', 3, '4800', T], [E, 2, 'p-interest-split', 3, '4,800', T], [E, 2, 'p-interest-split', 3, '£4,800', T], [E, 2, 'p-interest-split', 4, '2400', T],
  // equations 3
  [E, 3, 'p-bakery-stock', 1, '240-18h\\ge60', T], [E, 3, 'p-bakery-stock', 1, '240-18h\\geq60', T], [E, 3, 'p-bakery-stock', 1, '240-18h>=60', T], [E, 3, 'p-bakery-stock', 1, '240-18h≥60', T],
  [E, 3, 'p-bakery-stock', 1, '60\\le240-18h', T], [E, 3, 'p-bakery-stock', 1, '18h+60\\le240', T], [E, 3, 'p-bakery-stock', 1, '240-18h\\geqslant60', T], [E, 3, 'p-bakery-stock', 1, '240-18h>60', F],
  [E, 3, 'p-bakery-stock', 1, '240-18h=60', F], [E, 3, 'p-bakery-stock', 1, '240-18h', F],
  [E, 3, 'p-bakery-stock', 2, 'h\\le10', T], [E, 3, 'p-bakery-stock', 2, '10\\ge h', T], [E, 3, 'p-bakery-stock', 2, 'h<=10', T], [E, 3, 'p-bakery-stock', 2, 'h≤10', T],
  [E, 3, 'p-bakery-stock', 2, 'h<10', F], [E, 3, 'p-bakery-stock', 2, 'h=10', F], [E, 3, 'p-bakery-stock', 2, '10', F], [E, 3, 'p-bakery-stock', 2, '0\\le h\\le10', F],
  [E, 3, 'p-bakery-stock', 2, '240-18h\\ge60', F, RETYPE], [E, 3, 'p-bakery-stock', 2, '-18h\\ge-180', F, HALF],
  [E, 3, 'p-fridge-temperature', 1, '\\frac{F-32}{1.8}', T], [E, 3, 'p-fridge-temperature', 1, 'C=\\frac{F-32}{1.8}', T], [E, 3, 'p-fridge-temperature', 1, '\\frac{F-32}{1.8}=C', T],
  [E, 3, 'p-fridge-temperature', 1, '\\frac{5(F-32)}{9}', T], [E, 3, 'p-fridge-temperature', 1, '\\frac{5}{9}(F-32)', T], [E, 3, 'p-fridge-temperature', 1, '(F-32)\\div1.8', T],
  [E, 3, 'p-fridge-temperature', 1, '\\frac{F}{1.8}-\\frac{32}{1.8}', T], [E, 3, 'p-fridge-temperature', 1, '\\frac{5F-160}{9}', T], [E, 3, 'p-fridge-temperature', 1, '\\frac{f-32}{1.8}', T],
  [E, 3, 'p-fridge-temperature', 1, 'F=1.8C+32', F], [E, 3, 'p-fridge-temperature', 1, '1.8C=F-32', F],
  [E, 3, 'p-fridge-temperature', 2, '5', T], [E, 3, 'p-fridge-temperature', 2, '5.0', T],
  [E, 3, 'p-fridge-temperature', 3, 'F\\le41', T], [E, 3, 'p-fridge-temperature', 3, '41\\ge F', T], [E, 3, 'p-fridge-temperature', 3, 'F<41', F], [E, 3, 'p-fridge-temperature', 3, 'F\\le5', F],
  [E, 3, 'p-fridge-temperature', 3, '\\frac{F-32}{1.8}\\le5', F, RETYPE], [E, 3, 'p-fridge-temperature', 3, 'F-32\\le9', F, HALF],
  [E, 3, 'p-fridge-temperature', 4, '19', T],
  [E, 3, 'p-van-value', 1, '\\frac{P-V}{k}', T], [E, 3, 'p-van-value', 1, 't=\\frac{P-V}{k}', T], [E, 3, 'p-van-value', 1, '\\frac{P}{k}-\\frac{V}{k}', T], [E, 3, 'p-van-value', 1, '(P-V)\\div k', T],
  [E, 3, 'p-van-value', 1, '-\\frac{V-P}{k}', T], [E, 3, 'p-van-value', 1, '\\frac{V-P}{k}', F], [E, 3, 'p-van-value', 1, '\\frac{p-v}{k}', T],
  [E, 3, 'p-van-value', 1, 'kt=P-V', F],
  [E, 3, 'p-van-value', 3, 't<7.5', T], [E, 3, 'p-van-value', 3, '7.5>t', T], [E, 3, 'p-van-value', 3, 't<\\frac{15}{2}', T], [E, 3, 'p-van-value', 3, 't<7\\frac{1}{2}', T],
  [E, 3, 'p-van-value', 3, 't\\le7.5', F], [E, 3, 'p-van-value', 3, 't>7.5', F], [E, 3, 'p-van-value', 3, '24000-2400t>6000', F, RETYPE],
  [E, 3, 'p-fund-weight', 1, '\\frac{wb}{1-w}', T], [E, 3, 'p-fund-weight', 1, 'a=\\frac{wb}{1-w}', T], [E, 3, 'p-fund-weight', 1, '\\frac{bw}{1-w}', T], [E, 3, 'p-fund-weight', 1, '\\frac{-bw}{w-1}', T],
  [E, 3, 'p-fund-weight', 1, 'wb\\div(1-w)', T], [E, 3, 'p-fund-weight', 1, '\\frac{b}{\\frac{1}{w}-1}', T], [E, 3, 'p-fund-weight', 1, 'a=w(a+b)', F], [E, 3, 'p-fund-weight', 1, '\\frac{wb}{w-1}', F],
  [E, 3, 'p-fund-weight', 2, '4000', T], [E, 3, 'p-fund-weight', 2, '£4,000', T], [E, 3, 'p-fund-weight', 3, '2000', T],
  // functions 1
  [FN, 1, 'p-exchange-kiosk', 1, '1.15', T], [FN, 1, 'p-exchange-kiosk', 1, '23/20', T], [FN, 1, 'p-exchange-kiosk', 1, '€1.15', T], [FN, 1, 'p-exchange-kiosk', 1, '1.2', F],
  [FN, 1, 'p-exchange-kiosk', 2, '1.15x-3', T], [FN, 1, 'p-exchange-kiosk', 2, 'E(x)=1.15x-3', T], [FN, 1, 'p-exchange-kiosk', 2, '-3+1.15x', T], [FN, 1, 'p-exchange-kiosk', 2, '1.15\\times x-3', T],
  [FN, 1, 'p-exchange-kiosk', 2, '\\frac{115x}{100}-3', T], [FN, 1, 'p-exchange-kiosk', 2, '1.15(x-40)+43', T], [FN, 1, 'p-exchange-kiosk', 2, '1.15x', F], [FN, 1, 'p-exchange-kiosk', 2, 'x1.15-3', T],
  [FN, 1, 'p-exchange-kiosk', 3, '342', T], [FN, 1, 'p-exchange-kiosk', 3, '€342', T], [FN, 1, 'p-exchange-kiosk', 4, '200', T], [FN, 1, 'p-exchange-kiosk', 4, '£200', T],
  [FN, 1, 'p-van-fuel', 4, '0, 60', T], [FN, 1, 'p-van-fuel', 4, '60,0', T], [FN, 1, 'p-van-fuel', 4, '0 and 60', T], [FN, 1, 'p-van-fuel', 4, '60', F], [FN, 1, 'p-van-fuel', 4, '0, 400', F],
  [FN, 1, 'p-van-fuel', 4, '0 to 60', F],
  [FN, 1, 'p-van-fuel', 5, '24, 48', T], [FN, 1, 'p-van-fuel', 5, '48, 24', T], [FN, 1, 'p-van-fuel', 5, '12, 36', F],
  [FN, 1, 'p-stone-throw', 3, '0, 45', T], [FN, 1, 'p-stone-throw', 3, '45, 0', T], [FN, 1, 'p-stone-throw', 3, '0, 25', F], [FN, 1, 'p-stone-throw', 3, '25, 45', F],
  [FN, 1, 'p-stone-throw', 4, '1, 3', T], [FN, 1, 'p-stone-throw', 4, '3 and 1', T], [FN, 1, 'p-stone-throw', 4, 't = 1, t = 3', T], [FN, 1, 'p-stone-throw', 4, '1 or 3', T], [FN, 1, 'p-stone-throw', 4, '2 ± 1', T],
  [FN, 1, 'p-stone-throw', 4, '1', F], [FN, 1, 'p-stone-throw', 4, '-1, 5', F],
  [FN, 1, 'p-sapling-log', 3, '5w+12', T], [FN, 1, 'p-sapling-log', 3, '12+5w', T], [FN, 1, 'p-sapling-log', 3, 'h(w)=5w+12', T], [FN, 1, 'p-sapling-log', 3, '5(w-1)+17', T], [FN, 1, 'p-sapling-log', 3, '5w+17', F],
  [FN, 1, 'p-sapling-log', 4, '12', T],
  // functions 2
  [FN, 2, 'p-candle-burn', 1, '-2.5', T], [FN, 2, 'p-candle-burn', 1, '−2.5', T], [FN, 2, 'p-candle-burn', 1, '-5/2', T], [FN, 2, 'p-candle-burn', 1, '-2.50', T], [FN, 2, 'p-candle-burn', 1, '2.5', F],
  [FN, 2, 'p-candle-burn', 3, '10.4', T], [FN, 2, 'p-candle-burn', 3, '52/5', T], [FN, 2, 'p-candle-burn', 3, '10.24', F], [FN, 2, 'p-candle-burn', 3, '10', F],
  [FN, 2, 'p-path-and-pipe', 1, '0.5', T], [FN, 2, 'p-path-and-pipe', 1, '1/2', T], [FN, 2, 'p-path-and-pipe', 1, '.5', T],
  [FN, 2, 'p-path-and-pipe', 2, '0.5x+2', T], [FN, 2, 'p-path-and-pipe', 2, '\\frac{1}{2}x+2', T], [FN, 2, 'p-path-and-pipe', 2, '\\frac{x}{2}+2', T], [FN, 2, 'p-path-and-pipe', 2, 'y=0.5x+2', T],
  [FN, 2, 'p-path-and-pipe', 2, '.5x+2', T], [FN, 2, 'p-path-and-pipe', 2, '0.5(x+4)', T], [FN, 2, 'p-path-and-pipe', 2, '2+\\frac{x}{2}', T], [FN, 2, 'p-path-and-pipe', 2, '2x+2', F], [FN, 2, 'p-path-and-pipe', 2, '2y=x+4', F],
  [FN, 2, 'p-path-and-pipe', 3, '-2', T], [FN, 2, 'p-path-and-pipe', 3, '-2/1', T], [FN, 2, 'p-path-and-pipe', 3, '-1/0.5', T],
  [FN, 2, 'p-path-and-pipe', 4, '-2x+7', T], [FN, 2, 'p-path-and-pipe', 4, '7-2x', T], [FN, 2, 'p-path-and-pipe', 4, 'y=-2x+7', T], [FN, 2, 'p-path-and-pipe', 4, '-2(x-5)-3', T], [FN, 2, 'p-path-and-pipe', 4, '2x+7', F],
  [FN, 2, 'p-path-and-pipe', 5, '2', T], [FN, 2, 'p-path-and-pipe', 5, 'x=2', F],
  [FN, 2, 'p-two-gyms', 1, '18', T], [FN, 2, 'p-two-gyms', 1, '£18', T], [FN, 2, 'p-two-gyms', 4, '42', T],
  // functions 3
  [FN, 3, 'p-bakery-trays', 1, '-100', T], [FN, 3, 'p-bakery-trays', 1, '-£100', T], [FN, 3, 'p-bakery-trays', 1, '£-100', T],
  [FN, 3, 'p-bakery-trays', 2, '2, 10', T], [FN, 3, 'p-bakery-trays', 2, '10 and 2', T], [FN, 3, 'p-bakery-trays', 2, 'x = 2 or x = 10', T], [FN, 3, 'p-bakery-trays', 2, '2', F],
  [FN, 3, 'p-sledge-cyclist', 3, '6', T], [FN, 3, 'p-sledge-cyclist', 3, '0, 6', F],
  [FN, 3, 'p-two-cultures', 4, '3.3', T], [FN, 3, 'p-two-cultures', 4, '3.32', T], [FN, 3, 'p-two-cultures', 4, '3.4', F], [FN, 3, 'p-two-cultures', 4, '3.5', F], [FN, 3, 'p-two-cultures', 4, '3', F],
  [FN, 3, 'p-two-cultures', 5, '2000', T], [FN, 3, 'p-two-cultures', 5, '2,000', T], [FN, 3, 'p-two-cultures', 5, '1990', T], [FN, 3, 'p-two-cultures', 5, '1970', T], [FN, 3, 'p-two-cultures', 5, '1996', T],
  [FN, 3, 'p-two-cultures', 5, '1900', F], [FN, 3, 'p-two-cultures', 5, '2100', F],
  [FN, 3, 'p-track-cubic', 2, '0, 3', T], [FN, 3, 'p-track-cubic', 2, '3, 0', T], [FN, 3, 'p-track-cubic', 2, '0, 3, 3', F], [FN, 3, 'p-track-cubic', 4, '1, 4', T], [FN, 3, 'p-track-cubic', 4, '1', F],
];

let checks = 0, fails = 0, findings = 0;
const say = (ok, finding, msg) => { checks++; if (ok) return; if (finding) { findings++; console.log('FINDING ' + msg + '   [' + finding + ']'); } else { fails++; console.log('FAIL    ' + msg); } };

const isSet = (w) => G.isSetSpec(w) && w.unordered === true;
const gradeNumeric = (w, text) => {
  if (isSet(w)) { const r = G.numSetGrade(w, text); return { ok: !!r.ok, key: r.key }; }
  const pct = w.unit === '%';
  let v = G.parseNum(text); if (pct && !text.includes('%')) v /= 100;
  if (!Number.isFinite(v)) return { ok: false, key: 'NOPARSE' };
  if (G.within(v, w.answer, w.tol)) return { ok: true, key: null };
  const m = G.matchWrong(v, w.wrong, w.tol); return { ok: false, key: m ? m.id : null };
};
/* the widget's shape check (expression.js formOk), for the three forms these sets use */
const head = (j) => (Array.isArray(j) ? j[0] : null), args = (j) => (Array.isArray(j) ? j.slice(1) : []);
const hasSum = (j) => head(j) === 'Add' || head(j) === 'Subtract' || args(j).some(hasSum);
const size = (j) => (Array.isArray(j) ? 1 + args(j).reduce((a, x) => a + size(x), 0) : 1);
const isSumLike = (j) => head(j) === 'Add' || head(j) === 'Subtract';
const formOk = (w, L) => {
  if (!w.form) return true;
  try {
    return G.withParsed(ce, L, w.functions || [], (e) => {
      const j = e.json;
      if (w.form === 'expanded') return isSumLike(j) ? args(j).every(t => !hasSum(t)) : !hasSum(j);
      if (w.form === 'factorised-fully') return G.shapeFullyFactorised(j);
      if (w.form === 'simplified') { try { return size(j) <= size(e.simplify().json); } catch { return true; } }
      throw new Error('form not modelled: ' + w.form);
    });
  } catch (err) { if (/not modelled/.test(err.message)) throw err; return true; }
};
const gradeExpr = (w, L) => {
  const fo = { functions: w.functions || [], integers: w.integers || [] };
  const eq = (t) => { try { return !!G.exprEqual(ce, L, t, fo) || (!!G.normExpr(L) && G.normExpr(L) === G.normExpr(t)); } catch { return false; } };
  const same = [w.answer, ...(w.accept || [])].some(eq);
  if (same) return formOk(w, L) ? { ok: true, key: null } : { ok: false, key: 'form' };
  const x = (w.wrong || []).find(x => x.tex && eq(x.tex));
  return { ok: false, key: x ? x.id : null };
};

for (const [course, n] of SETS) {
  const set = JSON.parse(fs.readFileSync(`app/content/courses/${course}/problems-${n}.json`, 'utf8'));
  for (const it of set.items) it.parts.forEach((p, i) => {
    const w = p.widget, where = `${course} ${n} ${it.id} part ${i + 1}`, by = (p.feedback && p.feedback.byKey) || {};
    const typed = TYPED.filter((r) => r[0] === course && r[1] === n && r[2] === it.id && r[3] === i + 1);
    const row = (r, res) => say(res.ok === r[5], r[6], `${where}: typed "${r[4]}" ${r[5] ? 'refused' : 'accepted'} (key ${res.key})`);
    const wrongs = (grade) => {
      for (const x of w.wrong || []) {
        const r = grade(x);
        say(!r.ok && r.key === x.id, null, `${where}: wrong "${x.id}" ${x.value ?? x.tex} grades ${r.ok ? 'correct' : 'to key ' + r.key}`);
        say(!!by[x.id], null, `${where}: wrong "${x.id}" has no byKey line`);
      }
    };
    if (w.kind === 'numeric' && isSet(w)) {
      say(gradeNumeric(w, w.answers.join(', ')).ok, null, `${where}: set answer does not grade correct`);
      say(gradeNumeric(w, w.answers.slice().reverse().join(', ')).ok, null, `${where}: set answer reversed does not grade correct`);
      wrongs((x) => gradeNumeric(w, String(x.value)));
      say(!!by.count, null, `${where}: no "count" line`);
      for (const r of typed) row(r, gradeNumeric(w, r[4]));
    } else if (w.kind === 'numeric') {
      say(G.within(w.answer, w.answer, w.tol), null, `${where}: answer outside its own band`);
      wrongs((x) => gradeNumeric(w, String(x.value)));
      for (const x of w.wrong || []) { const t = (x.tol && x.tol.abs) || 0; if (t > 0 && Math.abs(x.value) > 0 && t > 0.2 * Math.abs(x.value)) console.log(`NOTE    ${where}: wrong "${x.id}" = ${x.value} has band ±${t}, wider than 20% of the value`); }
      for (const r of typed) row(r, gradeNumeric(w, r[4]));
    } else if (w.kind === 'expression') {
      say(gradeExpr(w, w.answer).ok, null, `${where}: answer does not grade correct (${JSON.stringify(gradeExpr(w, w.answer))})`);
      for (const a of w.accept || []) say(gradeExpr(w, a).ok, null, `${where}: accept "${a}" does not grade correct (${JSON.stringify(gradeExpr(w, a))})`);
      wrongs((x) => gradeExpr(w, x.tex));
      if (w.form) say(!!by.form, null, `${where}: form "${w.form}" with no "form" line`);
      for (const r of typed) row(r, gradeExpr(w, r[4]));
    }
  });
}
console.log(`grade-check: ${checks} checks, ${fails} failures, ${findings} findings (rows the reader holds to be faults)`);
process.exit(fails ? 1 : 0);
