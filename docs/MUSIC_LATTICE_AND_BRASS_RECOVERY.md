# Session recovery: brass-led instrumental search and fifths lattice

[Msg⛛{MUSIC-RECOVERY-20261021}] [Ctx⛛{Research}] [State⛛{Source-derived|Unverified-candidates}]

## Provenance and boundaries
Extracted from an operator conversation concerning a lost instrumental recording and a symbolic music-theory explanation. This is a research handoff, **not** a verified discography, a canonical conlang grammar, or evidence of live system health. Existing PR #25 already explores twelve-tone lexeme rotation; this note does not reimplement it.

## A. Lost ensemble identification
- Operator heard recording on an older MP3 player around **2005–2015**; the ensemble/recording could be older but should predate 2015.
- **Entirely instrumental** as remembered; obscure, loosely post-rock/math-rock-adjacent, but genre is **not** a hard filter.
- **Soft, trumpet-like timbre**, perhaps flugelhorn or mellophone; potentially **two distinct brass layers**.
- Crucial correction: brass is **foreground or co-lead**, not an occasional guest part, sampled pad, or distant orchestral wash.
- Prior long lists of post-rock and jazz candidates did **not** locate the recording; do not present previous guesses as verified matches.
- Future candidate ledger should contain: artist, earliest verified active year, album/year, track, instrument/performer evidence, listening source, confidence, operator verdict, and why rejected.
- Prioritize documentation of actual brass personnel/credits and track-level audible prominence over loose genre tags.
- Do not invent album/track pairs or claim flugelhorn/mellophone without credits or listening evidence.

### Suggested search algorithm (proposal, not measured)
Filter: recording <= 2015, instrumental preference; rank: verified foreground brass (high), multi-brass texture (high), soft trumpet-family timbre (high), complex rock/jazz rhythm (medium), obscurity (medium). Negative evidence: vocals, brass only in one incidental passage, later release, previously rejected by operator. A persistent rejection ledger prevents duplicate recommendations.

## B. Fifths/fourths as a testable pitch-class lattice
In 12-tone equal temperament, identify pitch classes with Z/12Z:
- Ascending fifth: F(n) = (p + 7n) mod 12.
- Ascending fourth: Q(n) = (p + 5n) mod 12.
- Fifth orbit from C=0: [0,7,2,9,4,11,6,1,8,3,10,5], returning to 0 at n=12.
- Fourth orbit from C=0: [0,5,10,3,8,1,6,11,4,9,2,7], returning to 0 at n=12.
- Inverse property: 7 + 5 = 12 ≡ 0 (mod 12).
- Opposite nodes on fifth cycle: F(n+6) - F(n) ≡ 6 (mod 12), the tritone.
- Enharmonic **pitch-class** identity does not mean identical notation, spelling, or harmonic function.
- Fifth-axis distance is not itself a model of perceived harmonic tension; tonic/dominant/secondary dominant labels require tonal context.
- Lydian and Phrygian are modal systems, not simply the sharpward/flatward direction of key signatures.

### Proposed experimental OmniTag mapping (not canonical)
```text
[Msg⛛{MUSIC-LATTICE}]
[Ctx⛛{12TET}]
[Root⛛{C:0}]
[Transform⛛{P5:+7mod12}]
[Inverse⛛{P4:+5mod12}]
[Axis⛛{Tritone:+6mod12}]
[State⛛{Proposed}]
```
The symbolic overlay ΨΛΘΣΞΦΩ is a mnemonic/conlang rendering. It is not evidence of quantum computation or a physically multidimensional tonal system. A future parser could validate the arithmetic while retaining symbolic annotation as optional display metadata.

## C. Follow-up acceptance checks
1. Verify and deduplicate candidate artist/album/track pairs against source credits before presenting.
2. Ask operator about acoustic vs amplified sound, pulse/drum style, and the MP3 source; retain rejection outcomes.
3. Unit-test 12 fifth/fourth steps, inverse property, and six-step tritone symmetry.
4. Cross-reference PR #25 before integrating music-specific grammar or code.
5. Keep this archival note separate from production authority and executable colony orchestration.

[State⛛{Research-preserved|Implementation-proposed|No-build-claim}]
