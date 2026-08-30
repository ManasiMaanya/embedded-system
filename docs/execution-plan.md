# Execution plan

**Who runs this:** you (Windows `cmd`). You can edit this file: set **Ready?**, paste what you saw, change the order.

The agent must add a **script you can run yourself** (`scripts\<name>.cmd` or `python sim\...` wrapped by a `.cmd`) and a **row in the table below** whenever a phase becomes runnable. Do not leave verification as `python -c` only.

| Doc | Role |
|-----|------|
| This file | What **you** type, expected output, Ready? |
| [implementation-plan.md](implementation-plan.md) | Phases, dependencies, checklists |
| [buy.md](buy.md) | Parts photos + specifications |
| [phase-execution-status.md](phase-execution-status.md) | Live board (agent updates before commit) |
| [mathematics.md](mathematics.md) | `T(v)` equations |
| [architecture.md](architecture.md) | L0–L5 |
| [electronics-components.md](electronics-components.md) | How ADC, MQ-2, pots, OLED, RGB work |
| [circuit-diagram.md](circuit-diagram.md) | Schematics Fig A / Fig B + netlist |

This workspace opens `.md` in Cursor’s built-in Markdown Preview (`vscode.markdown.preview.editor`). Reopen `hardware.md` after reload. **Ctrl+Shift+V** = preview tab; **Ctrl+K V** = preview beside source. Browser fallback: `scripts\preview-docs.cmd`.

Shared helpers (use these; do not copy-paste lookup logic):

| Script | Role |
|--------|------|
| `scripts\_lib.cmd` | Sets `REPO`, `PY`, `PIO`, `PIO_PROJECT`. Called by the others. |
| `scripts\pio.cmd` | Any PlatformIO command in `firmware\` (or `PIO_PROJECT`). |
| `scripts\p0.cmd` | Sim; extra args → `sim\adaptive_threshold.py` (`--help`). |
| `scripts\p1-*.cmd` | Thin aliases of `pio.cmd` / pip install. Extra args forwarded. |
| `scripts\gen-pin-schematic.cmd` | Rebuild `docs/images/circuit/pin-connection-schematic.svg` |

---

## 1. What you run (by phase)

Edit the **Ready?** column when you have actually run it.

| Phase | Ready? | You execute | Expected |
|-------|--------|-------------|----------|
| **P0** Sim + closed form | **yes** | `scripts\p0.cmd` | Closed form; `sim\out\math_summary.txt`; MOD→SAFE at `d=200`; CSV under `sim\out\`. Other d: `scripts\p0.cmd --delta 180` |
| **P1** Install PlatformIO | no | `scripts\p1-install-pio.cmd` | `pip` installs `platformio`; then **open a new cmd** |
| **P1** Build firmware | no | `scripts\p1-build.cmd` or `scripts\pio.cmd run` | Compile of `firmware/` succeeds *(needs PIO; first run downloads ESP32 platform)* |
| **P1** Upload + blink | no | `scripts\p1-upload.cmd` | Upload OK; on-board LED blinks *(needs ESP32)*. Port: `scripts\p1-upload.cmd --upload-port COM3` |
| **P1** Serial | no | `scripts\p1-monitor.cmd` | 115200 CSV header then rows *(needs ESP32)*. Port: `scripts\p1-monitor.cmd --port COM3` |
| **P2–P4** Bench bring-up | no | same upload/monitor; follow plan checklists | OLED / pots / RGB per [implementation-plan.md](implementation-plan.md) |
| **P5** Dry labs | no | pots + monitor; save CSV yourself | Tables vs sim |
| **P6** MQ-2 | no | set `DRY_POT` 0, then upload | Air-only SAFE on speed sweep |
| **P7** Optional | no | *(script when that lab is defined)* | Fan/IPA notes; no petrol |
| **Docs preview** | **yes** (agent) | `scripts\preview-docs.cmd` | Browser opens architecture. Other file: `scripts\preview-docs.cmd docs\overview.md`. HTML only: `scripts\preview-docs.cmd docs\overview.md --no-open` |

---

## 2. P0 — run now (no board)

From repo root:

```
scripts\p0.cmd
```

You should see the closed-form block (`T_mod(v) = 180 + 0.8 * v`, `v_enter_mod = 25`, `v_leave_mod = 75`) then tables A and B. If `python` is not on PATH, install Python 3 and retry.

To change `T_0` or `K`: edit `firmware\src\math_params.h` **and** `sim\adaptive_threshold.py`, then run `scripts\p0.cmd` again. Flags: `scripts\p0.cmd --help`.

---

## 3. Order (your plan)

You can rewrite this list.

1. `scripts\p0.cmd` — math + CSV + `sim\out\math_summary.txt`  
2. BUY parts — photos/specs in `docs/buy.md`; ticks in the implementation-plan BUY table  
3. `scripts\p1-install-pio.cmd` (once), new cmd, then `scripts\p1-build.cmd`  
4. Plug in ESP32: `scripts\p1-upload.cmd` — blink  
5. OLED → pots → FSM (P2–P4) + `scripts\p1-monitor.cmd`  
6. Dry tables (P5)  
7. MQ-2 (P6); optional P7  
8. P8: paste `math_summary.txt` + bench tables into the report  

Do not start P6 before P5. Do not test with petrol.

---

## 4. Agent rule (when implementing)

For each new runnable phase:

1. Add or extend a script under `scripts/` (`.cmd` from repo root).
2. Set **Ready?** to **yes** only if you (the agent) ran it successfully here; otherwise **no** and say so.
3. Add/update the table row: command + expected output.
4. Refresh [phase-execution-status.md](phase-execution-status.md).

You (the student) may set Ready? to **yes** after you run it on your machine, even if the agent had **no**.
