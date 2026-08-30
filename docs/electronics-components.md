# Electronics component overview

How each part in this capstone **works electrically**, how it talks to the ESP32, and what we **do not** claim. **Connection schematic:** `docs/circuit-diagram.md`. Pin numbers and bench **use**: `.cursor/skills/esp32-fuel-vapor/hardware.md`. Shop IDs B1–B12: `docs/buy.md`. Symbols: `docs/abbreviations.md`. Why `T(v)`: `docs/architecture.md` and `docs/mathematics.md`.

This is a **bench prototype**, not an automotive ECU. One MQ-2 at the tank zone. No petrol.

---

## 1. System as a circuit (L0)

Two analog channels and one digital display/alarm cluster share a **common GND**. Two **separate** 5 V-class sources:

```
  PC USB 5 V ---- USB-UART ---- ESP32 3.3 V LDO ---- 3V3 rail
                                      |                 |
                                      |            pots, OLED VCC, GPIO
                                      |
  Wall 5 V adapter ---------------- MQ-2 heater VCC
                                      |
                                   common GND
```

| Domain | Voltage | Who lives here |
|--------|---------|----------------|
| Logic | 3.3 V | ESP32 GPIO, ADC, OLED, pots, RGB, button, buzzer `+` |
| Heater | 5 V | MQ-2 heater only |
| USB | 5 V into DevKit | MCU + UART; **not** the MQ-2 heater |

GPIO is **not 5 V tolerant**. Anything that can exceed 3.3 V (typical MQ-2 AO when the module is on 5 V) needs a DMM check and, if needed, a resistor divider.

---

## 2. ESP32 DevKit V1 (B1)

**What it is:** A breakout for the **ESP32-WROOM-32** SoC: dual-core 32-bit Xtensa, up to 240 MHz, on-chip Wi-Fi/Bluetooth (unused here), 12-bit SAR ADC, I²C, UART.

**What we use**

| Block | Role in this project |
|-------|----------------------|
| ADC1 | GPIO 34 vapor index, GPIO 33 speed. Attenuation 11 dB so ~0–3.3 V maps to 0–4095. |
| I²C | Master for SSD1306 (SDA 21, SCL 22). |
| GPIO out | RGB 25/26/27, buzzer 13, on-board LED 2. |
| GPIO in | Button 4 with internal pull-up. |
| UART | USB-UART (CP2102 or CH340) at 115200 for CSV. |
| LDO | 5 V USB → 3.3 V for the chip and 3V3 pin. **Limited current** — do not hang the MQ-2 heater here. |

**What we do not use:** Wi-Fi, BLE, ADC2, SPI OLED, DAC as the vapor signal.

**Input-only pins:** GPIO 34–39 cannot drive HIGH/LOW. Vapor AO belongs on 34; do not try to blink an LED there.

**Strapping:** GPIO 0, 2, 12, 15 affect boot if held wrong. GPIO 13 is also a JTAG strap (F-010); we still use it for the buzzer.

**Firmware board id:** `esp32dev` in `firmware/platformio.ini`.

---

## 3. USB data cable (B2)

**What it is:** USB 2.0 with **D+ / D−** (data) plus 5 V and GND.

**Why it matters:** The on-board USB-UART chip needs data lines to enumerate a **COM** port. A charge-only cable has 5 V/GND only → the board may power but **upload and serial fail**.

Match **micro-USB vs USB-C** to the DevKit you bought.

---

## 4. 10 kΩ linear potentiometer (B3)

**What it is:** A three-terminal **resistive voltage divider**. Total resistance ~10 kΩ (B taper = **linear** with angle). The wiper taps a fraction of the voltage between the two ends.

```
  3V3 ---- R_upper ---- wiper ---- R_lower ---- GND
                         |
                      V_wiper = 3.3 * (R_lower / 10 kΩ)
                         |
                      ESP32 ADC (high impedance)
```

**Why 10 kΩ:** Low enough that ADC pin leakage is small; high enough that 3V3 current is only ~0.33 mA (`3.3 / 10000`). Logarithmic **A10K** (audio) would warp `v` vs knob angle — reject it.

**Speed pot (GPIO 33):** Firmware treats `V_wiper` as **calibrated speed**, not a car sensor:

`v = (N_v / 4095) * 120` km/h.

**Dry vapor pot (GPIO 34):** Same circuit, stands in for MQ-2 AO so `d` can be set by hand. **Never** parallel with MQ-2 AO.

**Noise:** Wipers bounce; L1 averages `M = 32` samples.

---

## 5. SSD1306 OLED 128×64 (B4)

**What it is:** A glass OLED panel plus **SSD1306** controller. Pixels are self-emissive (no backlight). This module is **I²C**, four pins: VCC, GND, SCL, SDA.

**Bus:** Two wires shared by all I²C devices. ESP32 is master. Default address **0x3C** (some boards **0x3D**, F-006). Open-drain SDA/SCL with pull-ups (usually already on the module).

**Why I²C:** Only two GPIOs vs 6–7 for SPI. Speed is plenty for ~2 Hz text updates.

**Logic:** Power from **3V3**. Do not feed 5 V into SDA/SCL from a 5 V-only module without checking.

**What the firmware shows:** `d`, `v`, `T_mod`, `T_high`, state — the adaptive law must be visible (L5).

**Library:** Adafruit SSD1306 + GFX (`platformio.ini`). 128×32 modules are too short for four lines.

---

## 6. RGB LED and 220 Ω resistors (B5)

**What it is:** Three LEDs in one 5 mm package (red, green, blue). **Common cathode:** the long/common pin is the shared **negative**. Each colour anode needs its own series resistor.

```
  GPIO 25 --[220 Ω]-- R anode
  GPIO 26 --[220 Ω]-- G anode ---- common cathode ---- GND
  GPIO 27 --[220 Ω]-- B anode
```

**Why 220 Ω:** LED current ≈ `(3.3 − Vf) / 220`. Vf is ~2.0 V (red) to ~3.0 V (blue). Current stays in a safe ~2–6 mA range for a demo. 180–330 Ω is OK.

**Firmware:** Active **high** (GPIO 1 = LED on). SAFE = green; MOD = red+green (yellow); HIGH = red. Common **anode** modules invert this (F-009) — confirm with DMM **diode** mode.

**Do not** omit the resistors; GPIO shorted to LED can overcurrent the pin.

---

## 7. Active buzzer (B6)

**What it is:** A sounder with an **internal oscillator**. DC on the `+` pin → tone. **Passive** piezo needs a square wave (`tone()`); we do **not** buy that.

**Drive:** GPIO 13 HIGH ≈ 3.3 V. Many 5 V buzzers still click at 3.3 V; if too quiet, a transistor + 5 V can be added later (not in the default schematic).

**Firmware:** SAFE off; MOD toggles every `T_beep` (300 ms) with `millis()`; HIGH held on. No `delay()` for cadence (loop must keep sampling).

**GPIO 13:** Also a JTAG strap (F-010). Fine for a class demo; do not fight the pin during boot with a short to 3V3.

---

## 8. Tactile button (B7)

**What it is:** Momentary **normally open** switch. Four legs: two pairs internally shorted. One pair to GPIO 4, one pair to GND.

**Pull-up:** `INPUT_PULLUP` holds the pin at 3.3 V when open. Press connects to GND → reads **LOW**. Firmware recaptures baseline `N_0`.

**Bounce:** Firmware currently can block on the button (F-003). For the viva, one clean press after warm-up is enough.

**DMM:** Continuity only **while pressed** (identifies the correct pair of legs).

---

## 9. Breadboard and Dupont (B8)

**What it is:** Solderless **tie-point** matrix. Typical MB102: centre gap (IC / ESP32 straddles it), left/right power rails. Many boards **break** the red/blue rails in the middle — jumper them or you have a dead half-rail.

**Dupont:** 2.54 mm jumpers. **M–M** hole-to-hole; **M–F** to module male headers (OLED, MQ-2).

**Current:** Fine for logic milliamps. MQ-2 heater (~150 mA) should use decent wires from the **5 V adapter**, not a flimsy 10 cm jumper if it gets warm.

---

## 10. MQ-2 module (B9)

**What it is:** A heated **SnO2** (tin dioxide) chemoresistor in a mesh can, plus a small PCB with a load resistor, comparator (**DO**), and trim pot. Conductivity **rises** with several combustible gases and smoke (LPG, hydrogen, alcohol, etc.). That is why it is an **index**, not “petrol ppm”.

**Heater:** A coil that needs **~5 V and ~120–180 mA** continuously. The ESP32 3V3 pin cannot supply this. Use B10. Preheat: datasheets quote hours for a new sensor; this lab uses **60 s** (`DRY_POT 0`) as a demo settle, not a laboratory calibration.

**AO:** Analog voltage from the divider (sensor + load). Often tracks **module VCC**. If VCC = 5 V, AO can exceed **3.3 V** → **must** DMM, then divider if needed.

**DO:** Digital trip vs onboard trim pot. Firmware **ignores** it. The academic law is `d` vs `T(v)` on AO counts.

**Rs/R0:** Datasheet log-log ppm curves. **Not implemented.** No inversion to concentration.

**Safety:** No petrol, no fuel tank, no vehicle. Optional IPA far from the PCB (P7).

---

## 11. 5 V adapter (B10)

**What it is:** A regulated **DC** wall wart, ≥1 A so the heater has margin. Output **5.0 V**, not 9 V / 12 V.

**Use:** MQ-2 **heater VCC** only. Tie **GND** to ESP32 GND (one ground, two positives).

**Do not:** Power the heater from USB 3V3. Do not assume a breadboard “MB102 5 V module” is a substitute for a real adapter unless you have measured 5 V and current capability.

**DMM:** DC V 20 V range on the barrel, **not** AC on the mains pins.

---

## 12. Digital multimeter (B11)

**What it is:** A handheld meter. This lab needs a cheap DT830-class unit.

Full dial map: `docs/buy.md` (How we use the multimeter).

| Function | Component job |
|----------|----------------|
| DC V | 3V3 rail, 5 V brick, pot wiper, MQ-2 AO ≤ 3.3 V |
| Ω | 220 Ω, 10 kΩ pot **ends**, divider |
| Diode | RGB common cathode vs anode |
| Continuity | GND net, Dupont, button |

Unused: AC V, amps, hFE, 10 A jack.

---

## 13. USB fan (B12, optional)

**What it is:** A 5 V brushless (or brushed) fan on USB-A. Independent of the ESP32.

**Use:** Move air across the **MQ-2** while `v` still comes from the **speed pot**. Qualitative “dilution” story. Not a tachometer; firmware does not read RPM.

---

## 14. 10 kΩ resistor pair (AO divider)

**What it is:** Two equal resistors as a **2:1** voltage divider.

```
  MQ-2 AO ---- R ---- mid ---- R ---- GND
                     |
                  GPIO 34
```

If AO ≈ 5 V max, mid ≈ 2.5 V, safe for ADC. Re-measure DC V at **mid**. Equal values keep the Thevenin resistance modest (5 kΩ for two 10 kΩ) so the ADC still sees a stiff source.

---

## 15. On-board LED (GPIO 2)

**What it is:** LED + resistor already on the DevKit. GPIO 2 is a boot strap — HIGH at reset is the usual LED-off / run condition on many boards. Firmware blinks it in **WARMUP**.

---

## 16. How data becomes `T(v)` (components → math)

| Stage | Hardware | Quantity |
|-------|----------|----------|
| L0 | Pot or MQ-2 AO | Voltage 0–3.3 V (after divider if any) |
| L1 | ADC1 + average `M` | `N`, `N_v` counts |
| L2 | Baseline button | `d = max(0, N − N_0)`, `v` from `N_v` |
| L3 | Software only | `T_mod(v)`, `T_high(v)` |
| L4 | Software FSM | SAFE / MOD / HIGH |
| L5 | OLED, RGB, buzzer, UART | Operator + CSV |

No component “computes” `T(v)`. The MCU does. The electronics only provide **voltages** and **actuators**.

---

## 17. Related files

| File | vs this document |
|------|------------------|
| `hardware.md` | Pins, wiring, what to do on the bench |
| `circuit-diagram.md` | ASCII + mermaid schematics, netlist |
| `buy.md` | Photos, specs, shop links, DMM dial |
| `abbreviations.md` | ADC, GPIO, `T_mod`, … |
| `architecture.md` | Why layers exist |
| `mathematics.md` | Equations for `d` and `T(v)` |
| `firmware.md` | Loop and serial format |
