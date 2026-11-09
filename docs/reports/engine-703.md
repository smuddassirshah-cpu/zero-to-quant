# Engine 703

Cause confirmed: the taylor/homework-1 `-marked-440` PNG was white below the first viewport (the app scrolls in an inner container, so Chromium does not paint beyond it).

Fix: in `shot` (`app/tools/playthrough.mjs`) an element shot first grows the viewport to the card's full height, counting any scrolling ancestor, capped at 8000 px, then restores it. Applies at desktop and every extra width; window shots are unchanged.

Test: `app/tools/test-playthrough-tall.mjs` with a fixture longform about three viewports tall, decoding the PNG: height over two viewports and lower rows inked. It fails without the fix and passes with it. `test-playthrough-overflow.mjs` still passes. Taylor shots re-read: full model and rubric painted.
