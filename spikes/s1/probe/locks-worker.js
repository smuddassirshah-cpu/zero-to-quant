// Spike S1 probe: holds one Web Lock in a dedicated worker, for the cross-agent step of platform.web-locks.
//
// Decision notes:
// - The lock's callback never returns on its own, so the page's ifAvailable request must get null and its
//   steal: true request must end this hold; the worker reports how its request ended (AbortError on a steal).
// - No import or export: the page starts it as a classic worker, the common case for a lock holder.

const post = m => self.postMessage(m);

self.onmessage = e => {
  const m = e.data;
  if (!m || m.cmd !== 'hold' || typeof m.name !== 'string') return;
  const locks = self.navigator?.locks;
  if (!locks || typeof locks.request !== 'function') {
    post({ type: 'no-locks' });
    return;
  }
  locks.request(m.name, lock => {
    post({ type: 'held', granted: !!lock });
    return new Promise(() => {}); // held until stolen or the worker ends
  }).then(
    () => post({ type: 'ended', name: null }),
    err => post({ type: 'ended', name: err?.name ?? null, message: String(err?.message ?? err).slice(0, 200) }),
  );
};

post({ type: 'ready', hasLocks: typeof self.navigator?.locks?.request === 'function' });
