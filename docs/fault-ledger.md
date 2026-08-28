# Fault ledger

Detected issues in this **ESP32 tank-vapor / adaptive `T(v)`** repo. The agent **logs** here. It **does not correct** a fault unless you name the **ID(s)** and explicitly approve the fix.

## How to approve

In chat, write the IDs and that they may be fixed, for example: `Approve F-001 F-008`.

Until then: do not patch firmware, sim, or docs “while you’re at it.” New findings get a new ID (`F-NNN`), status `open`.

## Status values

| Status | Meaning |
|--------|---------|
| `open` | Logged, not fixed |
| `approved` | User named this ID; fix may proceed |
| `fixed` | Change landed; note the files |
| `wontfix` | User declined or accepted as limitation |
| `verify` | Fix applied; waiting for bench or sim re-run |

## Open / active

| ID | Sev | Where | Fault | Status |
|----|-----|--------|--------|--------|
| F-001 | High | `firmware/src/main.cpp` state machine; `sim/adaptive_threshold.py` `next_state` | Leaving **HIGH** has no band on `T_high`. As soon as `d < T_high` the code takes MOD if `d ≥ T_mod`. At the HIGH trip, RGB/buzzer can **chatter** HIGH↔MOD. | open |
| F-002 | High | same | Hysteresis only tests `d < T_mod - H` to go **SAFE**. If state is **HIGH** and `d` sits in `(T_mod - H, T_mod)`, neither HIGH, MOD, nor SAFE fires → **stuck HIGH**. Same logic in the sim. | open |
| F-003 | Med | `firmware/src/main.cpp` | Calibrate path uses `delay(30)` and a **blocking** `while` on the button. Loop (buzzer `millis`, OLED, serial) freezes until release. Skill says no blocking delays on the alarm path. | open |
| F-004 | Med | `firmware/src/main.cpp` warmup | Warm-up uses `delay(20)` each pass. Harmless for demo length; still blocks ADC/serial cadence vs the rest of the loop. | open |
| F-005 | Med | `firmware/src/pins.h` | `DRY_POT` defaults to `1` (2 s warm-up). A P6 MQ-2 flash that forgets `DRY_POT 0` **skips heater settle** and will baseline too early. | open |
| F-006 | Med | `firmware/src/main.cpp` | OLED `begin` only at `0x3C`. Modules at `0x3D` fail with a serial line and a blank screen; no retry. | open |
| F-007 | Low | `sim/adaptive_threshold.py` | Comment on the speed sweep still says **d=250**; the run uses **200**. Docs/CSV names are 200. | open |
| F-008 | Low | firmware vs sim serial | Firmware `Alert` includes **Warmup=0**. Sim never emits state 0. Logs are not 1:1 during the first seconds on hardware. | open |
| F-009 | Low | `hardware.md` / RGB | Firmware assumes **common-cathode, active high**. A common-anode LED will invert colours with no detection. | open |
| F-010 | Info | GPIO 13 buzzer | ESP32 **GPIO 13** is MTCK (JTAG). Fine for many DevKits; can surprise if JTAG is in use. | open |
| F-011 | Info | Cursor IDE (not this repo) | In-tab Markdown Preview blank; `markdown.showPreviewToSide` / MPE do not show a webview on Cursor **3.17.21** Windows. Browser preview works. Paste-ready report: `docs/cursor-bug-markdown-preview.md`. | open |

Severity: **High** = wrong alarm behaviour; **Med** = bring-up or demo risk; **Low** / **Info** = docs, ports, assumptions.

## Closed

_(none yet)_

## Template (new rows)

```
| F-0xx | Sev | file / subsystem | One-sentence fault + how you know | open |
```

When fixing after approval, move the row to **Closed** with: date, files touched, one line on the change. Do not delete IDs.
