/*
 * The maths-typesetting service a widget receives as `services.tex` (docs/ARCHITECTURE.md 5.11, whose listing
 * names this file, B45), the interface only: `WidgetServices` names it and @zq/contracts may not import src/
 * (4.5). The implementation, `Tex` and `TexSlots` stay in src/engine/render (stage 12, docs/DECISIONS.md B42).
 * Both KaTeX configurations will come from this package's KaTeX module (B42), which waits on the owner's
 * decision on the tree (B27), so `html`'s notes cite it without importing it.
 */

export interface TexService {
  ready(): boolean;
  load(): Promise<void>; // imports KaTeX once: the web chunk, or the locked CDN module in the Artifact
  // KaTeX output from a least-recently-used cache of 1,000 entries keyed by source. 'authored' (the default) is
  // the B33 configuration, 'untrusted' (Bertie's replies, learner text) has trust false, strict 'ignore',
  // maxSize 10 and maxExpand 1000.
  html(src: string, display?: boolean, source?: 'authored' | 'untrusted'): string;
}
