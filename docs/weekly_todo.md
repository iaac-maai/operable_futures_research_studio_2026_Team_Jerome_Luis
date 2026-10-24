# Weekly to-do

Newest week on top. Every Monday: tick what is done, move what is not into the new week, add the new week from `spec/constitution/roadmap.md`.
Owner: J = Jerome, L = Luis, C = coding agent (Claude). Fill in the blanks.
**Every week:** update the deck for Thursday's studio presentation, in the layout set on 26 Oct.

---

## Week 1: 26 Oct to 1 Nov (studio Thu 29 Oct: tree, data map, repo, first real-data test)

### Done
- [x] Segmentation tree, data map, repo, AGENTS.md (C, 24 to 25 Oct)
- [x] First test on real data: quality gate on crack-seg, Darbhanga, SDNET2018 (C, 25 Oct)
- [x] Plan aligned with the syllabus dates (C, 25 Oct)

### Before Thursday 29 Oct
- [ ] Open the repo on GitHub and check that the figures show in the docs and README (__)
- [ ] Read `docs/experiments/2026-10-25_quality_gate_first_test.md`; be able to explain the two findings: the resolution bug and the smooth-wall blur problem (J + L)
- [ ] Mon 26 Oct: set the deck layout and style once, as a template for every weekly presentation (feedback: it looks too AI-generated); restyle the figures to match (J + L, C)
- [ ] Thursday's slides in the new layout: tree, data map, first real-data test and its two findings (J + L)
- [ ] Decide who presents what on Thursday (J + L)

### Engineering partners (send early, replies take time)
- [ ] Send a dated request to Engineers Without Borders: rate about 150 to 200 crack photos Low / Medium / High, at least 30 High, by 20 Nov; put a coin next to cracks in their own inspection photos (__)
- [ ] Same request to the third-party structural engineer; confirm the agreement (__)

### Photos
- [ ] Set up the iPhone: Most Compatible (JPEG), grid on, Camera location off (J + L)
- [ ] Print the crack-width card (C makes the PDF)
- [ ] Width test at the desk: about 36 photos, 6 line widths x 3 distances x 2 lights (__)
- [ ] Pilot: about 30 cracks on public facades, 3 shots each, plus about 6 deliberately bad shots (`spec/features/photo_protocol.md`) (J + L)
- [ ] Run `py src/pilot/prepare.py <phone folder> data/pilot/photos` and fill `data/pilot/labels.csv` (__)

### Decisions to take
- [ ] One material for the hackathon beta: brick or concrete walls (J + L)
- [ ] Building-data source for the first MCP connection (due 12 Nov) (J + L)
- [ ] Five or six crack patterns (`spec/decisions.md` D1) (J + L)

### Midterm (submit Wed 5 Nov, present Thu 6 Nov)
- [ ] Outline of the midterm deck in the new layout, reusing the content of figures 01 to 09 (__)
- [ ] Problem & data brief: answer the syllabus questions (where is the problem, what data, what AI can generate, limits, who is affected) (__)

### Repo (coding agent)
- [ ] Crack-width card PDF and one-page field sheet for the pilot (C)
- [ ] Sample-size rule ("rule of three") in `spec/features/evaluation.md` (C)

---

## Coming up (from the roadmap)
- **Week 2, 2 to 8 Nov:** midterm (5/6 Nov); pilot photos labelled; quality gate retuned on phone photos; label mapping to the patterns.
- **Week 3, 9 to 15 Nov:** first feature with tests against the baseline (coin + width); first MCP connection attempt (12 Nov).
- **Week 4, 16 to 20 Nov:** hackathon, beta version end to end on pilot photos.
