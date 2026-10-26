# Decisions log

Newest last. Each entry: date, decision, reason, status.

## D1 (2026-10-24): five crack patterns, not six
The deck (slide 5) names six crack types; the matrix (slide 7) and the code use five.
Decision: keep five. "Diagonal crack" and "stair-step crack in brick" both map to `diagonal_step`; "column crack" maps to `column_or_beam`.
Reason: the matrix rates both the same in every width band, and fewer classes need less labelled data.
Status: provisional, to confirm with the engineering partner in Phase 1.

## D2 (2026-10-24): boundary widths go to the wider band
Width bands are lower-inclusive: 1.0 mm is in `1_to_3`, 3.0 mm is in `over_3`.
Reason: any doubt goes towards more caution (AGENTS.md rule 2). Previously 3.0 mm fell in `1_to_3`.
Status: illustrative until calibrated.

## D3 (2026-10-24): failed measurement means Expert needed
A missing, NaN, negative or infinite width or confidence returns Expert needed, never a matrix level.
Reason: before this, NaN confidence and negative width returned Low, breaking rules 2 and 3.

## D4 (2026-10-24): confidence threshold is fixed in code
`CONFIDENCE_THRESHOLD = 0.8` is a module constant; callers cannot lower it.
Reason: a caller could pass `threshold=0` and turn any guess into Low.
Status: 0.8 is illustrative; the real value comes from the missed-High vs sent-to-expert curve on a labelled test set (deck slide 7).

## D5 (2026-10-24): every result carries a reason and a review flag
`assess()` returns level, reason and `engineer_review` (true for High and Expert needed). `triage()` still returns the level only.
Reason: rule 4 (an engineer confirms every High and referral) and the atomic problem ("with the reason").

## D6 (2026-10-25): non-commercial datasets are for research only
PHI-Net (CC BY-NC-SA 4.0) and CODEBRIM (non-commercial; trained models may not be used commercially) may be used to explore and pre-train in the studio.
Any model meant for real deployment is retrained without them, on CC0 / CC BY data and our own photos.
Reason: their licences forbid commercial use, and a deployed tool may later be run by a company or a funded programme.

## D7 (2026-10-25): SDNET2018 is a code test, not training data for thresholds
Public sets (crack-seg, Darbhanga, SDNET2018, METU, Strathclyde, run on 25 Oct) are used for the 29 Oct first test on real data. They do not set any threshold, because they are not phone photos and have no scale reference.
Thresholds for the quality gate come from the pilot phone photos; triage thresholds come from the engineering partner.

## D8 (2026-10-25): measure sharpness at a fixed working size
The quality gate scales every image down to a long side of 512 px before measuring sharpness and brightness.
Reason: the first real-data test rejected 67% of the Darbhanga brick images (768 px) as blurred; the same images scaled to 416 px failed only 11% (sample of 107 images). Laplacian variance depends on resolution, so phone photos (about 4000 px) would almost all fail.
Status: 512 px is illustrative; check on the pilot phone photos.

## D9 (2026-10-25): Ultralytics YOLO is AGPL-3.0
The `ultralytics` package (YOLO) is licensed AGPL-3.0, or under a paid Enterprise licence [35]. Using it in the studio is fine; any tool offered to others over a network must publish its source under AGPL-3.0, or buy the Enterprise licence, or swap the detector.
Decision: use it for research now; decide before any deployment. Keep the detector behind one function in `src/` so it can be swapped.
Status: open, to revisit before Phase 3.

## D10 (2026-10-25): engineering partners
The engineering partners are Engineers Without Borders and a third-party structural engineer. The agreement with the structural engineer is under construction.
They label photos, give the baseline ratings (an engineer's visual check), and sign off the risk matrix and thresholds.
Status: Engineers Without Borders named; structural engineer to confirm.

## D11 (2026-10-25): plan follows the syllabus dates
The plan runs to the final presentation on 17 Dec and the blog post by 24 Dec, with the midterm on 6 Nov, the hackathon (beta) on 16 to 20 Nov and the baseline comparison on 3 Dec (`spec/constitution/roadmap.md`). It replaces the earlier plan, which assumed a winter break and ran to 3 Jan.

## D12 (2026-10-25): the blur check is not trusted on smooth walls yet
Laplacian variance rejected 75 to 89% of SDNET2018 wall and deck tiles, most of them in focus but smooth (visual check of 8). Hairline cracks on smooth walls would be sent to retake again and again.
Decision: keep the check (a retake is never a Low, so it is safe), but do not tune it on public data. Choose the measure and threshold on the pilot photos, using the deliberately blurred shots as ground truth.
Status: open; confirmed on METU building walls (61% of cracked tiles rejected); results in `docs/experiments/2026-10-25_quality_gate_first_test.md`.

## D13 (2026-10-25): the name is Second Look
The project is called Second Look everywhere: repo, decks, logo, blog post. "Crack triage" is no longer used as a name; "triage" stays only as the word for what the tool does.
Reason: the 22 Oct deck said "Crack triage" while the repo said "Second Look"; one name for the logo and the weekly decks.

## D14 (2026-10-25): the concept is buildings in informal neighbourhoods
Second Look is for cracks in buildings in slum-like, informal or ageing unsupervised neighbourhoods, not bridges, roads or pavement.
Data is ranked by how close it is to that case (`docs/data_map.md`, section 0). Bridge and pavement sets (CODEBRIM, SDNET2018 decks and pavement) are off-concept; road-heavy sets (crack-seg, CrackSeg9k) are generic pre-training only.
Reason: the team's concept; earlier data choices leaned on bridge and pavement sets because they are the largest public ones.

## D15 (2026-10-25): train crack finding now; danger rating waits for our own data
Public data is enough to train crack segmentation, crack detection and crack / no-crack (`docs/data_map.md`, section 0b). It is not enough for the crack pattern (no dataset uses our five classes), width in mm (no scale anywhere), or Low / Medium / High per crack (Haiti and Nepal rate whole buildings).
Decision: the hackathon beta trains the crack-finding step on public data. Pattern labels, width and danger ratings come from hand labelling, the pilot photos and the engineering partners; those tasks stay on the critical path.

## D16 (2026-10-26): the segmentation tree shows only what the tool works on
Out-of-scope items (unauthorised construction, earthquake triggers, rebar and foundations, overridden warnings) and the Phase 3 item (soil erosion) are removed from the tree. The "Warnings overridden" branch is gone; "Data is scarce" becomes branch D. What the tool does not cover is stated once, in `spec/constitution/mission.md`.
The tree figure is redrawn as a flowchart: rounded pills for the macro problem and the four branches, letter tags on the connectors, circles for the micro items, then the atomic problem and the final output. Yellow marks the path into the atomic problem (B, C, B1, B2, B3, C1), navy the supporting context.
Reason: team feedback; out-of-scope nodes were unnecessary detail and the old box layout was hard to read.

## D17 (2026-10-26): scope is reinforced concrete; a material check comes first
Following the professor's feedback (26 Oct): the tool assesses cracks in reinforced concrete elements only (walls, columns, beams, slabs). A material check runs right after the quality check: concrete continues; not concrete or unsure goes to an engineer ("Expert needed: material not supported"). Brick image sets (Darbhanga, Strathclyde) become the "not concrete" examples for training this check.
Consequence: the brick stair-step pattern leaves the matrix; the diagonal pattern now means a diagonal (shear) crack in concrete.
Reason: fits the timeline, the professor's advice, the reference thesis (reinforced concrete) and the Haiti and Nepal surveys (concrete-frame buildings).

## D18 (2026-10-26): two users and a human-in-the-loop learning loop
The resident takes the photo; the engineer reviews every High and every referral on a review screen and confirms or corrects it. Corrections are stored as labels and the learned models (material, crack, pattern) are retrained in batches, each new version checked on held-out engineer-rated photos before use.
We call it human-in-the-loop learning, not reinforcement learning: it is supervised retraining with expert feedback. The risk matrix never changes automatically (AGENTS.md rule 5).

## D19 (2026-10-26): every result carries confidence, not only a colour
Each stage reports its output with a confidence: material, crack found, width in mm with an uncertainty range, pattern probability, and an overall confidence with the level. Full list in `spec/features/pipeline.md`.

## D20 (2026-10-26): risk matrix v2, with elements, warning signs and next steps
The matrix now has three parts: a base level from seven reinforced-concrete patterns x four width bands; element criticality (a column raises one level); and seven warning signs that can only raise the level (growing, rust staining, sticking openings, recent earthquake, added floors: +1; offset and sagging: straight to High). The width used is the upper end of the measurement. Every result adds a next step with a recheck interval. The values live in `src/triage/risk_matrix_v2.json` (version 2.0-illustrative), readable and editable by an engineer; each change is a new version recorded here.
Supersedes D1 (five patterns): surface map cracking replaces plaster crazing; vertical wall crack and column-or-beam are replaced by the element axis and by flexural, horizontal-column, along-bar and joint patterns.
Calibration plan in `spec/features/risk_matrix.md`: literature anchors (to verify in the sources), a sense check on the Haiti definitions, an engineer card session, a test on engineer-rated photos, and versioning. All values stay illustrative until then.
