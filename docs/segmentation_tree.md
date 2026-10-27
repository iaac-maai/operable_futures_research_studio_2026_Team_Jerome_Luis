# Problem segmentation tree

Version 3, for 29 Oct 2026 (decisions D16, D21, D25). Numbers in brackets refer to `docs/sources.md`.
Only what the tool works on. What it does not cover is stated once, in `spec/constitution/mission.md` (Out of scope).

![Segmentation tree](../figures/04_segmentation_tree.png)

**How to read it**
- **Paths.** Yellow: the crack path, into the atomic problem. Navy: the building path, into the building risk score. Grey: context that explains why the need exists; not an input.
- **Scales.** S, O, P: the scale of the photo, as in PHI-Net task 1: S structural (the building), O object (the element), P pixel (the crack) [53][55].
- **Evidence.** Under each node: a source number; expert input (studio professor, 27 Oct); measured (our data map); or an assumption still to test.

## Macro
People cannot judge whether the cracks in their ageing buildings are dangerous.
1.12 billion people lived in slums or slum-like conditions in 2022, 24.8% of the world's urban population, 53.6% of urban residents in Sub-Saharan Africa [1]; 90% of slum dwellers live in Africa and Asia [2].

## Meso and micro

### A. Buildings change unwatched (building path, scale S)
These are the inputs of the building risk score (`spec/features/building_score.md`).

| Node | Statement | Evidence |
|---|---|---|
| A1 | Ageing, no maintenance: Tripoli blocks 60 to 70 years old, past their structural life | [3][9] |
| A2 | Floors added on top of the original building | Expert input |
| A3 | Structure or use changed: walls or columns removed, ground floor opened, housing turned into workshops | Expert input |

### B. Residents cannot read the signs (crack path, scales P and O; B6: building path)
| Node | Statement | Evidence |
|---|---|---|
| **B1** | They cannot tell a harmless crack from a structural one: the missing piece is interpretation, not detection | Assumption, to test with a short resident survey |
| **B2** | No record of growth: nobody tracks whether a crack is getting wider, which is what engineers look at above all | Expert input; growth needs repeated measurements [46] |
| **B3** | Cheap phones, no scale: a photo cannot be measured without a scale and at least 3 pixels across the crack | Expert input; [46] |
| **B4** | Is it concrete? Residents cannot tell concrete from other materials | Assumption (team, 27 Oct) |
| **B5** | Which element? Residents cannot tell a column from a beam or a wall | Assumption (team, 27 Oct) |
| B6 | One crack hides the pattern: engineers read the pattern across the whole building | Expert input |

### C. Too few engineers (building path, scale S; C2 and C3: context)
| Node | Statement | Evidence |
|---|---|---|
| C1 | No ranked list of which building to visit first | Assumption, to ask the engineering partners |
| C2 | Reports are not acted on: the collapsed Tripoli building had been reported to a municipal call centre; engineers had not inspected it | [3][7][10] |
| C3 | Backlog: in Tripoli, 114 buildings ordered evacuated (announced 9 Feb 2026); 21 evacuated, 9 under reinforcement by 16 Feb | [3][5][6] |

### D. Data is scarce (context)
| Node | Statement | Evidence |
|---|---|---|
| D1 | Public crack data is mostly bridges, roads and pavement; almost none shows homes in informal areas | Measured: `docs/data_map.md`, 13 datasets checked |
| D2 | No crack is labelled by an engineer with a risk level and a scale | Measured: `docs/data_map.md` |

## Atomic problem (work on first)
**Is this crack dangerous, and is it growing?** One crack in one reinforced concrete element, photographed with a scale and seen again later, gives a level (Low, Medium, High, Expert needed, Retake), its confidence, a one-sentence reason, and whether it grew.
It comes from the crack path: B1 to B5 (bold above).

## Building risk score (what the atomic problem feeds)
**Which building does an engineer visit first?** The crack levels and their growth, the building data (A1 to A3) and the spread of damage across elements (B6) give a priority P1, P2 or P3 (`spec/features/building_score.md`). This answers C1.

## Same tree as Mermaid source

```mermaid
graph TD
  M["Macro: people cannot judge whether the cracks in their ageing buildings are dangerous"]
  M --> A["A. Buildings change unwatched"]
  M --> B["B. Residents cannot read the signs"]
  M --> C["C. Too few engineers"]
  M --> D["D. Data is scarce"]
  A --> A1["A1 Ageing, no maintenance (S)"]
  A --> A2["A2 Floors added on top (S)"]
  A --> A3["A3 Structure or use changed (S)"]
  B --> B1["B1 Harmless vs structural (P)"]
  B --> B2["B2 No record of growth (P)"]
  B --> B3["B3 Cheap phones, no scale (P)"]
  B --> B4["B4 Is it concrete? Can't tell (O)"]
  B --> B5["B5 Which element? Can't tell (O)"]
  B --> B6["B6 One crack hides the pattern (S)"]
  C --> C1["C1 No ranked list of buildings (S)"]
  C --> C2["C2 Reports not acted on"]
  C --> C3["C3 Backlog: 114 buildings"]
  D --> D1["D1 Public data: bridges, roads"]
  D --> D2["D2 No crack labels by engineers"]
  B1 --> AT["Atomic: is this crack dangerous, and is it growing?"]
  B2 --> AT
  B3 --> AT
  B4 --> AT
  B5 --> AT
  AT --> BS["Building risk score: which building does an engineer visit first? P1, P2, P3"]
  A1 --> BS
  A2 --> BS
  A3 --> BS
  B6 --> BS
  C1 --> BS
  classDef crack fill:#F2C14E,stroke:#F2C14E,color:#2F4B7C;
  classDef building fill:#2F4B7C,stroke:#2F4B7C,color:#fff;
  classDef context fill:#a8a7a1,stroke:#a8a7a1,color:#0b0b0b;
  class B,B1,B2,B3,B4,B5,AT crack;
  class A,C,A1,A2,A3,B6,C1,BS building;
  class D,C2,C3,D1,D2 context;
```
