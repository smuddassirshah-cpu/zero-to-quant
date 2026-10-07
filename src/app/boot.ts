// Stage 1's empty app: proves both targets build and boot. Stage 4 replaces it with the
// start-up sequence of ARCHITECTURE.md 5.10.1; the shell copy moves to copy.ts at stage 5.
export interface BootInfo {
  readonly target: 'web' | 'artifact';
  readonly devRoutes: boolean;
}

export function boot(root: HTMLElement, info: BootInfo): void {
  const title = document.createElement('h1');
  title.textContent = 'Zero to Quant';
  const note = document.createElement('p');
  note.textContent = info.devRoutes
    ? `Development build, ${info.target} platform`
    : 'The engine is being built.';
  root.replaceChildren(title, note);
  root.dataset.zqBoot = info.target;
}
