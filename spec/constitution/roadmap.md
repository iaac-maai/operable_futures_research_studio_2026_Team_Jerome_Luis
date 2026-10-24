# Roadmap

1. Calibrate: agree the risk matrix and thresholds per element (columns, beams, slabs, brick walls) with structural engineers. Fix the photo protocol (coin, element tag, distance). Set consent and data rules.
2. Build and test: collect and label phone photos, train the detector and segmenter, compare against buildings an engineer has already assessed.
   Goal: flag every crack the engineer rated High, and send only a few cases to an expert.
3. Widen the scope, only if the Phase 2 goal is met: more materials, ground fissures, multi-storey frames, offline use.

## Dates (from the syllabus)
- 29 Oct 2026: segmentation tree, full data map (availability, access, format, gaps), repository and AGENTS.md, agent working on real data as a first test.

## 10-week plan (26 Oct 2026 to 3 Jan 2027)

![Timeline](../../figures/09_timeline.png)

Weeks start on Monday. The only fixed date from the syllabus is 29 Oct; add the other review dates when they are known.
Assumption: weeks 9 and 10 fall in the winter break, so they hold only write-up and evaluation.
"At risk" means the task depends on the engineering partner.

| Workstream | Task | Weeks | At risk |
|---|---|---|---|
| Deliverables | 29 Oct: tree, data map, repo, AGENTS.md, first test on real data | 1 | |
| Data | SDNET2018 first test through the quality gate | 1 | |
| Data | Download CrackSeg9k, Darbhanga, CODEBRIM; check formats and licences | 2 | |
| Data | Map public labels to the five patterns | 2 to 3 | |
| Pilot | Collect pilot photos (about 30 cracks, `spec/features/photo_protocol.md`) | 2 | |
| Pilot | Prepare and label the pilot photos | 2 to 3 | |
| Pilot | Tune the quality gate on pilot photos | 3 to 4 | |
| Pilot | Coin detection and width measurement | 4 to 6 | |
| Models | U-Net on CrackSeg9k and masonry masks | 3 to 5 | |
| Models | Pattern model, pre-trained on public sets | 5 to 7 | |
| Models | YOLO element detector | 6 to 8 | |
| Engineering partner | Contact partners (Order of Engineers Tripoli, volunteer networks) | 1 to 2 | |
| Engineering partner | Calibration sessions: matrix, thresholds, protocol | 3 to 6 | yes |
| Engineering partner | Engineer-labelled photos | 6 to 10 | yes |
| Integration | End-to-end pipeline on pilot photos | 7 to 8 | |
| Integration | Streamlit prototype | 8 to 9 | |
| Integration | Evaluate against the baseline (confusion tables) | 9 to 10 | yes |
| Integration | Write-up and figures | 9 to 10 | |

Milestones: week 1 (29 Oct) deliverables; week 4 pilot done and gate tuned; week 6 matrix signed off (at risk); week 8 end-to-end demo on pilot photos; week 10 first measured results (at risk).

Fallback: if no partner has agreed by week 4, the pipeline is evaluated on pilot photos against our own width measurements only, the triage matrix stays illustrative, and the report says so.

## Open items
- Impact section: indicator with unit, baseline, target, evidence.
- Engineering partner and labelled photos.
