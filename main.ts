// news-image-20261118 — program (Node 22, standard library only).
//
// It hands in the entry's image: the file entry.png beside this program,
// drawn for this competition by draw.py (PIL, deterministic) from the
// reporting of Wednesday 18 November 2026. The program copies it to
// /output/entry.png. A plain copy is byte-identical every run, which is
// what the competition requires (both runs must write the same bytes).
//
// Run it: mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, existsSync } from 'node:fs';
import { join } from 'node:path';

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const source = new URL('./entry.png', import.meta.url);

// Fail loudly instead of copying a missing file: the grader's two runs
// must both write the same bytes, and a silent miss would break that.
if (!existsSync(source)) {
  throw new Error('entry.png is missing from the repository');
}

copyFileSync(source, join(outDir, 'entry.png'));
console.log(`wrote ${join(outDir, 'entry.png')}`);
