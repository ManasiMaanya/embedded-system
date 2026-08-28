# Abbreviations and symbols

Glossary for this workspace (ESP32 tank-vapor monitor, speed-scheduled `T(v)`). Symbols that are math, not acronyms, are listed under **Signals and thresholds**.

| Doc | Role |
|-----|------|
| This file | Abbreviations |
| [overview.md](overview.md) | Course narrative |
| [architecture.md](architecture.md) | L0–L5 |
| [mathematics.md](mathematics.md) | Equations |
| [hardware.md](../.cursor/skills/esp32-fuel-vapor/hardware.md) | Pins and part use |
| [buy.md](buy.md) | Shop IDs B1–B12 |

---

## A–Z (project terms)

| Abbr. / token | Expansion | Meaning here |
|---------------|-----------|----------------|
| **3V3** | 3.3 volt rail | ESP32 logic supply; pot high side; OLED VCC. Not for MQ-2 heater. |
| **5 V** | Five volts DC | MQ-2 heater (B10). Common GND with USB. |
| **AC** | Alternating current | **Do not** measure wall AC with the DMM in this lab. |
| **ADC** | Analog-to-digital converter | 12-bit ESP32 converter. Thresholds use **counts**, not volts. |
| **ADC1** | ADC unit 1 | Only ADC1 pins in this lab (GPIO 33, 34). ADC2 conflicts with Wi-Fi (unused). |
| **ADC1_CH5 / CH6** | ADC1 channel 5 / 6 | Speed pot = CH5 (GPIO 33). Vapor/MQ-2 = CH6 (GPIO 34). |
| **AO** | Analog output (MQ-2) | Voltage proportional to vapor **index**. Goes to GPIO 34 after DMM check. |
| **B10K** | Linear 10 kΩ pot (B taper) | Required for speed and dry vapor. Not **A10K** (audio/log). |
| **A10K** | Logarithmic 10 kΩ pot | **Reject** for this project. |
| **BLE** | Bluetooth Low Energy | On the ESP32 chip; **not used**. |
| **BOM** | Bill of materials | Parts list (`hardware.md`, `buy.md`). |
| **BOOT** | Boot button | ESP32 download / boot mode. |
| **CH340 / CP2102** | USB–UART bridge ICs | Either is fine if Windows installs a driver. |
| **CLI** | Command-line interface | `pio`, `scripts\*.cmd`. |
| **COM** | Communications port (Windows) | Serial device after USB enumerate. Also DMM **COM** jack (black probe). |
| **CSV** | Comma-separated values | Serial and sim log: `t_ms,raw,baseline,delta,speed,Tmod,Thigh,state`. |
| **DC** | Direct current | All bench voltages (3.3 V, 5 V, AO). |
| **DC V / V⎓** | DC voltage (DMM dial) | Main meter function. Range **20 V**. |
| **DevKit** | Development kit | DOIT **ESP32 DevKit V1**, 30-pin, WROOM-32. |
| **DMM** | Digital multimeter | B11. DC V, Ω, diode, continuity only. |
| **DO** | Digital output (MQ-2) | Comparator trip. **Unused** in firmware. |
| **DRY_POT** | Dry-potentiometer mode | `pins.h`: `1` = 2 s warm-up, no heater; `0` = 60 s MQ-2 warm-up. |
| **Dupont** | Dupont jumper wire | M–M and M–F 2.54 mm jumpers. |
| **EN** | Enable / reset | ESP32 reset button. |
| **ESP32** | Espressif 32-bit SoC | Dual-core Xtensa MCU on the DevKit. |
| **ESP-IDF** | Espressif IoT Development Framework | Not required; this repo uses Arduino via PlatformIO. |
| **F-NNN** | Fault ID | `docs/fault-ledger.md`. Fix only after `Approve F-xxx`. |
| **FSM** | Finite-state machine | L4: WARMUP, SAFE, MOD, HIGH. |
| **GFM** | GitHub Flavored Markdown | Tables in docs. |
| **GND** | Ground | Common return: USB, 5 V brick, pots, OLED, MQ-2. |
| **GPIO** | General-purpose input/output | Numbered pins, e.g. GPIO 34. |
| **H** | Hysteresis width | 40 counts on `T_mod` (leave toward SAFE). See F-001/F-002. |
| **HIGH** | High-alarm state | `d ≥ T_high`; red LED; continuous buzzer. |
| **HMI** | Human–machine interface | OLED + RGB + buzzer + UART (L5). |
| **HTML** | HyperText Markup Language | `scripts\preview_md.py` browser preview. |
| **I²C / I2C** | Inter-Integrated Circuit | OLED bus. SDA GPIO 21, SCL GPIO 22. |
| **IC** | Integrated circuit | e.g. SSD1306, CP2102. |
| **IDE** | Integrated development environment | Cursor / VS Code; Arduino IDE not required. |
| **i.i.d.** | Independent and identically distributed | Math assumption for averaging `M` samples. |
| **INR / ₹** | Indian rupee | BUY budget ~₹2000. |
| **IoT** | Internet of Things | Marketing term on ESP32 listings; this lab is **offline**. |
| **IPA** | Isopropyl alcohol | Optional P7 chemical demo. **Not petrol.** Far from PCB. |
| **I/O** | Input/output | GPIO, ADC. |
| **JTAG** | Joint Test Action Group | Debug pins; GPIO 13 is a strap (F-010, buzzer). |
| **K / K_MOD / K_HIGH** | Slope of `T(v)` | Counts per km/h. `K_MOD = 0.8`, `K_HIGH = 1.2` default. |
| **KaTeX** | LaTeX renderer (web) | Optional in HTML preview; docs use ASCII `T_mod`. |
| **L0–L5** | Architecture layers | Analog → acquire → features → threshold → FSM → HMI. |
| **LED** | Light-emitting diode | RGB and on-board GPIO 2. |
| **M** | Averaging length | 32 ADC samples (`kAvgSamples`). |
| **M–M / M–F** | Male-to-male / male-to-female | Dupont connectors. |
| **MA** | Moving average | L1 filter (block average of `M` samples). |
| **MCU** | Microcontroller unit | ESP32. |
| **MD** | Markdown | `.md` docs. |
| **MOD** | Moderate-alarm state | `d ≥ T_mod` (and not HIGH); yellow; intermittent beep. |
| **MQ-2** | Metal-oxide gas sensor (Hanwei type) | Combustible-vapor **index**, not petrol-specific ppm. |
| **ms** | Milliseconds | `t_ms`, `T_log` = 500 ms, `T_beep` = 300 ms. |
| **N** | ADC code | Raw / averaged count, 0–4095. |
| **N_0** | Baseline count | Clean-air (or dry-pot zero) average. |
| **N_bar** | Averaged ADC | `N` after `M` samples. |
| **N_v** | Speed-pot ADC | Mapped to `v`. |
| **N_max** | Full-scale ADC | 4095 (12-bit). |
| **OLED** | Organic LED display | SSD1306 128×64. |
| **Ω** | Ohm | DMM resistance; 220 Ω, 10 kΩ. |
| **P0–P8** | Implementation phases | Sim → blink → OLED → pots → HMI → dry labs → MQ-2 → optional → report. |
| **PATH** | Executable search path | Where `python` / `pio` are found. |
| **PCB** | Printed circuit board | Keep IPA/solvents off it. |
| **PIO / pio** | PlatformIO CLI | `scripts\pio.cmd`. |
| **ppm** | Parts per million | **Not** used. No MQ-2 Rs/R0 inversion. |
| **PSU** | Power supply unit | B10 5 V adapter. |
| **PWM** | Pulse-width modulation | Not required for the active buzzer. |
| **R0 / Rs** | MQ-2 clean-air / sense resistance | Datasheet curve; **out of scope**. |
| **RGB** | Red–green–blue LED | Alarm colours. |
| **SAFE** | Safe state | Below `T_mod` (with hysteresis); green; buzzer off. |
| **SCL** | Serial clock (I²C) | GPIO 22. |
| **SDA** | Serial data (I²C) | GPIO 21. |
| **SKU** | Stock keeping unit | Shop listing; clones of DevKit V1 are OK if 30-pin WROOM-32. |
| **SoC** | System on chip | ESP32. |
| **SPI** | Serial Peripheral Interface | **Not** used (reject 7-pin SPI OLED). |
| **SSD1306** | OLED controller IC | 128×64, I²C. |
| **T(v)** | Threshold as a function of speed | Academic core: `T_mod(v)`, `T_high(v)`. |
| **T_0 / T_MOD_0 / T_HIGH_0** | Intercept of `T(v)` | Parked trip: 180 and 420 counts default. |
| **T_beep** | Buzzer toggle period | 300 ms in MOD. |
| **T_fix** | Fixed (non-adaptive) threshold | `T_MOD_0`; contrast with `T_mod(v)`. |
| **T_h / Thigh** | `T_high(v)` | CSV column `Thigh`. |
| **T_high(v)** | High-band schedule | `T_HIGH_0 + K_HIGH * v`. |
| **T_log** | UART log period | 500 ms (~2 Hz). |
| **T_m / Tmod** | `T_mod(v)` | CSV column `Tmod`. |
| **T_mod(v)** | Moderate-band schedule | `T_MOD_0 + K_MOD * v`. |
| **T_w** | Warm-up time | 2 s dry / 60 s MQ-2. |
| **UART** | Universal asynchronous receiver/transmitter | USB serial 115200. |
| **USB** | Universal Serial Bus | DevKit power+data; optional fan. |
| **USB-C / micro-USB** | USB connector types | Must match B1 and B2. |
| **VCC** | Positive supply pin | Module “VCC”: OLED 3.3 V; MQ-2 heater 5 V. |
| **V_FS** | Full-scale voltage | ~3.3 V at ADC_11db (working assumption). |
| **VIN** | Voltage in | DevKit 5 V input pin; this lab uses USB instead. |
| **VIT** | Vellore Institute of Technology | Course context. |
| **WARMUP** | Warm-up state | `d` forced 0; no trip; LED blink. |
| **WROOM-32** | ESP32 module name | Metal can on DevKit V1. |
| **WYSIWYG** | What you see is what you get | Cursor rich Markdown Preview (can be blank; use built-in preview or `preview-docs.cmd`). |
| **d** | Delta / vapor index | `max(0, N_bar − N_0)`, **counts**. |
| **d_enter** | Trip delta at fixed `v` | `d_enter_mod(v) = T_mod(v)`. |
| **esp32dev** | PlatformIO board id | `firmware/platformio.ini`. |
| **hFE** | Transistor gain (DMM) | **Unused.** |
| **km/h** | Kilometres per hour | Unit of `v` (pot calibration, not a car sensor). |
| **v** | Speed | 0–120 km/h from speed pot. |
| **v_enter / v_leave** | Inverse trip speeds | `docs/mathematics.md` §5. Default `d=200`: 25 and 75 km/h. |
| **v_max** | Maximum mapped speed | 120 km/h. |

---

## Architecture layers (L0–L5)

| Layer | Name | One-line use |
|-------|------|----------------|
| **L0** | Analog | MQ-2 AO or vapor pot; speed pot; 3.3 V |
| **L1** | Acquisition | ADC1, average `M` samples |
| **L2** | Features | `v` from `N_v`; `d` from baseline |
| **L3** | Threshold | `T_mod(v)`, `T_high(v)` |
| **L4** | Decision | Hysteresis FSM |
| **L5** | HMI | OLED, RGB, buzzer, UART CSV |

---

## Alarm states

| Token | CSV `state` | RGB | Buzzer |
|-------|-------------|-----|--------|
| **WARMUP** | 0 | Off / blink GPIO 2 | Off |
| **SAFE** | 1 | Green | Off |
| **MOD** | 2 | Yellow (R+G) | Intermittent |
| **HIGH** | 3 | Red | Continuous |

---

## Phases, BUY IDs, scripts

| Token | Meaning |
|-------|---------|
| **BUY** | Parts acquisition (parallel with P0) |
| **B1–B12** | Catalog IDs in `docs/buy.md` |
| **P0** | PC sim + closed form |
| **P1** | Toolchain + blink |
| **P2** | OLED |
| **P3** | ADC pots + `T(v)` on display |
| **P4** | Alarm FSM + HMI |
| **P5** | Dry two-pot labs |
| **P6** | MQ-2 on 5 V |
| **P7** | Optional IPA / fan / tune `K` |
| **P8** | Report + viva |
| **p0.cmd** | Run `sim/adaptive_threshold.py` |
| **pio.cmd** | PlatformIO wrapper |

---

## Serial / sim CSV columns

| Column | Meaning |
|--------|---------|
| **t_ms** | Time since start (ms) |
| **raw** | Averaged vapor ADC (empty in sim) |
| **baseline** | `N_0` (empty in sim) |
| **delta** | `d` |
| **speed** | `v` (km/h) |
| **Tmod** | `T_mod(v)` |
| **Thigh** | `T_high(v)` |
| **state** | 0–3 as above |

---

## Fault prefix

**F-** = logged issue (`docs/fault-ledger.md`). Examples: **F-001** HIGH↔MOD chatter; **F-002** stuck HIGH; **F-011** Cursor Markdown preview.

Do not patch firmware/sim for an open **F-** ID unless the user names it and approves.
