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
Public sets (crack-seg and Darbhanga, run on 25 Oct; SDNET2018) are used for the 29 Oct first test on real data. They do not set any threshold, because they are not phone photos and have no scale reference.
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
Status: open; results in `docs/experiments/2026-10-25_quality_gate_first_test.md`.
