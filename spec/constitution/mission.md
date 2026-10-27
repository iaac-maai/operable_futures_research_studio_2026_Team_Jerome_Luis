# Mission

Second Look is a human-in-the-loop triage system for cracks in reinforced concrete. It checks the photo and the material, finds and measures the crack in millimetres, classifies its pattern, and applies written, auditable risk rules, returning a level with its confidence. An engineer confirms every High and every referral, and their corrections retrain the models. It never issues a safety clearance.

## Problem
In dense, ageing neighbourhoods, residents see cracks every day but cannot tell a harmless one from a sign of structural failure.
Engineers are too few to inspect every building. Tripoli, February 2026: two blocks collapsed on 8 February (14 to 15 dead, AFP and Reuters),
and 114 buildings were ordered evacuated. Rana Plaza, Dhaka, 2013: cracks were visible the day before the collapse.

## Mission
Give residents and field workers a fast, cheap early-warning triage from a phone photo, and give scarce engineers a ranked list of which buildings to visit first.

## Scope
Cracks in reinforced concrete elements (walls, columns, beams, slabs). Other materials go to an engineer (`spec/decisions.md` D17). The unit of analysis is the building, seen at three scales (S, O, P) and over time (D21).

## Users
- Residents of old buildings, field workers and community leaders: take the photo and receive a level, a reason and a next step.
- Structural engineers: review every High and every referral, confirm or correct it, and so improve the models (`spec/features/pipeline.md`). Engineers and municipalities also use the ranked list to decide where to inspect first.

## Success (works, used, matters)
- Works: beats the non-AI baseline (an engineer's visual check) on held-out, engineer-labelled photos.
- Used: runs inside a real workflow and people trust it.
- Matters: impact indicators move. Indicator, unit, baseline, target and evidence are still to be defined (see `roadmap.md`).

## Failure (stop condition)
We stop or redesign if the tool misses High cases that engineers would flag.

## Out of scope
Permits, legal clearances, foundation or rebar assessment, any claim a surface photo cannot support. Materials other than reinforced concrete are not assessed (they are referred).
