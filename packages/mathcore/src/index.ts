// @zq/mathcore (docs/ARCHITECTURE.md 4.3). This entry exports nothing: each module is imported by its
// subpath, `@zq/mathcore/rng` for src/rng.ts through the package's `./*` export, so the units that write
// modules in parallel never edit a shared barrel [our choice].
export {};
