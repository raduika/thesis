# Ralph loop progress — thesis grammar/style/abbreviations pass

Chapters in scope: uvod.tex, kap01.tex, kap02.tex, kap03.tex, zaver.tex, abstract-cs.tex, zkratky.tex

Status legend: [ ] not started, [~] in progress, [x] done

## Task 1 — Czech grammar (čárky, shoda, pády, diakritika, překlepy)
- [x] uvod.tex
- [x] kap01.tex
- [ ] kap02.tex
- [ ] kap03.tex
- [ ] zaver.tex
- [ ] abstract-cs.tex

## Task 2 — Style glitches (terminologie, kalky, opakování, formátování, odkazy)
- [x] uvod.tex
- [x] kap01.tex
- [ ] kap02.tex
- [ ] kap03.tex
- [ ] zaver.tex
- [ ] abstract-cs.tex

## Task 3 — Abbreviations (zkratky.tex)
- [ ] grep all chapters for abbreviations/acronyms actually used
- [ ] cross-check vs current zkratky.tex list (ČLR, EU, FOMO, GDPR, SyRI, UI, USA)
- [ ] add missing entries
- [ ] normalize existing entries to consistent format

## Notes / decisions log
(newest on top)

- Iter 2: kap01.tex done (grammar+style). Found house style confirmed: section/subsection headings should NOT end with a period (majority convention across kap02/kap03); kap01 had 5 headings with stray trailing periods -> removed. Fixed rusism-style calque "rozuměla pod rozumem" -> "rozuměla rozumem"; added missing apposition commas around "fronésis, \uv{praktická moudrost},"; fixed "v zkušenosti" -> "ve zkušenosti"; fixed inconsistent citation (bare "(1977)" for Foucault instead of \parencite{Foucault77}); stripped stray leading whitespace on 40 lines + 2 interior double-spaces. Verified cross-refs to "oddíl X.Y" (hand-numbered, no \label/\ref used anywhere in thesis - confirmed this is the consistent house style, not a bug) - all checked accurate, no fix needed. No new abbreviations (only UI, USA appear, both already in zkratky.tex). Build clean (53p). TODO for later kap02 pass: it also has 4 headings with stray trailing periods (lines 21,33,46,65 in kap02.tex) - fix when doing kap02. Next: kap02.tex.

- Iter 1: uvod.tex done (grammar+style). Fixed: double semicolon typo ("; ;" -> ";"), wrong capital letter after colon mid-sentence ("Rozsáhlá" -> "rozsáhlá"), stray leading whitespace on ~9 lines (cosmetic, no semantic change), one repetition ("je... a je zdrojem" -> "je... a bývá zdrojem"). No new abbreviations found in uvod.tex beyond ones already in zkratky.tex (SyRI, GDPR, ČLR referenced; AI Act appears but is covered under UI entry). Build verified clean (53p). Next: kap01.tex.
