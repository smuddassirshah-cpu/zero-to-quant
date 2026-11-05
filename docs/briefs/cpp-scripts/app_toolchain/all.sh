#!/bin/bash
# Every problem, c++17 and c++20, in the app's own toolchain. Usage: ZQ_PKGS=<pkgs> bash all.sh > ../results_app.txt
cd "$(dirname "$0")"
python3 dump.py > /dev/null
for p in P-move-buffer P-copy-samples P-hand-vtable P-add-overflows P-unique-ptr P-shared-ptr P-scope-guard P-vec P-clone-basket; do
  for std in c++17 c++20; do STD=$std node run.mjs $p 2>&1 | grep "^\[P-\|FAIL"; done
done
