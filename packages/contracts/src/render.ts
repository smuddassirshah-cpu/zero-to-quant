/*
 * The maths-typesetting service a widget receives as `services.tex` (docs/ARCHITECTURE.md 5.11), the interface
 * only. 5.11 declares it in src/engine/render, which @zq/contracts may not import (4.5), and `WidgetServices`
 * names it, so it moved here; the implementation, `Tex` and `TexSlots` stay in src/engine/render (stage 12,
 * docs/DECISIONS.md B42). Both KaTeX configurations will come from this package's KaTeX module (B42), which
 * waits on the owner's decision on the tree (B27), so `html`'s notes cite it without importing it.
 */

export interface TexService {
  ready(): boolean;
  load(): Promise<void>; // imports KaTeX once: the web chunk, or the locked CDN module in the Artifact
  // KaTeX output from a cache of 1,000 entries keyed by source. 'authored' (the default) is the B33 configuration,
  // 'untrusted' (Bertie's replies, learner text) has trust false, strict 'ignore', maxSize 10 and maxExpand 1000.
  html(src: string, display?: boolean, source?: 'authored' | 'untrusted'): string;
}
