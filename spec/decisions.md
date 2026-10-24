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
SDNET2018 is used for the 29 Oct first test on real data. It does not set any threshold, because its tiles are camera crops with no scale reference.
Thresholds for the quality gate come from the pilot phone photos; triage thresholds come from the engineering partner.
