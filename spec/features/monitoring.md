# Feature: crack monitoring (`spec/features/monitoring.md`)

Status: specified on 27 Oct 2026; code planned for 26 Nov (`spec/constitution/roadmap.md`). Values are illustrative until calibrated (decision D23).

## Why
Whether a crack is growing is what engineers look at above all (studio professor, 27 Oct). One visit cannot show growth. Cracks also open and close with daily temperature, so long-term change can only be told apart from that movement with repeated measurements [46].

## How
1. **Crack ID.** Every crack gets an ID made of the building ID and a crack number (for example `B014-C03`), written on the scale card in every photo of that crack.
2. **Marker stickers.** At the first visit, two round stickers are placed on either side of the crack, about 5 to 10 cm apart (assumption), and stay on the wall. This is a low-cost version of the marker technique in the reference thesis, which tracks markers fixed on both sides of a crack between inspections [46].
3. **Recheck date** from the crack level (matrix v2 next steps): Low in 6 months, Medium in 1 month. High and Expert needed go to an engineer at once.
4. **Revisit.** The app shows the previous photo as a faint overlay so the same view is taken (same distance and angle), with the scale card; a burst of photos; at a similar time of day as the first visit, to limit the effect of temperature [46].
5. **Measure** the crack width and the distance between the two stickers, each with its uncertainty: ±1 pixel at the measured pixel size [46].
6. **Growth** counts only when the increase in width or in sticker distance is larger than the sum of the two visits' uncertainties. Only then the warning sign `growing` is set: +1 crack level (matrix v2), which also raises the building risk score through the worst crack (`spec/features/building_score.md`).
7. **Ask** the resident whether doors or windows have started to stick (warning sign `sticking_openings`).
8. **Crack not found again** or stickers missing: growth is recorded as unknown, the previous level stays, and the case is marked for the engineer's review; new stickers are placed.

## Limits
Phone photos only show clear growth of several pixels. Movements of micrometres, as measured in the thesis with marker detection and digital image correlation [46], are out of reach.

## Tests (when coded)
- Growth smaller than the combined uncertainty is not growth; growth larger than it sets `growing`.
- The recheck date follows the level; High and Expert needed are never scheduled for a later recheck instead of an engineer.
- A missing crack or missing stickers gives "growth unknown", keeps the previous level and flags the engineer.
