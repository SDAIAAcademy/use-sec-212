# الذكاء الاصطناعي في المدن والسياحة والحج: notes for coding agents

This repository is one SDAIA Academy course: **الذكاء الاصطناعي في المدن والسياحة والحج** (`use-sec-212`, catalog code USE-SEC-212). It holds content only.
The SDAIA Academy engine (major version 1) turns it into a static site: slide decks
with speaker notes and a presenter view, the course page, lab pages, a practice page and Markdown
for AI assistants. The repository is public, and so is everything in it.

## What is where

| Path | What it is |
|---|---|
| `course.json` | The manifest: every fact about the course, once (titles, outcomes, units, sessions, labs, capstone) |
| `slides/*.html` | Slide sources: `<section class="slide" id="…">` elements only; `slides/<lang>/` holds a translation with the same ids |
| `labs/` | Notebooks or lab pages, data and helpers (`labs/_src/` and `labs/_tools/` are never published) |
| `assessments/bank.json` | Practice and checkpoint questions (published). Exam items never live here |
| `assets/` | Images, and `course.css` or `course.js` when the course extends the engine. Everything here is published |
| `reviews/` | `CHANGELOG.md`, the log of what changed in each version, is committed. Trainers' feedback files (`reviews/inbox/`) and their triage (`reviews/*-feedback.*`) stay on this computer: git ignores them |
| `README.md` | About the course, for people who find the repository. Its marked blocks (`<!-- academy:<name> -->`) repeat `course.json` and are written by `node academy.mjs readme --write` |
| `GLOSSARY.md` | The term table of a translated course: one Arabic term for each English term. Committed, not published |

Values that start with the word REPLACE and a colon are what the scaffold could not know.
Replace each one; `node academy.mjs check` lists those that are left.

## Commands

Run them from this folder. `academy.mjs` finds the engine in `$ACADEMY_ENGINE`, then in the
folder written on the first line of the file `.academy-engine` here (git ignores that file, so
a clone has none), then in `../engine`. It checks the engine's major version against
`course.json` and runs it. If it answers "no engine found", do one of the three things the
message names: set `ACADEMY_ENGINE` to the engine folder, write the engine's absolute path into
`.academy-engine`, or put this folder beside the folder `engine`. If you do not know where the
engine is, ask once.

| Command | What it does |
|---|---|
| `node academy.mjs dev` | Build, serve on http://127.0.0.1:4173 and rebuild on every change |
| `node academy.mjs build --strict` | Build the site into `dist/`; `--strict` fails on warnings |
| `node academy.mjs check` | The gates: manifest, slides, labs, checkpoints, forbidden text, translation parity, outcome coverage, the README's blocks, files that git ignores. Its last line counts the findings of each code |
| `node academy.mjs check --only <unit id>` | The same for one unit (`--only day2`): its deck, labs, questions and part of the manifest |
| `node academy.mjs check --layout --shots` | Every slide in a browser, and the reading view on a phone; contact sheets under `.shots/` to look at |
| `node academy.mjs check --links` | Every external address requested once |
| `node academy.mjs readme --write` | Write the README's marked blocks again from `course.json` |
| `node academy.mjs feedback reviews/inbox/*.json` | Read trainers' feedback files: where each comment points, what is stale, what can be applied. Running it again keeps the answers already recorded |
| `node academy.mjs resolve <review.json> --id <id> --status resolved --note "…"` | Record the answer to one comment; the id is the "Id" column of the review |
| `node academy.mjs exam --pool exam --bank <private file>` | An exam paper and its key, written to `exams/` (ignored by git); `--pool practice` for a mock exam from the public questions |
| `node academy.mjs publish` | Build in strict mode, run the static gates, and push `dist/` to the `gh-pages` branch; an error stops it (`--dry` shows what would be sent) |

`node academy.mjs help` lists every command, `node academy.mjs help <command>` its options.
A change is finished when `build --strict` and `check` end with 0 errors and 0 warnings, you
have looked at the contact sheets of the decks you changed, and the change is committed. Before
the course is handed over or published, one more gate: clone it into a temporary folder and
build, check and run the lab solutions there. Every other gate reads this folder, and a clone
has only what was committed.

## Skills

The engine repository holds the skills under `skills/`, each a folder with a `SKILL.md`. Read the
one that fits the task before you start, and follow it:

| Skill | When |
|---|---|
| `academy-course-build` | Designing and writing the course from its catalog entry: outline, manifest, labs, decks, gates |
| `academy-course-update` | Changing the course from comments in words or from trainers' feedback files |
| `academy-course-translate` | Making or maintaining the other language edition |
| `academy-assessment` | Checkpoints, the question bank, exam items, papers with keys |
| `academy-course-migrate` | Moving material from the previous slide system |
| `academy-catalog-build` | Working through many catalog entries, one course per folder (run from the folder above this one) |
| `academy-engine-dev` | A change the engine itself needs (a component, a plugin, a check); never patch the engine from here |

## Rules for a public course repository

- Nothing internal from the catalog: no hours per badge domain, no priorities, no exam weights, no
  notes on which entries a course was derived from. Use what
  `node academy.mjs catalog --code USE-SEC-212` prints; it leaves those out (the engine
  finds the catalog beside itself; `--catalog <folder>` names it when it is elsewhere).
- No exam questions. Exam items live in `assessments/*.private.json` (ignored by git) or in a file
  outside the repository passed to `academy exam --bank <file>`. `assessments/bank.json` holds
  practice and checkpoint questions only.
- No paths on someone's computer (a drive letter, a home folder), no clock times in slides or
  pages (durations only), no break slides (trainers press B in the deck), no em dashes. When
  such a thing is the subject of a lab (a path that is the planted fault, a timestamp in the
  data), mark it as a deliberate example: the attribute `data-example` on its element, or the
  words `academy:example` on the same line of a file that is not HTML.
- Every file a lab needs is committed. `check` reports a course file that git ignores
  (`repo/ignored`) with the line to add to `.gitignore`.
- No unpublished sources: cite only what a reader can open. Every source goes into
  `course.json` (`sources`) with its address. Product facts come from official pages.
- Text comes from the manifest once: outcomes and lab steps are written in `course.json` and
  appear on the slides, the course page and the Markdown by themselves.
- Slide ids are stable slugs of the idea (`bpe-merges`), never numbers; comments and citations
  point at them. An id never changes when its slide is reworded.
  `node academy.mjs ids --write` gives a slide without one its id.
- Every user-facing text exists in English and Arabic when the course has both, changed in the
  same commit; Arabic uses Western digits, the terms of `GLOSSARY.md`, and the engine's own
  words where the engine writes them (a course is «المقرر», a lab «المختبر»).
- A checkpoint's wrong options each name their misconception; a lab's steps add up to its
  minutes; a changed lab is run again before a slide quotes its output.
- On overflow, fix the wording, then split the slide. Never shrink the type.
- A change to published content bumps `version` in `course.json` and gets an entry in
  `reviews/CHANGELOG.md`.
- Commit messages are plain imperative sentences, with no attribution trailer of any kind.
- Creating a remote repository, pushing, publishing and switching GitHub Pages on are the
  Director's decisions: do them only when asked in the conversation, and say first what becomes
  public.
