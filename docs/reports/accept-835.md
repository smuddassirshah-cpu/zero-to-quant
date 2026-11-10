# Accept repair for ENGINE-BACKLOG 835

The 18 STILL-DEAD text-mode `accept` entries listed in `engine-835.md` are repaired. Only `accept[]` changed; no `answer`, prompt or Fluency set was touched (none of the 18 is in a Fluency set). Each rewrite was checked against `answer` with sympy.

| File | Item | Old spelling | New spelling |
|---|---|---|---|
| integrals/homework-2 | item 0 | `x^4+2e^(3x)-2ln(x)` | `x^4+2e^{3x}-2ln(x)` |
| integrals/homework-2 | item 0 | `x^4+2e^(3*x)-2ln(x)` | `x^4+2e^{3*x}-2ln(x)` |
| integrals/homework-2 | item 0 | `x^4+2*e^(3x)-2ln(x)` | `x^4+2*e^{3x}-2ln(x)` |
| integrals/homework-2 | item 0 | the six same forms with `+C` or `+c` | same, with `e^{..}` |
| integrals/l9-undo-chain | screen 2 | `sin(x²)`, `sin(x**2)` | deleted (duplicates `sin(x^2)`) |
| integrals/l9-undo-chain | screen 4 | `ln(x**2+1)` | deleted (duplicates `ln(x^2+1)`) |
| integrals/l9-undo-chain | quiz 0 | `sin(x³)`, `sin(x**3)` | deleted (duplicates `sin(x^3)`) |
| odes/homework-4 | item 2 | `2e^(-t)cos(2t)+0.5e^(-t)sin(2t)`, `e^(-t)(2cos(2t)+sin(2t)/2)` | `e^{-t}` in place of `e^(-t)` |
| odes/l15-solving-with-laplace | screen 4 | `e^(-t)*cos(2t)+0.5*e^(-t)*sin(2t)`, `e^(-t)(cos(2t)+sin(2t)/2)` | `e^{-t}` in place of `e^(-t)` |

Counts: 13 rewritten, 5 deleted, 0 left.

Checks: audit STILL-DEAD 0, WRONG-OK 0; validator 0 errors; playthrough green for integrals/homework-2, integrals/l9-undo-chain, odes/homework-4, odes/l15-solving-with-laplace.

Note: other `e^(3x)` accepts in integrals/homework-2 (the `lnx` and `ln|x|` forms) were not in the list and were left alone.
