# Firmware patterns

Project root: `firmware/`. Layers: `docs/architecture.md`. Equations: `docs/mathematics.md`. L3 numbers: `src/math_params.h` (must match `sim/adaptive_threshold.py`).

## OLED (adaptive study)

Always show four numbers, not just “Safe”:

```
Tank vapor
d=###  v=## km/h
Tm=### Th=###
SAFE | MOD | HIGH
```

If the display cannot make the threshold change obvious, the project has failed its own brief.

## Serial CSV (2 Hz)

```
t_ms,raw,baseline,delta,speed,Tmod,Thigh,state
```

`state`: 0 warmup, 1 safe, 2 moderate, 3 high.

Paste into Excel: scatter **speed vs T_mod**, and **delta vs T_mod** at a few fixed speeds. Predicted rows: `scripts\p0.cmd` → `sim/out/`. Keep sim constants identical to `math_params.h`.

## Loop

```
setup: pins, OLED, ADC_11db, WARMUP timer
loop:
  raw = avg(GPIO34)
  v = map(avg(GPIO33) → 0..120)
  Tmod, Thigh = T0 + K * v
  if WARMUP: blink; return
  on leaving WARMUP or button: baseline = raw
  delta = max(0, raw - baseline)
  state from delta vs Tmod/Thigh + hysteresis
  RGB, buzzer (millis), OLED, serial
```

Dry-pot mode: shorter warm-up (e.g. 2 s) is allowed if MQ-2 heater is disconnected; keep a `DRY_POT` constant so viva knows which build was flashed.

## Commands

Generic (pass any PlatformIO args; extra flags after the verb):

```
scripts\pio.cmd run
scripts\pio.cmd run -t upload
scripts\pio.cmd device monitor
scripts\p1-upload.cmd --upload-port COM3
```

Phase aliases (`p1-build` / `p1-upload` / `p1-monitor`) call `pio.cmd`. Same verbs work if `pio` is already on PATH inside `firmware\`.
