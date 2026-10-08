/*
 * The global keys of docs/ARCHITECTURE.md 5.5: the key column of its table, for
 * src/engine/interaction/keymap.ts and the keyboard help sheet in src/ui/.
 * Decision notes:
 * - Only the keys are typed. The actions are prose in 5.5 and the doc names no identifiers for them, so
 *   naming them is left to the keymap's own stage.
 * - The type sits here, not in keymap.ts where 5.5 puts the keymap, because the help sheet in src/ui/
 *   needs the same keys and 4.5's table lets ui/ import only `engine/motion` and `@zq/contracts`, not
 *   `engine/interaction` [sourced: ARCHITECTURE.md 4.5] [our choice].
 * - Keys are named as the table writes them ('H', not KeyboardEvent.key's 'h'); the keymap maps events
 *   onto them. The rest of 5.5 is behaviour the host, the player and ui/ implement.
 */

type Digit = '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9';

/** 5.5's table: Enter, Escape, H, W, D, T, 1 to 9 and ?. */
export type GlobalKey = 'Enter' | 'Escape' | 'H' | 'W' | 'D' | 'T' | Digit | '?';
/** On by default; off under Settings, Accessibility, "Single-key shortcuts" (decision 34; WCAG 2.2 SC 2.1.4). Enter and Escape stay. */
export type SingleKey = Exclude<GlobalKey, 'Enter' | 'Escape'>;
