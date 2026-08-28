# Phase execution status

Live board for this ESP32 `T(v)` project. **Update this file before every git commit** (and whenever a phase starts, finishes, or blocks). Checklists live in `docs/implementation-plan.md` — tick those in the same change. Do not mark a phase `done` unless its **exit criterion** in the plan is met.

| Field | Value |
|-------|--------|
| Last updated | 2026-08-28 (commit: scripts + BUY links) |
| Current phase | **P1 toolchain** (blocked on PIO + ESP32) after **P0 done** |
| Next action | You: BUY ESP32 + two pots. Run `scripts\p1-install-pio.cmd`, new cmd, then `scripts\p1-build.cmd`. |
| Blockers | `pio` not on PATH. No MCU verified. F-001, F-002 open. Cursor in-tab Markdown preview still unreliable (F-011). |

Definitions: `not_started` · `in_progress` · `blocked` · `done` · `skipped`

## Board

| ID | Name | Status | Exit met? | Notes |
|----|------|--------|-----------|--------|
| BUY | Parts | `not_started` | no | Parallel with P0. Catalog + shop URLs: `docs/buy.md` |
| P0 | PC sim + closed-form `T(v)` | `done` | yes (code/CSV) | Sim runs; `v_leave(200)=75` km/h. Screenshot + hand derivation left for P8 |
| P1 | Toolchain + blink | `blocked` | no | Need PlatformIO install + ESP32. Use `scripts\p1-install-pio.cmd` |
| P2 | OLED I²C | `not_started` | no | Source assumes `0x3C` (F-006) |
| P3 | ADC pots + `T(v)` on OLED | `not_started` | no | Source drafted; needs two pots |
| P4 | Alarm FSM + HMI | `not_started` | no | Source drafted; F-001/F-002 still open |
| P5 | Dry two-pot labs | `not_started` | no | Depends on P4 + P0 |
| P6 | MQ-2 5 V + air sweep | `not_started` | no | `DRY_POT` still `1` (F-005) |
| P7 | IPA / fan / tune `K` | `not_started` | — | Optional; may `skipped` |
| P8 | Report + viva | `in_progress` | no | Overview, architecture, math, plan exist (ASCII `T_mod` so editor is readable); plots/demo incomplete |

## Current work

- P0 complete including `sim/out/math_summary.txt`.
- P1 **blocked** here: `pio` missing. Scripts updated to fall back to `python -m platformio`.
- Docs use firmware names (`T_mod`, `T_MOD_0`) instead of LaTeX so they read in the source editor. Browser preview: `scripts\preview-docs.cmd`.
- Scripts share `scripts\_lib.cmd`; firmware goes through `scripts\pio.cmd`; P0/preview take extra CLI args.

## Next action

1. **You (this week):** buy from `docs/buy.md` links (B1 DevKit V1 30-pin + two B10K pots first).
2. `scripts\p1-install-pio.cmd` → new Command Prompt → `scripts\p1-build.cmd`.
3. Plug board in → `scripts\p1-upload.cmd` (P1 blink). Then P2 OLED.

## Execution log

| Date | What changed |
|------|----------------|
| 2026-08-28 | Board created. P0 sim + math_params + architecture/math docs. P1–P7 not started on hardware. P8 docs started. Faults F-001–F-010 open. |
| 2026-08-28 | `docs/execution-plan.md` + `scripts\p0.cmd` (ran OK) and P1 pio wrappers. Skill: always ship a user-editable script + execution-plan row. |
| 2026-08-28 | Started P1 path: `p1-install-pio.cmd`; p0 writes `math_summary.txt`. Agent machine has no `pio`. |
| 2026-08-28 | First repo snapshot: skill, architecture/math/plan, firmware + sim, `scripts\*.cmd`. Docs switched to ASCII `T_mod` (Cursor preview does not typeset LaTeX). |
| 2026-08-28 | Scripts made reusable: `_lib.cmd`, `pio.cmd`, `%*` forwarded; sim/preview `--help`. |
| 2026-08-28 | BUY catalog: `docs/buy.md` + photos under `docs/images/buy/`; plan table IDs B1–B12. |
| 2026-08-28 | Shared `scripts\_lib.cmd` / `pio.cmd`; sim and preview CLI flags. Shop URLs for B1–B12 in `docs/buy.md`. |

When logging a new row, also set **Last updated**. If a phase moves to `done`, tick the matching boxes in `docs/implementation-plan.md`.
