/*
 * The global keys of docs/ARCHITECTURE.md 5.5: the key column of its table.
 * Decision notes:
 * - Only the keys are typed. The actions are prose in 5.5 and the doc names no identifiers for them, so
 *   naming them is left to the keymap's own stage.
 * - 5.5 puts the keymap in src/engine/interaction/keymap.ts. The key names are one shared type for that
 *   keymap and any keyboard help, so they are kept in @zq/contracts as a types-only contract [our choice];
 *   the main session ratifies the location in docs/DECISIONS.md B45.
 * - Keys are named as the table writes them ('H', not KeyboardEvent.key's 'h'); the keymap maps events
 *   onto them. The rest of 5.5 is behaviour the host, the player and ui/ implement.
 */

type Digit = '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9';

/** 5.5's table: Enter, Escape, H, W, D, T, 1 to 9 and ?. */
export type GlobalKey = 'Enter' | 'Escape' | 'H' | 'W' | 'D' | 'T' | Digit | '?';
/** On by default; off under Settings, Accessibility, "Single-key shortcuts" (decision 34; WCAG 2.2 SC 2.1.4). Enter and Escape stay. */
export type SingleKey = Exclude<GlobalKey, 'Enter' | 'Escape'>;
