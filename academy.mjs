#!/usr/bin/env node
/* Runs the SDAIA Academy engine for this course: node academy.mjs <command> [options]

   The engine is looked for in $ACADEMY_ENGINE, then in the folder named by the file
   .academy-engine beside this one (one line: the engine's absolute path; "academy new" writes it
   when the course is not beside the engine, and git ignores it), then in ../engine. Its major
   version must be the one "engine" in course.json asks for. The command runs on this course
   (--root is added unless you pass one) with the arguments as given, and its exit code is the
   engine's: 0 done, 1 the course has problems, 2 the command could not run (which is also what
   this file answers when it finds no engine). */

import { spawnSync } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const COURSE = path.dirname(fileURLToPath(import.meta.url));
const POINTER = path.join(COURSE, '.academy-engine');
const CANNOT_RUN = 2;

function fail(message) {
  process.stderr.write(`academy.mjs: ${message}\n`);
  process.exit(CANNOT_RUN);
}

function readJson(file) {
  try {
    return JSON.parse(fs.readFileSync(file, 'utf8'));
  } catch (e) {
    return fail(`cannot read ${file}: ${e.message}`);
  }
}

/* the first line of .academy-engine, as a folder (relative to the course when it is not absolute) */
function pointed() {
  try {
    const line = fs.readFileSync(POINTER, 'utf8').split(/\r?\n/)[0].trim();
    return line ? path.resolve(COURSE, line) : null;
  } catch {
    return null;
  }
}

const CANDIDATES = [process.env.ACADEMY_ENGINE, pointed(), path.join(COURSE, '..', 'engine')].filter(Boolean);
const engine = CANDIDATES.find((dir) => fs.existsSync(path.join(dir, 'bin', 'academy.mjs')));
if (!engine) {
  fail(`no engine found in ${CANDIDATES.join(', ')}. Tell this course where the engine is in one of three ways: set ACADEMY_ENGINE to the engine folder, write the engine folder's absolute path on the first line of ${POINTER}, or put the course folder beside the engine folder, which is named engine`);
}

const wanted = String(readJson(path.join(COURSE, 'course.json')).engine || '').replace(/^[~^]/, '').split('.')[0];
const version = String(readJson(path.join(engine, 'package.json')).version || '');
if (wanted && version.split('.')[0] !== wanted) {
  fail(`course.json asks for engine ${wanted}, and ${engine} is engine ${version}. Check out the engine at a v${wanted} tag (git -C "${engine}" checkout v${wanted}.<minor>.<patch>), or point ACADEMY_ENGINE at one`);
}

const args = process.argv.slice(2);
const hasRoot = args.some((a) => a === '--root' || a.startsWith('--root='));
const result = spawnSync(process.execPath, [path.join(engine, 'bin', 'academy.mjs'), ...args, ...(hasRoot ? [] : ['--root', COURSE])], { stdio: 'inherit' });
if (result.error) fail(result.error.message);
process.exit(result.status == null ? CANNOT_RUN : result.status);
