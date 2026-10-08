/*
 * The global keys of docs/ARCHITECTURE.md 5.5, encoded from its table for engine/interaction/keymap.ts
 * and the keyboard help sheet in ui/.
 * Decision notes:
 * - Keys are named as the table writes them ('H', not KeyboardEvent.key's 'h'); the keymap maps events
 *   onto them. Action names reuse 5.7.1's overlay and player event names where one exists [our choice].
 * - The rest of 5.5 is behaviour with no shape to type: Enter acts only with focus on the screen itself;
 *   in a text field or the code editor the keys are off and Ctrl or Cmd with Enter replaces Enter; the
 *   widget keys belong to useDrag, useRoving and useLiftDrop (src/engine/interaction); the pointer
 *   pipeline, announcements, focus and phone text entry belong to the host, the player and ui/.
 */

type Digit = '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9';

/** 5.5's table, one action per key; the digits 1 to 9 select option cards in order. */
export interface GlobalKeymap extends Readonly<Record<Digit, 'option'>> {
  readonly Enter: 'primary'; // Check, Continue or Try again
  readonly Escape: 'close'; // close the open sheet or modal; cancel a drag in progress
  readonly H: 'hints'; // the hint ladder (when available)
  readonly W: 'why'; // after grading
  readonly D: 'describe'; // describe('full') for every widget on the screen
  readonly T: 'table'; // Table view of the focused chart
  readonly '?': 'keys'; // keyboard help sheet
}
export type GlobalKey = keyof GlobalKeymap;
export type GlobalAction = GlobalKeymap[GlobalKey];
/** On by default; off under Settings, Accessibility, "Single-key shortcuts" (decision 34; WCAG 2.2 SC 2.1.4). Enter and Escape stay. */
export type SingleKey = Exclude<GlobalKey, 'Enter' | 'Escape'>;
