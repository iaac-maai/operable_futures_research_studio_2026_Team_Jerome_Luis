# Data map

Version for 29 Oct 2026. Public dataset facts checked on the source pages on 24 Oct 2026; numbers in brackets refer to `docs/sources.md`.
Raw data is never committed; it lives in `data/` (git-ignored).

## 1. What each pipeline stage needs, and where it comes from

![Data coverage](../figures/05_data_coverage.png)

| Stage | Needs | Covered by | Gap |
|---|---|---|---|
| Quality gate | Photos labelled usable / unusable (blur, light, coin visible) | Nothing yet | Rules first (blur and brightness scores), then tune on our own phone photos |
| YOLO detector | Bounding boxes for element (column, beam, slab, brick wall) and crack | Nothing with boxes. PHI-Net has component type as a class only [26] | Draw boxes on our own photos |
| U-Net segmenter | Pixel masks of cracks | CrackSeg9k [25] | Few columns, beams and brick walls |
| Measurement | Crack width in mm with a coin for scale | Nothing public | Our photos with a coin, width measured by the engineer (crack gauge) |
| Pattern model | Labels for the 5 patterns (`spec/decisions.md` D1) | Nothing uses our labels. SDNET2018 is crack / no crack only [22]; PHI-Net has damage type with 4 classes [26] | Label mapping, then our own labels |
| Agent (building data) | Construction type, age, footprint | Candidates in section 2 | Source not chosen; access not agreed |
| Triage rules | Signed-off matrix and thresholds | Illustrative matrix (`spec/features/triage.md`) | Engineer sign-off (Phase 1) |
| Evaluation | On-site engineer rating per crack (ground truth) and an engineer's photo-only rating (baseline) | Nothing yet | Engineering partner (`spec/features/evaluation.md`) |

## 2. Datasets

![Dataset sizes](../figures/06_dataset_sizes.png)

| Data | Source | Availability | Access | Format | Size | Licence | Covers | Gaps |
|---|---|---|---|---|---|---|---|---|
| SDNET2018 | Utah State University [22] | Available | Public download, no registration | JPEG tiles, crack / no-crack by folder | "Over 56,000" images; 503.8 MB zip | CC BY 4.0 (attribution) | Concrete bridge decks, walls, pavements | Concrete only; no masks, no scale, no brick, columns or beams |
| CrackSeg9k | Harvard Dataverse, doi:10.7910/DVN/EGIEBY [25] | Available | Public download | RGB images and masks, resized to 400 x 400; train/test split included | 9,255 images; two zips, 1.55 GB and 1.26 GB | CC0 1.0 (public domain) | Ten merged crack-segmentation sets | Mostly pavement and concrete; mask format to check on download; no scale |
| PEER Hub ImageNet (PHI-Net) | PEER, UC Berkeley [26][27] | Available | Download page per task; registration not stated | Images with 8 classification tasks (scene, damage state, spalling, material, collapse mode, component type, damage level, damage type) | 36,413 images (as of Nov 2019) | CC BY-NC-SA 4.0 (non-commercial, share-alike) | Post-earthquake structural images | No pixel masks, no width, no scale; non-commercial licence limits any product use |
| Engineer-labelled phone photos | To collect (Phase 2) | Does not exist | Needs engineering partner and resident consent | Photo + coin + element tag; labels: element, material, pattern, width (mm), Low / Medium / High, on-site rating | Target size: assumption, to set with the partner | Ours; consent rules to write | The real target data | Everything: partner, consent, protocol test |
| Engineers' Syndicate list of 106 buildings, Tripoli | MTV Lebanon, 25 Jan 2026 [8] | Reported in the press; list itself not found | Ask the Order of Engineers, Tripoli (assumption: not public) | Unknown | 106 buildings | Unknown | Buildings engineers already judged at risk: candidate ground truth and photo sites | Access, content and format unknown |
| Municipal evacuation list, Tripoli | Government announcement, 9 Feb 2026 [3][5] | Reported; list not found | Ask the municipality (assumption) | Unknown | 114 buildings | Unknown | Same as above | Same as above; overlap with the 106 list unknown [6] |
| BUET factory survey, Dhaka | Reported by AFP, The Daily Star [16][17] | Reported; raw survey not found | Ask BUET (assumption) | Unknown | Unknown | Unknown | Engineer assessments of factory buildings | Frames, Phase 3; old (2013) |
| Building database for the agent (construction type, footprint) | Not chosen | - | Over MCP (planned) | To define | - | - | Context for the agent | Source, schema and access all open |

## 3. Not usable as data
- Example photos in the deck (slide 8): stock images, authors not identified; their risk labels are a visual guess.
- Case-study figures (deaths, evacuations): context for the problem, not training data.

## 4. Open items
- Consent and data rules: the deck says "photos stay with the household"; Phase 2 needs photos for labelling. Write who keeps what, for how long, and how faces and addresses are removed.
- Download one slice of CrackSeg9k and SDNET2018 into `data/` for the first agent test on real data, and record the mask format.
- Approach the Order of Engineers in Tripoli about the 106-building list and an engineering partner.
