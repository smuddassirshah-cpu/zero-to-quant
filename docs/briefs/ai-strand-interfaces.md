# AI strand: shared interfaces (binding on every AI-strand content agent)

Set by the main session, session AK, 27 Nov 2026. A brief that disagrees with this file loses.

- **Data folder.** Every strand data file lives in `app/content/data/ai/`, named `<course>-<what>.<ext>` (shared files keep their names: `names.txt`, `tiny-shakespeare.txt`, `tiny-shakespeare-vocab.json`, `autograd.py`). At most 256 KB a file. A content agent may add files there with its own course prefix, and never edits another course's files. Credit and licence lines go in `app/content/data/ai/README.md`.
- **Autograd.** `app/content/data/ai/autograd.py` is written by the `backprop` L4 author to the contract in `docs/briefs/backprop.md` Level 4, then frozen: later courses ship it verbatim through the code widget's `files` and never edit it. A missing op is raised in the report, not patched in.
- **Course ops modules are per level.** `<course>_ops_l<n>.py` in the data folder (for example `interp_ops_l2.py`). A level may import an earlier level's module; it never edits one. This replaces the single appended `<course>_ops.py` some briefs describe.
- **GPT weights.** The app's tiny GPT is trained by a committed number script; weights are split one file per block plus one for embeddings and the head (`gpt-w-embed.json`, `gpt-w-block0.json`, ...), each under 256 KB, so a two-block model fits (`interp` L1 needs two blocks).
- **Budgets.** `docs/reports/ai-timing-spike.md`: a graded case costs 1 s or less on desktop, 10 s or less with an explicit `budget`, never above 20 s. Training thresholds carry a margin.
- **Number scripts.** Run with the venv `/tmp/claude-0/-home-user-zero-to-quant/b2245dfe-6f55-570e-8d22-d9384c33129b/scratchpad/venv/bin/python` (Python 3.12, the CI pins: NumPy 2.0.2, scikit-learn 1.6.1, SciPy 1.18.1). Figures from any other scikit-learn version are recomputed.
- **Playthrough.** `--local-cdn /tmp/claude-0/-home-user-zero-to-quant/b2245dfe-6f55-570e-8d22-d9384c33129b/scratchpad/aitiming/pkgs` (jsDelivr is blocked in the sandbox).
- **Drills.** `ml-int` L2 uses the drill recipe in `docs/AUTHORING.md` (no new engine pattern).
