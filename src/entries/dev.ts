import { boot } from '../app/boot.ts';

const root = document.getElementById('app');
if (!root) throw new Error('Missing #app element');
boot(root, { target: __TARGET__, devRoutes: __DEV_ROUTES__ });
