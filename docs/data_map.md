# Data map

Version for 29 Oct 2026. Public dataset facts checked on the source pages on 24 and 25 Oct 2026; numbers in brackets refer to `docs/sources.md`.
Raw data is never committed; it lives in `data/` (git-ignored).

**Bottom line.** Public data can pre-train the detector and the segmenter. No public dataset has an engineer's risk rating on a crack photo with a scale reference, so the engineer-labelled phone photos are unavoidable and are the critical path.

## 1. What each pipeline stage needs, and where it comes from

![Data coverage](../figures/05_data_coverage.png)

| Stage | Needs | Covered by | Gap |
|---|---|---|---|
| Quality gate | Phone photos labelled usable / unusable (blur, light, coin visible) | Pilot photos (section 4), planned | Public sets are camera tiles; SDNET2018 only tests the code |
| YOLO detector | Bounding boxes for element (column, beam, slab, brick wall) and crack | Partly: CODEBRIM has defect bounding boxes [28]; PHI-Net has component type as a class only [26] | No public set has element boxes; draw them on our own photos |
| U-Net segmenter | Pixel masks of cracks | CrackSeg9k [25]; Dais et al. masonry masks [31] | Few columns and beams |
| Measurement | Crack width in mm with a coin for scale | Pilot photos with a crack-width card, planned | Nothing public has a scale reference |
| Pattern model | Labels for the 5 patterns (`spec/decisions.md` D1) | Partly: SDNET2018 crack / no crack [22]; PHI-Net damage type [26]; CODEBRIM spalling, exposed bars, corrosion stains for `spalling_rust` [28]; Darbhanga brick masonry cracks [30] | Nobody uses our labels; needs a mapping, then our own labels |
| Agent (building data) | Construction type, age, footprint | Candidates in section 2 | Source not chosen; access not agreed |
| Triage rules | Signed-off matrix and thresholds | Illustrative matrix (`spec/features/triage.md`) | Engineer sign-off (Phase 1) |
| Evaluation | On-site engineer rating per crack (ground truth) and an engineer's photo-only rating (baseline) | Nothing yet | Engineering partner (`spec/features/evaluation.md`) |

## 2. Datasets

![Dataset sizes](../figures/06_dataset_sizes.png)

### Public image sets

| Data | Source | Availability | Access | Format | Size | Licence | Covers | Gaps |
|---|---|---|---|---|---|---|---|---|
| SDNET2018 | Utah State University [22] | Available | Public page; scripted download blocked (403), download in a browser | JPEG tiles, crack / no-crack by folder | "Over 56,000" images; 503.8 MB zip | CC BY 4.0 | Concrete bridge decks, walls, pavements | Concrete only; no masks, no scale, no brick, columns or beams; camera tiles, not phone photos |
| CrackSeg9k | Harvard Dataverse, doi:10.7910/DVN/EGIEBY [25] | Available | Public download | RGB images and masks, resized to 400 x 400; train/test split included | 9,255 images; two zips, 1.55 GB and 1.26 GB | CC0 1.0 | Ten merged crack-segmentation sets, including a masonry subset (240 images per [32], to confirm on download) | Mostly pavement and concrete; mask format to check; no scale |
| PEER Hub ImageNet (PHI-Net) | PEER, UC Berkeley [26][27] | Available | Download page per task; registration not stated | Images with 8 classification tasks (scene, damage state, spalling, material, collapse mode, component type, damage level, damage type) | 36,413 images (as of Nov 2019) | CC BY-NC-SA 4.0 | Post-earthquake structural images | No masks, no width, no scale; non-commercial |
| CODEBRIM | Zenodo record 2620293 [28], CVPR 2019 paper [29] | Available | Open record, licence file must be accepted | Original images, cropped defects with class labels from bounding boxes, classification sets | 36.4 GB in total (cropped set 7.9 GB); image count not stated on the record | Non-commercial research and education only; no redistribution; trained models may not be used commercially | Five concrete defects on 30 bridges: crack, spalling, exposed bars, efflorescence, corrosion stains | Bridges, not homes; no scale; licence blocks any product use |
| Brick masonry cracks, Darbhanga Fort | Singh and Maity, Mendeley Data [30] | Available | Public download | Images with labels (train / val / test); label format to check on download | 4,259 images (3,407 train incl. 203 without cracks, 639 val, 213 test) | CC BY 4.0 | Superficial cracks in red brick masonry | One heritage structure, not homes; no scale; label format unknown |
| Masonry crack masks, Dais et al. 2021 | GitHub repository [31] | Subset available | Public repository | 224 x 224 images with crack masks | Subset only; count not stated | GPL-3.0 on the repository (written for code; terms for the images to confirm with the authors) | Masonry walls, complex backgrounds | Small; part of it is already in CrackSeg9k [32] |

### Our own data

| Data | Source | Availability | Access | Format | Size | Licence | Covers | Gaps |
|---|---|---|---|---|---|---|---|---|
| Pilot phone photos (no engineer) | Us, Barcelona, public facades (`spec/features/photo_protocol.md`) | To collect this week | Our own; no people, no addresses | Photo + coin + element tag + crack-width card; labels in a CSV | Target about 30 cracks, 3 shots each (assumption) | Ours | Photo protocol, quality gate, width measurement | No risk labels; Barcelona is not the target context |
| Engineer-labelled phone photos | To collect (Phase 2) | Does not exist | Needs engineering partner and resident consent | Same protocol, plus element, material, pattern, width (mm), Low / Medium / High, on-site rating | Target size: assumption, to set with the partner | Ours; consent rules to write | The real target data | Everything: partner, consent, sites |

### Building data and ground-truth candidates

| Data | Source | Availability | Access | Format | Size | Licence | Covers | Gaps |
|---|---|---|---|---|---|---|---|---|
| Engineers' Syndicate list of 106 buildings, Tripoli | MTV Lebanon, 25 Jan 2026 [8] | Reported in the press; list itself not found | Ask the Order of Engineers, Tripoli (assumption: not public) | Unknown | 106 buildings | Unknown | Buildings engineers already judged at risk: candidate ground truth and photo sites | Access, content and format unknown |
| Municipal evacuation list, Tripoli | Government announcement, 9 Feb 2026 [3][5] | Reported; list not found | Ask the municipality (assumption) | Unknown | 114 buildings | Unknown | Same as above | Same as above; overlap with the 106 list unknown [6] |
| BUET factory survey, Dhaka | Reported by AFP, The Daily Star [16][17] | Reported; raw survey not found | Ask BUET (assumption) | Unknown | Unknown | Unknown | Engineer assessments of factory buildings | Frames, Phase 3; old (2013) |
| Building database for the agent (construction type, footprint) | Not chosen | - | Over MCP (planned) | To define | - | - | Context for the agent | Source, schema and access all open |

## 3. Not usable as data
- Example photos in the deck (slide 8): stock images, authors not identified; their risk labels are a visual guess.
- Case-study figures (deaths, evacuations): context for the problem, not training data.

## 4. Plan, in order
1. **First test on real data (29 Oct):** SDNET2018 through the quality gate (`src/experiments/sdnet_quality.py`). Tests the code, not the thresholds.
2. **U-Net training set:** CrackSeg9k, plus the Dais et al. masonry masks if their image terms allow it.
3. **Pattern gaps:** CODEBRIM for spalling with rust (research only), Darbhanga for brick masonry.
4. **Pilot photos this week:** about 30 cracks on public facades in Barcelona, following `spec/features/photo_protocol.md`. Tests the protocol and gives the quality gate real phone photos.
5. **Engineering partner, now:** the Order of Engineers in Tripoli about the 106-building list, or a volunteer engineers' network. Everything in Phase 2 waits on this.

## 5. Open items
- Consent and data rules for Phase 2: the deck says "photos stay with the household"; labelling needs copies. Write who keeps what, for how long, and how faces and addresses are removed.
- Licences: PHI-Net and CODEBRIM are non-commercial (`spec/decisions.md` D6).
- Confirm the Darbhanga label format and the Dais image terms on download.
