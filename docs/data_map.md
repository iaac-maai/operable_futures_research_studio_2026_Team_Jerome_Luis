# Data map

Version for 29 Oct 2026. Public dataset facts checked on the source pages on 24 and 25 Oct 2026; numbers in brackets refer to `docs/sources.md`.
Raw data is never committed; it lives in `data/` (git-ignored).

**Bottom line.** The concept is cracks in **buildings in slum-like, informal neighbourhoods** (`spec/decisions.md` D14). No public dataset shows those buildings with a crack, a scale reference and an engineer's rating. Public data can only pre-train the detector and the segmenter; the photos we collect with our partners are the real data and the critical path.

## 0. How close each dataset is to the concept

| Fit | Data | Why |
|---|---|---|
| **Target** | Engineer-labelled phone photos from informal neighbourhoods (to collect with the partners) | The exact case: homes, phone photos, coin, engineer rating |
| **High (closest public)** | Haiti 2010 Earthquake Database [41] | Engineers' photos of 183 real buildings in Port-au-Prince and Léogâne, reinforced concrete and concrete-block masonry, each rated light / moderate / severe with crack-based definitions; ratings are per building, after an earthquake, no scale |
| **High (closest public)** | 2015 Nepal Earthquake Building Performance Database [42] | 146 low-rise RC buildings with masonry infill in Kathmandu, photos, rated light / moderate / severe / collapse; per building, no scale |
| Medium | Building Surveys after Earthquakes (Nepal, Ecuador, Taiwan, Korea) [43] | Same kind of per-building engineer surveys with photos; non-commercial |
| Medium | Strathclyde brickwork cracks [44] | 700 brick facade images, crack / no crack; small |
| Medium | PHI-Net [26] | Real damaged buildings after earthquakes, with component and damage labels; not pre-failure cracks; non-commercial |
| Medium | Darbhanga brick masonry [30] | Brick walls, the material of many informal homes; one heritage fort, not homes |
| Medium | Dais et al. masonry masks [31] | Masonry walls with pixel masks; small |
| Medium | Pilot photos, Barcelona old facades | Real buildings and phone photos with a coin; not informal settlements, no engineer |
| Low | METU concrete cracks [36] | Concrete walls of campus buildings; formal buildings, tiles only |
| Low | SDNET2018 walls subset [22] | Concrete walls, but of bridge-related structures; tiles only |
| Low | crack-seg [33], CrackSeg9k [25] | Mostly roads and pavement; generic pre-training for crack pixels only |
| **Off-concept** | CODEBRIM [28], SDNET2018 decks and pavement [22] | Bridges and roads, not buildings |

**Closest public data:** the post-earthquake building surveys from Haiti and Nepal [41][42]. Haiti on our disk: 183 buildings rated by engineers (reinforced concrete: 74 light, 27 moderate, 70 severe; masonry walls: 47 light, 25 moderate, 90 severe) and 4,450 photos, 96% of which pass our quality gate. These surveys show real buildings in dense, poor neighbourhoods, photographed and rated by engineers. Their damage classes map onto our levels: light (no damage or hairline cracks), moderate (wider cracks or spalling), severe (see-through cracks, failure). Limits: one rating per building, not per crack; damage after an earthquake, not slow deterioration; no scale reference.

**Still missing:** per-crack photos with a scale from informal or self-built housing before any disaster. Only our own collection with the partners can give that.

## 0b. What we can train now, and what we cannot (25 Oct 2026)

| Step | Enough data now? | What we have | What is missing | How we get it |
|---|---|---|---|---|
| Find crack pixels (U-Net) | **Yes** | CrackSeg9k and crack-seg: about 13,000 images with crack outlines | Plaster and brick walls of homes are rare in them | Pre-train on these, fine-tune on our own photos |
| Detect cracks (YOLO) | **Yes, for cracks** | Darbhanga crack boxes on brick walls, crack-seg polygons | Boxes for the element (column, beam, slab, wall) | Draw element boxes on our own photos |
| Crack or no crack | **Yes** | METU, Strathclyde, SDNET2018: over 90,000 images | Smooth plaster walls of homes | Our pilot photos |
| Crack pattern (5 classes) | **No** | No dataset uses our five patterns | Labels | Label a few hundred images by hand (number: assumption, to set when we start) |
| Width in mm | **No** | Nothing public has a coin or any scale | Photos with a coin and a known width | Pilot photos with the crack-width card |
| Low / Medium / High | **No** | Haiti and Nepal rate whole buildings, after an earthquake | A rating per crack, by an engineer | Our photos rated by Engineers Without Borders and the structural engineer |
| Proof that the tool works (3 Dec baseline) | **No** | Nothing | Held-out photos rated per crack, plus an engineer's photo-only rating | Same as above; at least 30 High cases (`spec/features/evaluation.md`) |

**In one line:** we can train the "find the crack" step now (hackathon target); the "how dangerous is it" step, and the proof that it works, still depend on our own photos and the engineers (`spec/decisions.md` D15).

## 1. What each pipeline stage needs, and where it comes from

![Data coverage](../figures/05_data_coverage.png)

| Stage | Needs | Covered by | Gap |
|---|---|---|---|
| Quality gate | Phone photos labelled usable / unusable (blur, light, coin visible) | Pilot photos (section 4), planned. First code test on five public sets done (`docs/experiments/2026-10-25_quality_gate_first_test.md`) | Public sets are not phone photos; they test the code only |
| YOLO detector | Bounding boxes for element (column, beam, slab, brick wall) and crack | Cracks only: crack-seg polygons [33], Darbhanga crack boxes [30], CODEBRIM defect boxes [28]; PHI-Net has component type as a class only [26] | No public set has element boxes; draw them on our own photos |
| U-Net segmenter | Pixel masks of cracks | CrackSeg9k [25]; crack-seg polygons converted to masks [33]; Dais et al. masonry masks [31] | Few columns and beams |
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
| SDNET2018 | Utah State University [22] | **Downloaded** (in a browser; scripted download blocked, 403) | Public page | JPEG tiles 256 x 256, crack / no-crack by folder | 56,092 images counted (deck 13,620, wall 18,138, pavement 24,334); 503.8 MB zip | CC BY 4.0 | Concrete bridge decks, walls, pavements | Concrete only; no masks, no scale, no brick, columns or beams; camera tiles, not phone photos |
| CrackSeg9k | Harvard Dataverse, doi:10.7910/DVN/EGIEBY [25] | **Downloaded** (Vol1, MD5 matches; Vol2 not yet) | Public download, scriptable | Vol1: 9,159 greyscale masks at 400 x 400 with soft values (0, 1, 2, 3...), need a threshold; 5,413 of the RGB images; train/test lists; a "Heads" folder (DINO features, not masks) | 9,255 images stated, 9,159 masks found; two zips, 1.55 GB and 1.26 GB | CC0 1.0 | Ten merged sets (largest: CRACK500, Rissbilder, DeepCrack, Volker, GAPS384) plus 1,411 non-crack images; a masonry subset of 240 per [32] | Mostly pavement and concrete; masonry subset not identifiable by file name; no scale |
| Ultralytics crack-seg | Ultralytics, from a 2022 Roboflow "crack" dataset [33][34] | **Downloaded** | Public download (GitHub release), scriptable | YOLO segmentation polygons, 1 class; all images 416 x 416 | 4,029 images (3,717 train, 200 val, 112 test; the YAML comments swap val and test); 96 MB zip; 1 empty label | Public Domain on the dataset page; the YAML file header says AGPL-3.0 (Ultralytics' own licence); licence of the original Roboflow set not checked | Cracks on roads and walls | No scale; no element type; roads and walls mixed |
| PEER Hub ImageNet (PHI-Net) | PEER, UC Berkeley [26][27] | Available | Download page per task; registration not stated | Images with 8 classification tasks (scene, damage state, spalling, material, collapse mode, component type, damage level, damage type) | 36,413 images (as of Nov 2019) | CC BY-NC-SA 4.0 | Post-earthquake structural images | No masks, no width, no scale; non-commercial |
| CODEBRIM | Zenodo record 2620293 [28], CVPR 2019 paper [29] | Available | Open record, licence file must be accepted | Original images, cropped defects with class labels from bounding boxes, classification sets | 36.4 GB in total (cropped set 7.9 GB); image count not stated on the record | Non-commercial research and education only; no redistribution; trained models may not be used commercially | Five concrete defects on 30 bridges: crack, spalling, exposed bars, efflorescence, corrosion stains | Bridges, not homes; no scale; licence blocks any product use |
| Brick masonry cracks, Darbhanga Fort | Singh and Maity, Mendeley Data [30] | **Downloaded** (SHA-256 matches) | Public download, scriptable | YOLO bounding boxes (class x y w h), 1 class; all images 768 x 768; test set has no labels | 4,259 images (3,407 train incl. 203 without cracks, 639 val, 213 test); 363 MB zip | CC BY 4.0 | Superficial cracks in red brick masonry | One heritage structure, not homes; no scale; boxes, not masks |
| METU Concrete Crack Images for Classification | Özgenel, Mendeley Data, doi:10.17632/5y9wdsg2zt.2 [36] | **Downloaded** (SHA-256 matches) | Public download, scriptable; RAR archive | JPEG tiles 227 x 227, Positive / Negative folders | 40,000 (20,000 crack, 20,000 no crack), cut from 458 photos of 4032 x 3024; 241 MB | CC BY 4.0 | Concrete surfaces of buildings on the METU campus, Ankara | Formal campus buildings, not informal homes; no masks, no scale |
| Haiti Earthquake Database (2010) | Sedra, Eberhard, Pujol et al., DataCenterHub, doi:10.4231/D3P843W0H [41] | **Partly downloaded**: the Dropbox zip broke at 85% and cannot resume; 4,450 photos, the drawings and the ratings spreadsheet recovered, each file CRC-checked | Public page, data in a Dropbox folder, no login stated | Spreadsheet (one row per building), photographs, field diagrams | 6,526 photos of 183 structures (170 surveyed in detail: 138 Port-au-Prince, 38 Léogâne); 14.0 GB zip | Not stated on the page: ask the authors before reuse | RC and concrete-block masonry buildings, 1 to 12 floors; damage light / moderate / severe for RC and for masonry walls, defined by crack width | One rating per building; post-earthquake; no scale |
| 2015 Nepal Earthquake Building Performance Database | Shah, Pujol, Puranam, Laughery, DataCenterHub, doi:10.7277/Z82F-0728 [42] | Not downloaded: the archive now only offers Nepal inside a 228 GB zip with Ecuador, Taiwan and Korea (more than our free disk) | DataCenterHub is now a static archive run by the University of Canterbury [45]; download only the Nepal folder from the Dropbox page in a browser | Spreadsheet per building with photos, drawings, KML map | 146 low-rise RC buildings, Kathmandu; photo count not stated | CC BY-SA 3.0 | RC with masonry infill; structural damage light / moderate / severe / collapse, infill damage light / moderate / severe | Per building; post-earthquake; no scale |
| Building Surveys after Earthquakes | Monical, ACI Committee 133, DataCenterHub, doi:10.7277/368Q-T523 [43] | Not downloaded (one 228 GB zip) | Public page | Per-building dimensions, ground motion, photos, figures | Counts not stated | CC BY-NC-SA 4.0 (non-commercial) | 2015 Nepal, 2016 Ecuador, 2016 Taiwan, 2017 South Korea; RC buildings | Damage scheme not stated on the page; non-commercial |
| Brickwork Cracks Dataset | Seyedzadeh, Katsigiannis et al., Zenodo, doi:10.5281/zenodo.8014150 [44] | **Downloaded** (MD5 matches) | Open, Zenodo | 227 x 227 images, Positive / Negative folders | 700 (350 crack, 350 no crack); 9 MB | CC BY 4.0 | Brick facades | Small; no masks, no scale |
| Masonry crack masks, Dais et al. 2021 | GitHub repository [31] | Subset available | Public repository | 224 x 224 images with crack masks | Subset only; count not stated | GPL-3.0 on the repository (written for code; terms for the images to confirm with the authors) | Masonry walls, complex backgrounds | Small; part of it is already in CrackSeg9k [32] |

### Our own data

| Data | Source | Availability | Access | Format | Size | Licence | Covers | Gaps |
|---|---|---|---|---|---|---|---|---|
| Pilot phone photos (no engineer) | Us, Barcelona, public facades (`spec/features/photo_protocol.md`) | To collect this week | Our own; no people, no addresses | Photo + coin + element tag + crack-width card; labels in a CSV | Target about 30 cracks, 3 shots each (assumption) | Ours | Photo protocol, quality gate, width measurement | No risk labels; Barcelona is not the target context |
| Engineer-labelled phone photos | To collect (Phase 2) | Does not exist | Needs engineering partner and resident consent | Same protocol, plus element, material, pattern, width (mm), Low / Medium / High, on-site rating | Target size: assumption, to set with the partner | Ours; consent rules to write | The real target data | Everything: partner, consent, sites |

### Building data and ground-truth candidates

| Data | Source | Availability | Access | Format | Size | Licence | Covers | Gaps |
|---|---|---|---|---|---|---|---|---|
| List of 106 at-risk buildings, Tripoli | MTV Lebanon, 25 Jan 2026 [8] | Reported in the press; list itself not found | No access route identified | Unknown | 106 buildings | Unknown | Buildings engineers already judged at risk: candidate ground truth and photo sites | Access, content and format unknown |
| Municipal evacuation list, Tripoli | Government announcement, 9 Feb 2026 [3][5] | Reported; list not found | Ask the municipality (assumption) | Unknown | 114 buildings | Unknown | Same as above | Same as above; overlap with the 106 list unknown [6] |
| BUET factory survey, Dhaka | Reported by AFP, The Daily Star [16][17] | Reported; raw survey not found | Ask BUET (assumption) | Unknown | Unknown | Unknown | Engineer assessments of factory buildings | Frames, Phase 3; old (2013) |
| Building database for the agent (construction type, footprint) | Not chosen | - | Over MCP (planned) | To define | - | - | Context for the agent | Source, schema and access all open |

## 3. Not usable as data
- Example photos in the deck (slide 8): stock images, authors not identified; their risk labels are a visual guess.
- Kaggle "Crack Dataset" (yatata1, CC BY-SA 4.0, 13.8 GB, "under development") [37]: checked 25 Oct, not used. Its description says it was assembled from existing public crack sets (Rissbilder, the Kaggle "Crack Segmentation Dataset") and UAV infrastructure inspections, so it overlaps CrackSeg9k; mostly concrete and asphalt, off-concept (D14).
- Kaggle "Crack Detection/Classification Dataset" (Apache 2.0 as labelled by the uploader, about 20 GB, v1 Aug 2026) [38]: checked 25 Oct, not used. Nine mixed domains (roads, metal, car bodies, wood, circuit boards, welding, synthetic concrete); only `Wall_Concrete` is near the concept, and it mixes walls with bridges. The sources it aggregates are not named, so provenance and licence cannot be traced.
- Kaggle "Building Crack Detection Dataset" (CC0 as labelled by the uploader, v1 Jul 2026) [39]: checked 25 Oct, not used. Only 51 images (17 hairline, 17 irregular, 17 wide cracks), no uncracked images despite the description, no scale, and no stated source for the photos.
- Kaggle "Satellite Imagery Data for Haiti" (Techsalerator) [40]: checked 25 Oct, not used. A vendor listing: the 1.3 MB download holds another company's real-estate sample files and one image, no satellite imagery; the full data is on request. Satellite images cannot show wall cracks anyway; at most they could locate informal neighbourhoods for the agent.
- Case-study figures (deaths, evacuations): context for the problem, not training data.

## 4. Plan, in order
1. **First test on real data (29 Oct): done** on crack-seg, Darbhanga and SDNET2018 (`docs/experiments/2026-10-25_quality_gate_first_test.md`). It found and fixed a resolution bug in the blur check, and showed that the blur check confuses smooth walls with blur (D12). Tests the code, not the thresholds.
2. **U-Net pre-training:** CrackSeg9k for generic crack pixels, then fine-tune on masonry (Dais et al., if their image terms allow it) and on our own building photos.
3. **Building-like data first:** Haiti and Nepal engineer surveys (real buildings, engineer ratings), then Darbhanga and Strathclyde (brick), PHI-Net (damaged buildings), METU (building concrete). CODEBRIM is off-concept (bridges): use it only if no building photos of spalling with rust turn up.
4. **Find informal-housing crack photos:** post-disaster housing surveys, reconnaissance photo sets, shelter assessments (section 0).
5. **Pilot photos this week:** about 30 cracks on public facades in Barcelona, following `spec/features/photo_protocol.md`. Tests the protocol and gives the quality gate real phone photos.
6. **Engineering partners, now:** Engineers Without Borders and a third-party structural engineer (agreement under construction) for labelled photos, baseline ratings and sign-off. Everything in Phase 2 waits on this.

## 5. Open items
- Consent and data rules for Phase 2: the deck says "photos stay with the household"; labelling needs copies. Write who keeps what, for how long, and how faces and addresses are removed.
- Licences: PHI-Net and CODEBRIM are non-commercial (`spec/decisions.md` D6).
- Confirm the Dais image terms with the authors.
- Confirm the Haiti database licence before using any photo in slides or training (email drafted 25 Oct). The archive's contact is santiago.pujol@canterbury.ac.nz, subject "datacenterhub inquiry" [45]; ask in the same email about the Türkiye 2023 (ACI 133) survey, whose link returned an empty file.
- Nepal 2015: download only the Nepal folder in a browser into `data/raw/nepal2015/`.
- Pick a threshold for the CrackSeg9k soft masks; find the masonry subset's file prefix.
- Ultralytics (YOLO) software is AGPL-3.0 (`spec/decisions.md` D9).

## 6. Local copies (`data/raw/`, never on GitHub)
What is downloaded on Jerome's PC as of 25 Oct 2026. Anyone else downloads from the source (section 2) into the same folder names.

| Folder | Dataset | On disk | Images | Download check |
|---|---|---|---|---|
| `crack-seg/` | Ultralytics crack-seg [33] | 218 MB | 4,029 | Counted in the zip |
| `darbhanga/` | Brick masonry, Darbhanga [30] | 708 MB | 4,259 | SHA-256 matches Mendeley |
| `metu/` | METU concrete cracks [36] | 556 MB | 40,000 | SHA-256 matches Mendeley |
| `sdnet2018/` | SDNET2018 [22] | 629 MB | 56,092 | Downloaded in a browser; file sizes checked |
| `strathclyde-brickwork/` | Brickwork cracks [44] | 19 MB | 700 | MD5 matches Zenodo |
| `crackseg9k/` | CrackSeg9k Vol1 [25] | 1.5 GB | not extracted | MD5 matches Dataverse |
| `haiti2010/` | Haiti Earthquake Database [41] | 12 GB extracted (broken zip deleted) | 4,450 photos; spreadsheet of 183 buildings | Partial zip, every recovered file CRC-checked |
| `nepal2015/` | Nepal 2015 surveys [42] | - | not downloaded | Nepal folder to download in a browser |

Run the real-data test on all of them: `py src/experiments/real_data_quality.py data/raw/crack-seg data/raw/darbhanga data/raw/metu data/raw/sdnet2018 data/raw/strathclyde-brickwork --per-group 2000`.
