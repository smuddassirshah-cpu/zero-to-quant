// @zq/contracts (docs/ARCHITECTURE.md 5). This entry exports nothing: each module is imported by its
// subpath, `@zq/contracts/base` for src/base.ts through the package's `./*` export, so the units that
// write modules in parallel never edit a shared barrel [our choice].
export {};
