# Hardware reference

Single tank MQ-2 + speed potentiometer. Pins must match `firmware/src/pins.h`. Shop photos and URLs: `docs/buy.md`. Abbreviations: `docs/abbreviations.md`. L3 numbers: `firmware/src/math_params.h` (not copied ad hoc in `main.cpp`).

## BOM — what each part is for

| ID | Item | Qty | Pin / connection | Use in this project |
|----|------|-----|------------------|---------------------|
| B1 | ESP32 DevKit V1 30-pin | 1 | USB + breadboard | Runs the loop: ADC, `T(v)`, FSM, OLED, RGB, buzzer, serial CSV. **No Wi-Fi.** MCU power = USB only. |
| B2 | USB **data** cable | 1 | PC ↔ ESP32 | Flash (`p1-upload`) and 115200 CSV (`p1-monitor`). Charge-only cable = P1 fails. |
| B3a | 10 kΩ linear pot **speed** | 1 | Ends 3V3/GND, wiper **GPIO 33** | Simulated vehicle speed `v` = 0–120 km/h. Moves `T_mod(v)` and `T_high(v)` on the OLED. |
| B3b | 10 kΩ linear pot **dry vapor** | 1 | Ends 3V3/GND, wiper **GPIO 34** | Fake vapor index `d` for P3–P5. **Remove** before MQ-2 uses GPIO 34. |
| B4 | SSD1306 128×64 I²C OLED | 1 | VCC 3V3, GND, SDA **21**, SCL **22** | Always show `d`, `v`, `T_mod`, `T_high`, state. Address `0x3C` (try `0x3D`). |
| B5 | RGB LED + 3× ~220 Ω | 1 | R **25**, G **26**, B **27**, common **GND** | Green SAFE, yellow (R+G) MOD, red HIGH. Common **cathode**, active high. |
| B6 | Active buzzer | 1 | `+` **GPIO 13**, `−` GND | Off / intermittent (`millis`) / continuous. Not a passive piezo. |
| B7 | Tactile 6×6 | 1 | GPIO **4** to GND | Recapture baseline `N_0` (pull-up; press = LOW). |
| B8 | Breadboard + Dupont | 1 | — | All wiring. Jump split power rails. |
| B9 | MQ-2 module (**one**) | 1 | Heater **5 V** (B10), AO → **34** after DMM | Tank-zone vapor **index** (counts, not ppm). Ignore **DO**. No petrol. |
| B10 | 5 V ≥1 A adapter | 1 | MQ-2 VCC + **common GND** | Heater only (~150 mA). Never ESP32 3V3. |
| B11 | DMM | 1 | See `docs/buy.md` B11 | **DC V** rails/AO/wiper; **Ω** resistors/pots; **diode** RGB; **continuity** GND/button. |
| B12 | USB fan | 0–1 | Own USB 5 V | Optional P7 airflow at MQ-2, not at the ESP32 plug. |
| Extra | 2× 10 kΩ | 0–2 | AO divider mid → 34 | Only if AO **> 3.3 V**. |
| — | On-board LED | 1 | GPIO **2** | Warm-up blink (P1). |

---

## Use by part (bench)

### B1 — ESP32 DevKit

**Use:** The only MCU. Implements L1–L5: average ADC, map speed, subtract baseline, compute `T_mod`/`T_high`, hysteresis FSM, drive HMI, print CSV.

**Do:** USB power. Sit on the breadboard so both header rows are reachable. PlatformIO board `esp32dev`.

**Do not:** 5 V on GPIO. Wi-Fi. A second MCU.

**DMM:** DC V **3V3 vs GND** ≈ 3.3 V. Continuity **GND** to breadboard GND.

### B2 — USB data cable

**Use:** Power the DevKit **and** the UART so you can upload and watch `t_ms,raw,baseline,delta,speed,Tmod,Thigh,state`.

**Do:** Match micro-USB vs USB-C to the board. Confirm Windows shows a COM port.

**Do not:** Charge-only cables.

### B3a — Speed pot (GPIO 33)

**Use:** Independent variable for the academic claim: as `v` rises, thresholds rise, so a fixed leak `d` can leave MOD toward SAFE.

```
3V3 ----[speed pot]---- GND
              |
           GPIO 33
```

Firmware: `v_kmh = (adc / 4095) * 120`. Label the knob **speed**.

**DMM:** Ω between **ends** ≈ 10 kΩ. DC V on **wiper vs GND** sweeps ~0–3.3 V.

### B3b — Dry vapor pot (GPIO 34)

**Use:** Stand-in for MQ-2 AO during P3–P5 so you can set `d` without gas. Same 3-terminal wiring as speed, wiper on **34**.

**Do not:** Leave this pot on GPIO 34 when MQ-2 AO is connected.

### B4 — OLED

**Use:** Prove `T(v)` live. Four numbers every update, not a lone “Safe”.

| OLED pin | ESP32 |
|----------|--------|
| VCC | 3V3 |
| GND | GND |
| SDA | GPIO 21 |
| SCL | GPIO 22 |

**DMM:** DC V on VCC ≈ 3.3 V if the glass is black.

### B5 — RGB + 220 Ω

**Use:** Same state as OLED/buzzer without reading text from across the room.

| Colour | GPIO | State |
|--------|------|--------|
| Green | 26 | SAFE |
| Red + green | 25 + 26 | MOD (yellow) |
| Red | 25 | HIGH |
| Blue | 27 | unused / off unless you add a colour |

Each colour → **220 Ω** → GPIO. Common cathode → **GND**.

**DMM:** Ω on each 220 Ω. **Diode** mode to confirm common cathode (`docs/buy.md` B11).

### B6 — Active buzzer

**Use:** Hear MOD vs HIGH. SAFE silent. `+` → GPIO 13, `−` → GND. Cadence from `millis()`, not `delay()`.

**DMM:** Continuity `−` to GND. Optional DC V on `+` when HIGH (~3.3 V).

### B7 — Calibrate button

**Use:** After warm-up or if clean-air drifted: press to set `N_0` so `d = max(0, N − N_0)`. GPIO 4 — GND. Internal pull-up.

**DMM:** Continuity **only while pressed**.

### B8 — Breadboard + Dupont

**Use:** Hold B1 and all modules. M–M for holes; M–F for OLED/MQ-2 headers.

**DMM:** Continuity of jumpers; jumper **split** red/blue rails if the board is cut in the middle.

### B9 — MQ-2 (P6)

**Use:** Real tank-zone **index** on AO. Firmware treats AO as ADC counts, not petrol ppm. Heater VCC = **B10 5 V**. AO → GPIO 34 **after** DMM. Leave DO unconnected.

**Never:** Petrol. AO and B3b on GPIO 34 together. Heater on ESP32 3V3.

**DMM (required):** DC V heater VCC ≈ 5 V. DC V **AO vs GND ≤ 3.3 V**. Continuity GNDs.

### B10 — 5 V adapter

**Use:** MQ-2 heater supply only. Tie **GND** to ESP32 GND. DevKit stays on USB.

**DMM:** DC V adapter output ≈ 5.0 V (no load, then with MQ-2). **Not** AC on the wall pin.

### B11 — DMM

**Use:** Bring-up and P6 safety. Dial guide and unused ranges: **`docs/buy.md` → How we use the multimeter**.

| Dial | Hardware use |
|------|----------------|
| DC V 20 V | 3V3, 5 V brick, pot wiper, MQ-2 AO |
| Ω | 220 Ω, 10 kΩ pot ends, divider |
| Diode | RGB common cathode vs anode |
| Continuity | GND net, button, Dupont |

Skip AC V, amps, hFE, 10 A jack.

### B12 — USB fan (optional)

**Use:** P7 only — blow air at MQ-2 while the **speed pot** still sets `T(v)`. Qualitative plant story, not a speed sensor.

### Extra — 10 kΩ divider

**Use:** If AO > 3.3 V: two equal resistors, AO at the top, GND at the bottom, **midpoint → GPIO 34**. Measure DC V at the midpoint again.

### On-board LED (GPIO 2)

**Use:** P1 blink / warm-up. No extra part.

---

## Pin map (ESP32 DevKit V1)

| Function | GPIO | ADC | Use |
|----------|------|-----|-----|
| MQ-2 AO **or** dry vapor pot | 34 | ADC1_CH6 | Input-only. One source only. |
| Speed pot wiper | 33 | ADC1_CH5 | `v` 0–120 km/h |
| OLED SDA | 21 | — | Display data |
| OLED SCL | 22 | — | Display clock |
| RGB red | 25 | — | HIGH / yellow |
| RGB green | 26 | — | SAFE / yellow |
| RGB blue | 27 | — | Spare |
| Buzzer | 13 | — | MOD/HIGH sound (JTAG strap, F-010) |
| Recalibrate | 4 | — | Baseline button |
| On-board LED | 2 | — | Warm-up blink |

OLED address `0x3C` (try `0x3D` if needed).

## Power

- ESP32 from USB (B2).
- MQ-2 **heater VCC = 5 V** (B10), not ESP32 3V3 (~150 mA heater).
- Common ground: USB, 5 V brick, pots, OLED, MQ-2.
- Measure MQ-2 AO with B11 at 5 V heater power. If AO can exceed 3.3 V, Extra divider before GPIO 34.

## MQ-2 vs dry vapor pot

Never parallel MQ-2 AO and B3b on GPIO 34.

- **P6 sensor run:** B9 AO → GPIO 34 (`DRY_POT 0`).
- **P3–P5 dry run:** B3b wiper → GPIO 34 (`DRY_POT 1`).

## Adaptive constants (tune after tests)

Edit **`firmware/src/math_params.h` and `sim/adaptive_threshold.py` together**. Cite `docs/mathematics.md`.

Default: `T_mod = 180 + 0.8 v`, `T_high = 420 + 1.2 v` (ADC delta counts). Replace after Experiment 1–2 in `tests.md`.
