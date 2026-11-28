# representations level 3: performance task

- `homework-3.json`, item `h-vae-step`, index 0. Kind `code` (Python, difficulty 5).
- Matched objective: l12 "Write the reparameterisation trick, and train a small VAE on two-dimensional data." (also l9 "Write a latent variable model as a story, and sample data from it.", and the derive objectives of l10 and l11).
- Task: from a one-line stub, `vae_step(x_batch, params, eps, lr)` builds one VAE training step with the autograd: encode with `representations_ops_l3.vae_encode`, sample $z = \mu + e^{\ell/2}\epsilon$, decode, form the minibatch loss (closed-form KL minus $\ln p(\mathbf x \mid z)$ with its constant, averaged over the batch), backpropagate, and return the loss with the parameters after one plain gradient step.
- 9 hidden tests, 2 examples, all on the shipped `representations-l12-vae.json` weights and fixed noise: the loss to 9 places and updated decoder bias to 6 on the trained weights; the loss and an updated weight table on the starting weights at two step sizes; a one-point batch (loss and an encoder table); a log-variance head pushed to $-800$, so the variance underflows to 0 (the zero-variance guard: the loss must be finite to 6 places and the update finite); a step of size 0 that must return the weights unchanged. Four mutants: the KL through the log of the variance (fails the guard), the noise scaled by the variance, the rebuild term summed while the KL is averaged, and a step up the gradient. The number script reruns every test with the solution and with a hand-written backward pass.
- Overlapping screens: l11 screen 9 codes the KL from the log-variance; l12 screens 8 and 9 code `reparam_sample`, `vae_loss` and the Adam loop `train_vae` with a scaffold (screens counted from 0). The task asks for the whole step from nothing, with plain gradient descent, the guard and a one-point batch that no screen tests.

Gates:
1. `node tools/validate.mjs`: 0 errors.
2. `VOICE_BASE=app/content/courses/representations python3 docs/reviews/voice-scan.py 35`: 0 over 35 words and 0 lesson ids in code spans.
3. Numbers script `docs/reports/representations-L3-numbers.py` through `node tools/run-number-scripts.mjs --only representations-L3` (strict): every check passes, exit 0; it reruns the solution and a hand-backprop twin against every test.
4. Playthrough `--set representations/homework-3 --local-cdn <pkgs>`, with and without `--mobile`: all passed, the starter fails. Desktop time per hidden test in Pyodide: under 40 ms.
