# BUY catalog — parts, photos, specifications

Class budget about **₹2000**. Photos are **look-like** listing shots so you can match a shop photo; they are not a specific brand SKU. Pins and power: `.cursor/skills/esp32-fuel-vapor/hardware.md`. Tick the boxes when the part is **on the desk** and matches the **Must match** row.

**Do not buy petrol, a fuel tank, or extra MQ-2 modules** (localization is out of scope).

Prices are typical India hobby-shop ranges (2026). **Shop links go out of stock**; if a page 404s, search that shop for the same name. Prefer one cart (Robu / Circuit City / Robocraze) so shipping is once.

**Primary product pages (open these):**

| ID | Buy this listing |
|----|------------------|
| B1 | [Circuit City — ESP32 DevKit V1 30-pin](https://circuit-city.in/product/esp-32/) |
| B2 | [Robu — USB-A to micro-USB 1 m (data)](https://robu.in/product/usb-to-micro-usb-cable-wire-1m-for-nodemcu/) |
| B3 | [Robu — 10 kΩ pot](https://robu.in/product/10k-pot/) (**qty 2**; confirm **linear / B10K**) |
| B4 | [Robu — 0.96″ SSD1306 I²C OLED](https://robu.in/product/0-96-inch-oled/) |
| B5 | [Robocraze — 5 mm RGB **common cathode**](https://robocraze.com/products/5mm-rgb-led-common-cathode-diffuse-pack-of-10) + [Amazon search: 220 Ω ¼ W](https://www.amazon.in/s?k=220+ohm+1%2F4+watt+resistor+pack) |
| B6 | [Robu — 5 V **active** buzzer](https://robu.in/product/5v-active-electromagnetic-buzzer-pack-of-5/) |
| B7 | [Robu — 6×6 tactile](https://robu.in/product/6x6x5mm-tactile-push-button-switch-pack-of-20/) |
| B8 | [Robu — MB102 830-point breadboard](https://robu.in/product/mb102-830-points-solderless-prototype-pcb-breadboard-high-quality/) + [M–F Dupont 40×30 cm](https://robu.in/product/male-to-female-jumper-wires-40-pin-30cm/) + [Amazon search: male-to-male Dupont 40 pin](https://www.amazon.in/s?k=male+to+male+jumper+wire+40+pin+dupont) |
| B9 | [Robocraze — MQ-2 module](https://robocraze.com/products/mq-2-gas-sensor) (**one** only) |
| B10 | [Robu — 5 V 2 A wall adapter](https://robu.in/product/orange-5v-2a-power-supply-with-dual-pin-dc-plug-adapter/) |
| B11 | [Robu — DT830D DMM](https://robu.in/product/digital-multimeter-small-yellow-color-lcd-ac-dc-measuring-voltage-current/) (skip if lab has a meter) |
| B12 | [Robu — 5 V USB cooling fan](https://robu.in/product/dc-5v-5010-oil-containing-cooling-fan-with-usb-size505010mm/) (optional) |
| Extra | [Amazon search: 10 kΩ ¼ W resistor](https://www.amazon.in/s?k=10k+ohm+1%2F4+watt+resistor+pack) (AO divider, two pieces) |

## Summary

| | ID | Item | Qty | Phase | Use in this project | Typical ₹ | Tick |
|---|----|------|-----|-------|---------------------|-----------|------|
| <img src="images/buy/buy-esp32.png" alt="ESP32 DevKit" width="140"/> | B1 | ESP32 DevKit | 1 | P1 | MCU: ADC, I²C, GPIO, USB serial | 250–450 | [ ] |
| <img src="images/buy/buy-usb.png" alt="USB data cable" width="140"/> | B2 | USB **data** cable | 1 | P1 | Upload firmware + CSV monitor | 50–150 | [ ] |
| <img src="images/buy/buy-pots.png" alt="10k potentiometers" width="140"/> | B3 | 10 kΩ **linear** pots | 2 | P3 | Speed `v` + dry vapor `d` | 20–50 each | [ ] |
| <img src="images/buy/buy-oled.png" alt="SSD1306 OLED" width="140"/> | B4 | SSD1306 128×64 I²C OLED | 1 | P2 | Show `d`, `v`, `T_mod`, `T_high`, state | 150–280 | [ ] |
| <img src="images/buy/buy-rgb.png" alt="RGB LED and 220 ohm resistors" width="140"/> | B5 | RGB LED + 220 Ω resistors | 1 + 3 | P4 | Green / yellow / red alarm | 20–60 | [ ] |
| <img src="images/buy/buy-buzzer.png" alt="Active buzzer" width="140"/> | B6 | Active buzzer | 1 | P4 | Off / beep / continuous | 20–50 | [ ] |
| <img src="images/buy/buy-button.png" alt="Tactile button" width="140"/> | B7 | Tactile button 6×6 mm | 1 | P4 | Recapture baseline | 5–20 | [ ] |
| <img src="images/buy/buy-breadboard.png" alt="Breadboard and Dupont wires" width="140"/> | B8 | Breadboard + Dupont wires | 1 kit | P1 | Wire the bench without solder | 120–250 | [ ] |
| <img src="images/buy/buy-mq2.png" alt="MQ-2 module" width="140"/> | B9 | MQ-2 **module** | 1 | P6 | Tank vapor index (AO) | 120–220 | [ ] |
| <img src="images/buy/buy-psu.png" alt="5V adapter" width="140"/> | B10 | 5 V adapter ≥1 A | 1 | P6 | MQ-2 heater only | 150–350 | [ ] |
| <img src="images/buy/buy-dmm.png" alt="Digital multimeter" width="140"/> | B11 | DMM (borrow OK) | 1 | P6 | DC V, Ω, diode, continuity | 0–400 | [ ] |
| <img src="images/buy/buy-fan.png" alt="USB fan" width="140"/> | B12 | USB fan | 1 optional | P7 | Optional airflow demo | 100–300 | [ ] |

**Need by P1:** B1, B2, B8. **Need by P2:** B4. **Need by P3:** B3. **Need by P4:** B5–B7. **Need by P6:** B9, B10, B11. Buy B9 early; it can ship slowly.

Optional extra (no photo): two **10 kΩ ¼ W** resistors if MQ-2 AO is above 3.3 V (divider). ₹5–15.

---

## How we use the multimeter (B11)

A cheap DT830-class meter is enough. You do **not** need True RMS, capacitance, or 10 A current for this capstone.

Black probe in **COM**. Red probe in **VΩmA** (the left/small jack), never the 10 A jack unless you are measuring amps (we are not).

| Dial | Name | Use in this project | Typical reading |
|------|------|---------------------|-----------------|
| **V⎓** (DC volts), range **20 V** | DC voltage | **Main tool.** Rails, adapter, sensor AO, pot wiper. | 3.3 V rail; ~5.0 V heater; AO **must be ≤ 3.3 V** before GPIO 34 |
| **Ω** (200 / 2k / 20k) | Resistance | Check 220 Ω and 10 kΩ parts; pot end-to-end ~10 kΩ | 220 Ω bands; 10 kΩ pot between the two **ends** (not wiper) |
| **Diode** (▶\|) | Diode / LED | Identify RGB **common cathode** vs common anode (F-009) | One colour lights with red on that pin, black on common → common is **cathode** |
| **Continuity** (♪) if the meter has it; else Ω near 0 | Beep / short | Wires, button closed, **common GND** from USB to 5 V brick | Beep = connected |

**Do not use for this lab**

| Dial | Why skip |
|------|----------|
| **V~** AC volts | Bench is DC only. Mains AC is a shock hazard; do not probe wall sockets. |
| **A / mA** current | Not required. Measuring current means breaking the circuit; easy to blow the meter fuse. |
| **hFE** transistor socket | Unused. |
| **10 A** jack | Unused. Leave red probe out of that hole. |

**DC V procedure (every voltage check):** range **20 V DC** (or auto). Black on **GND** (ESP32 GND / breadboard blue rail). Red on the point under test. Read volts.

**Must-pass check (P6, before GPIO 34):** heater **5 V** on MQ-2 VCC, common GND, **AO to GND** ≤ **3.3 V**. If higher, fit the Extra 10 kΩ divider, then measure **again** at the ESP32 side of the divider.

---

## B1 — ESP32 DevKit

<img src="images/buy/buy-esp32.png" alt="ESP32 DevKit V1 style board" width="280"/>

| Field | Spec |
|-------|------|
| Search terms | `ESP32 DevKit V1`, `DOIT ESP32 DevKit`, `ESP32-WROOM-32 30-pin` |
| MCU | Espressif **ESP32**, dual-core Xtensa, up to 240 MHz |
| Wireless | Wi-Fi + Bluetooth on the chip — **this project does not use them** |
| Logic | **3.3 V only.** Do not put 5 V on GPIO. |
| Flash | typically 4 MB on the module |
| ADC | 12-bit; this lab uses **ADC1** only (GPIO 34 vapor, GPIO 33 speed) |
| USB-UART | CP2102 **or** CH340. Either is fine if Windows installs a driver. |
| Connector | micro-USB **or** USB-C — **match the cable (B2)** |
| Headers | 30-pin DevKit V1 (two long rows) preferred so it sits on a breadboard |
| Must match | Board enumerates as a COM port; `EN` / `BOOT` buttons present |
| Reject | ESP8266 NodeMCU, STM32 “Blue Pill”, 5 V Arduino Uno as the only MCU |
| Used with | USB (B2), breadboard (B8) |

**Use in this project:** L0–L5 controller. Runs `firmware/` (`esp32dev`): ADC on GPIO 34/33, I²C OLED, RGB, buzzer, serial CSV. Power the **MCU from USB only**. Wi-Fi/Bluetooth stay **off**. On-board LED (GPIO 2) blinks in warm-up (P1).

**DMM on this part:** **DC V** 3V3 pin vs GND ≈ 3.3 V with USB plugged in. **Continuity** from ESP32 GND to breadboard GND (must beep). Do not put 5 V on any GPIO.

Firmware target: `esp32dev` in `firmware/platformio.ini`.

**Buy this board (not S3 / C3 / 38-pin):** **DOIT ESP32 DevKit V1**, **30 pins**, **ESP32-WROOM-32**. Same pinout as [espboards.dev DevKit V1](https://www.espboards.dev/esp32/esp32doit-devkit-v1/). CP2102 or CH340 both work.

| Shop | Link | Plug | Notes |
|------|------|------|-------|
| Circuit City (recommended) | https://circuit-city.in/product/esp-32/ | micro-USB | Title says **DevKit V1, 30-pin, WROOM-32**. Match B2 to **micro-USB**. |
| techiesms | https://techiesms.com/product/esp32-development-board-doit-devkit-v1/ | check listing | Named **Doit DevKit V1**. Confirm **30-pin** in photos. |
| RobuKits | https://robukits.in/product/301/esp32-development-board-esp32-devkit-v1 | micro-USB | **30 pins**, WROOM-32. USB-C twin: https://robukits.in/product/865/esp32-development-board-esp32-devkit-v1-30-pins-c-type (stock varies). |

Listings go out of stock. If a link 404s, search the same shop for `ESP32 DevKit V1 30 pin WROOM-32`. Do **not** substitute ESP32-C3 SuperMini, ESP32-S3, ESP8266 NodeMCU, a bare WROOM module (no USB), or a **38-pin** ESP32 board without rechecking silkscreen vs `hardware.md`.

---

## B2 — USB data cable

<img src="images/buy/buy-usb.png" alt="USB data cables" width="280"/>

| Field | Spec |
|-------|------|
| Search terms | `USB data cable` (not “charge only”) + the plug on **your** ESP32 |
| Must match | Computer sees a **COM / serial** device when the board is plugged in |
| Reject | Charge-only cables (no data wires) — upload will fail |
| Used with | B1, P1 upload |

**Use in this project:** Power + **data** so PlatformIO can upload and `scripts\p1-monitor.cmd` can print CSV. Charge-only cables fail P1.

**DMM:** not required. If upload fails, try another cable before blaming the board.

**Buy:** Circuit City ESP32 listing is **micro-USB**, so this cable matches B1.

| Shop | Link | Notes |
|------|------|-------|
| Robu (recommended if B1 is micro-USB) | https://robu.in/product/usb-to-micro-usb-cable-wire-1m-for-nodemcu/ | 1 m USB-A → micro-USB; listing says data + charge. |
| Robu (short) | https://robu.in/product/20-cm-usb-cable/ | 20 cm micro-USB; fine on the bench. |
| Amazon (USB-C board) | https://www.amazon.in/s?k=usb+a+to+usb+c+data+cable | Only if you bought the **Type-C** DevKit V1. |

---

## B3 — Two 10 kΩ linear potentiometers

<img src="images/buy/buy-pots.png" alt="Two 10k breadboard potentiometers" width="280"/>

| Field | Spec |
|-------|------|
| Search terms | `10k linear potentiometer breadboard`, `B10K` (B = linear) |
| Resistance | **10 kΩ** ±20% is OK |
| Taper | **Linear (B)**. Do **not** buy audio/log **A10K** as the speed pot |
| Power | 0.1 W or 0.5 W; either is fine |
| Terminals | **3** (two ends + wiper). Knob optional but useful for the demo |
| Wiring | Ends: 3V3 and GND. Speed wiper → **GPIO 33**. Dry-vapor wiper → **GPIO 34** (MQ-2 disconnected) |
| Map | `v = (ADC/4095)*120` km/h |
| Qty | **2** (speed + dry vapor). One pot is not enough for P3/P5 |
| Reject | 1 kΩ or 100 kΩ only; dual-gang stereo pots unless you know the pinout |
| Used with | P3–P5; never in parallel with MQ-2 AO on GPIO 34 |

**Use in this project**

| Pot | Role | Pin | What you demonstrate |
|-----|------|-----|----------------------|
| Speed | Independent variable `v` (0–120 km/h) | Wiper → GPIO **33** | `T_mod(v)` and `T_high(v)` move on OLED |
| Dry vapor | Fake `d` without MQ-2 | Wiper → GPIO **34** | P3–P5 tables; **unplug** before MQ-2 |

Ends of each pot: **3V3** and **GND**.

**DMM:** **Ω** 20 k range, probes on the two **ends** (not wiper) ≈ 10 kΩ. **DC V** 20 V: black GND, red **wiper** — voltage sweeps ~0–3.3 V as you turn (same as the ADC sees).

**Buy qty 2.** Title must say **10 kΩ** and **linear** / **B10K**, not A10K.

| Shop | Link | Notes |
|------|------|-------|
| Robu | https://robu.in/product/10k-pot/ | Add **2** to cart. Confirm linear in the description. |
| Electro Boat | https://electroboat.in/products/details/10k-ohm-potentiometer-rotary-variable-resistor-3-pin-with-knob | 3-pin with knob; good for the viva demo. |
| Project Point | https://projectpoint.in/index.php?route=product/product&product_id=498978119243 | Elcon **B10K** 16 mm, breadboard-friendly. |

---

## B4 — SSD1306 OLED 128×64 I²C

<img src="images/buy/buy-oled.png" alt="0.96 inch SSD1306 OLED" width="280"/>

| Field | Spec |
|-------|------|
| Search terms | `0.96 OLED SSD1306 I2C 128x64 4 pin` |
| Controller | **SSD1306** (not SH1106 unless you change the library) |
| Resolution | **128×64** |
| Size | 0.96 inch typical |
| Bus | **I²C**, 4 pins: `VCC GND SCL SDA` |
| Address | **0x3C** (firmware default). Some modules are **0x3D** (F-006) |
| VCC | 3.3–5 V. Prefer **3.3 V** from ESP32 3V3 |
| Pins here | SDA **GPIO 21**, SCL **GPIO 22** |
| Must show | `d`, `v`, `T_mod`, `T_high`, state — not a blank “Safe” only |
| Reject | SPI 7-pin OLED unless you rewire firmware; 128×32 “too short” for four lines |
| Used with | P2 onward |

**Use in this project:** Operator HMI (L5). Always show `d`, `v`, `T_mod`, `T_high`, and SAFE/MOD/HIGH so the adaptive law is visible. Wiring: VCC→3V3, GND→GND, SDA→GPIO **21**, SCL→GPIO **22**.

**DMM:** **DC V** on OLED **VCC** vs GND ≈ 3.3 V. If the screen is blank, check that before swapping I²C address (0x3C vs 0x3D).

**Buy:** 4 pins `VCC GND SCL SDA`, **128×64**, **SSD1306**. Not 7-pin SPI.

| Shop | Link | Notes |
|------|------|-------|
| Robu (recommended) | https://robu.in/product/0-96-inch-oled/ | 0.96″, SSD1306, I²C. |
| Probots | https://probots.co.in/0-96-inch-128-x-64-spi-i2c-4pin-oled-blue-display-module-ssd1306-controller.html | 4-pin I²C despite “SPI” in the URL; address 0x3C/0x3D. |
| ElectroPi | https://www.electropi.in/0.96-inch-i2c-iic-128x64-oled-display-module-4-pin-white-color | White pixels; same driver. |

---

## B5 — RGB LED + ~220 Ω resistors

<img src="images/buy/buy-rgb.png" alt="RGB LED and 220 ohm resistors" width="280"/>

| Field | Spec |
|-------|------|
| Search terms | `5mm RGB LED common cathode` + `220 ohm resistor` |
| LED | **4-pin 5 mm RGB**. Firmware assumes **common cathode**, active **high** (F-009 if inverted) |
| Identify cathode | Datasheet, or longest pin is often common on cheap 5 mm RGB — **verify with DMM diode mode** |
| Alternative | Three separate R/G/B LEDs, each with 220 Ω, commons to GND |
| Resistors | **3 × 220 Ω** ¼ W (red-red-brown-gold). 180–330 Ω is OK |
| GPIO | R **25**, G **26**, B **27** |
| Colours | Green SAFE, yellow = R+G MOD, red HIGH |
| Reject | Unlabeled 2-pin “RGB” modules with a driver chip unless you map pins |
| Used with | P4 |

**Use in this project:** Alarm colours (L5). Green = SAFE, yellow (R+G) = MOD, red = HIGH. Each colour pin through a **220 Ω** to GPIO 25/26/27; common cathode to **GND**.

**DMM:** **Ω** on each 220 Ω resistor (~220). **Diode** mode on the RGB: find which pin is common (see [How we use the multimeter](#how-we-use-the-multimeter-b11)). Firmware assumes **common cathode**; if colours are inverted you have common anode (F-009).

**Buy:** LED must be **common cathode**. Pack of 10 is fine (use one). Need **three** 220 Ω (or 180–330 Ω) ¼ W resistors.

| Shop | Link | Notes |
|------|------|-------|
| Robocraze (LED) | https://robocraze.com/products/5mm-rgb-led-common-cathode-diffuse-pack-of-10 | Title says **common cathode**. |
| Amazon (resistors) | https://www.amazon.in/s?k=220+ohm+1%2F4+watt+resistor+pack | Any ¼ W carbon-film pack. |
| Alternative LED | three 5 mm LEDs (R, G, B) from any hobby shop + same resistors | Commons to GND. |

---

## B6 — Active buzzer

<img src="images/buy/buy-buzzer.png" alt="Active buzzer" width="280"/>

| Field | Spec |
|-------|------|
| Search terms | `active buzzer 5V Arduino` (internal oscillator) |
| Type | **Active** (beeps on DC). Not a **passive** piezo that needs a square wave |
| Voltage | 3.3–5 V. If it is weak on 3.3 V GPIO, use a transistor + 5 V later |
| Pins | 2: `+` and GND. `+` → **GPIO 13** (note: GPIO 13 is also a JTAG strap, F-010) |
| Behaviour | Off / intermittent (`millis`) / continuous — **no** `delay()` for cadence |
| Reject | Passive buzzer (needs tone()) unless you change firmware |
| Used with | P4 |

**Use in this project:** Acoustic alarm (L5). Off in SAFE, intermittent in MOD (`millis()`), continuous in HIGH. `+` → GPIO **13**, `−` → GND. Active type: DC on/off is enough (no `tone()`).

**DMM:** **Continuity** from buzzer `−` to GND. Optional **DC V** across `+` and GND when HIGH (GPIO high ≈ 3.3 V). Skip current (A) measurement.

**Buy:** listing must say **active**. Pack of 5: use one.

| Shop | Link | Notes |
|------|------|-------|
| Robu (recommended) | https://robu.in/product/5v-active-electromagnetic-buzzer-pack-of-5/ | 5 V active, 2-pin. |
| Robu (module) | https://robu.in/product/5v-active-alarm-buzzer-module-arduino/ | PCB module; still **active**. Do not buy a **passive** buzzer. |

---

## B7 — Tactile button

<img src="images/buy/buy-button.png" alt="6x6 mm tactile buttons" width="280"/>

| Field | Spec |
|-------|------|
| Search terms | `6x6 tactile switch 4 pin breadboard` |
| Size | 6×6 mm through-hole, 4 legs |
| Wiring | One side **GPIO 4**, other side **GND**. Firmware `INPUT_PULLUP` |
| Function | Recapture clean-air / dry baseline |
| Qty | 1 required; extras are cheap |
| Used with | P4, P6 calibrate |

**Use in this project:** Recapture baseline `N_0` (L2) after warm-up or if clean air drifted. One side GPIO **4**, other **GND**. Firmware pull-up: pressed = LOW.

**DMM:** **Continuity** (or Ω) across the switch: open = infinite, **pressed** = short. Confirms you found the correct pair of legs on a 4-pin tact.

**Buy:** 6×6 mm through-hole. Pack of 20: use one.

| Shop | Link | Notes |
|------|------|-------|
| Robu | https://robu.in/product/6x6x5mm-tactile-push-button-switch-pack-of-20/ | 6×6 tactile, 4 legs. |

---

## B8 — Breadboard + Dupont wires

<img src="images/buy/buy-breadboard.png" alt="Breadboard and jumper wires" width="280"/>

| Field | Spec |
|-------|------|
| Search terms | `830 tie point breadboard` + `Dupont M-M M-F jumper 20 cm` |
| Breadboard | Full-size (~830 points) so ESP32 + pots + OLED fit |
| Wires | Mix of male–male and male–female (OLED often has male pins) |
| Must match | Power rails not broken in the middle without jumpers |
| Used with | All bench phases |

**Use in this project:** Prototype wiring without solder. ESP32 straddles the centre gap; pots, OLED, RGB, button, and (later) MQ-2 sit on the same board. Dupont: M–M for breadboard holes, M–F for OLED / module headers.

**DMM:** **Continuity** along a jumper (both ends). **Continuity** between the two GND rails if you jumpered them. Power rails on cheap boards are often **split** in the middle — continuity-check or add a jumper.

**Buy:** 830-point board **plus** M–M and M–F Dupont. Do not buy the “UNO R3 starter kit” unless you want extra Arduino junk.

| Shop | Link | Notes |
|------|------|-------|
| Robu (board) | https://robu.in/product/mb102-830-points-solderless-prototype-pcb-breadboard-high-quality/ | MB102 ~830 points. |
| Robu (M–F) | https://robu.in/product/male-to-female-jumper-wires-40-pin-30cm/ | OLED male pins → breadboard. |
| Amazon (M–M) | https://www.amazon.in/s?k=male+to+male+jumper+wire+40+pin+dupont | Breadboard-to-breadboard / ESP32 headers. |
| Robu (kit, optional) | https://robu.in/product/mb102-830-points-solderless-prototype-breadboard-power-supply-module-140-jumper-wires-arduino-diy-starter-kit/ | Board + jumpers; **do not** use the MB102 5 V rail to power the MQ-2 heater. |

---

## B9 — MQ-2 module (one only)

<img src="images/buy/buy-mq2.png" alt="MQ-2 analog gas sensor module" width="280"/>

| Field | Spec |
|-------|------|
| Search terms | `MQ-2 module AO DO` |
| Qty | **1** (tank zone only) |
| What it is | Combustible-vapor **index**, not petrol ppm |
| Heater | **5 V**, about **120–180 mA**. **Do not** power heater from ESP32 3V3 |
| Analog | Pin **AO** → GPIO 34 after DMM check |
| Digital | **DO** unused in this firmware |
| AO voltage | Often follows **module VCC**. If VCC=5 V, AO can be **> 3.3 V** → **must** divide before GPIO 34 |
| Warm-up | New sensor: long datasheet preheat; this lab: **60 s** in firmware when `DRY_POT 0` |
| Never | Petrol / fuel tank / vehicle. Optional later: **IPA** far from PCB (P7) |
| Never | AO and the vapor pot on GPIO 34 at the same time |
| Reject | MQ-135 / MQ-7 as a silent substitute without changing the report story |
| Used with | B10, B11, P6 |

**Use in this project:** Tank-zone vapor **index** (L0–L1). Analog **AO** only (firmware ignores **DO**). Heater VCC from **B10 5 V**, not ESP32 3V3. After DMM pass, AO → GPIO **34**. `DRY_POT 0`, 60 s warm-up, then calibrate. No petrol.

**DMM (required before the pin):** heater on. **DC V** MQ-2 **VCC vs GND** ≈ 5 V. **DC V** **AO vs GND** — must be **≤ 3.3 V**. If not, Extra divider, then measure the **divided** node. Common GND with ESP32 (**continuity** GND to GND).

**Buy exactly one.** Module with **AO** and **DO**. Heater still needs **5 V** (B10).

| Shop | Link | Notes |
|------|------|-------|
| Robocraze (recommended) | https://robocraze.com/products/mq-2-gas-sensor | MQ-2 module, ~5 V. |
| ElectroPi | https://www.electropi.in/sensors/mq2-flammable-gas-smoke-sensor-module-india | Cheap module; still check AO ≤ 3.3 V. |
| The Engineer Store | https://www.theengineerstore.in/products/mq-2-gas-sensor-module-for-h2-lpg-ch4-co-smoke-or-propane-detector-module | AO + DO, 5 V. |

---

## B10 — 5 V adapter (MQ-2 heater)

<img src="images/buy/buy-psu.png" alt="5V DC adapter" width="280"/>

| Field | Spec |
|-------|------|
| Search terms | `5V 2A DC adapter 5.5x2.1` + breadboard barrel adapter, **or** a dedicated 5 V USB brick **only for the sensor** |
| Voltage | **5.0 V DC** regulated |
| Current | **≥ 1 A** (heater ~0.15 A plus margin) |
| Ground | **Common GND** with ESP32 USB ground |
| Must not | Power the MQ-2 heater from the ESP32 3V3 pin |
| Used with | B9, P6 |

**Use in this project:** MQ-2 **heater** power only (~150 mA). ESP32 still from USB. Tie adapter **GND** to ESP32 **GND**. Do not power the MCU from this brick unless you know the 5 V rail is 5 V-tolerant on VIN only — this lab keeps USB for the DevKit.

**DMM:** **DC V** 20 V: adapter **+** to **−** ≈ **5.0 V** with no sensor, then again with MQ-2 connected (should stay near 5 V). Never measure AC on the wall pin.

**Buy:** **5 V**, **≥ 1 A**, Indian mains plug. You still need a way onto the breadboard (barrel jack + wires, or a USB 5 V brick **only** for the sensor, common GND).

| Shop | Link | Notes |
|------|------|-------|
| Robu (recommended) | https://robu.in/product/orange-5v-2a-power-supply-with-dual-pin-dc-plug-adapter/ | 5 V **2 A** wall wart. |
| Robu (higher current) | https://robu.in/product/pro-range-5v-3a-power-adapter/ | 5 V 3 A; confirm barrel size vs your jack. |
| Amazon | https://www.amazon.in/s?k=5V+2A+DC+adapter+5.5mm | Any regulated 5 V ≥1 A; not a 12 V laptop brick. |

---

## B11 — Digital multimeter

<img src="images/buy/buy-dmm.png" alt="Handheld DMM" width="280"/>

| Field | Spec |
|-------|------|
| Search terms | Any student DMM with **DC volts** |
| Use | Measure MQ-2 **AO vs GND** with heater at 5 V **before** GPIO 34 |
| Pass | AO stays **≤ 3.3 V** (or fit a divider) |
| Borrow | Lab DMM is fine; no need to buy if you have access |
| Used with | P6 |

**Use in this project:** Safety and bring-up instrument for **every** analog/power check. Full dial guide: [How we use the multimeter](#how-we-use-the-multimeter-b11).

**Features we use:** DC volts (20 V), ohms, diode (RGB), continuity. **Features we do not use:** AC volts, amps, hFE, 10 A jack.

**Buy only if** you cannot borrow a lab meter. DC volts is enough.

| Shop | Link | Notes |
|------|------|-------|
| Robu | https://robu.in/product/digital-multimeter-small-yellow-color-lcd-ac-dc-measuring-voltage-current/ | DT830-class student DMM. |
| Amazon | https://www.amazon.in/s?k=DT830D+digital+multimeter | Same class of meter. |

---

## B12 — USB fan (optional, P7)

<img src="images/buy/buy-fan.png" alt="Small USB fan" width="280"/>

| Field | Spec |
|-------|------|
| Search terms | `USB desk fan 5V` |
| Role | Airflow anecdote vs speed; **not** a vehicle speed sensor |
| Aim | At MQ-2, not at the ESP32 USB connector |
| Skip | Allowed — tick Skip P7 in the implementation plan |
| Used with | P7 only |

**Use in this project:** Optional **plant** anecdote: airflow past MQ-2 while speed pot still sets `T(v)`. Aim at the sensor, not the ESP32 USB plug. Skip P7 if you want.

**DMM:** none required. Optional **DC V** on a USB charger that powers the fan ≈ 5 V.

**Buy only if** you are doing P7. Any small **5 V USB** fan is enough.

| Shop | Link | Notes |
|------|------|-------|
| Robu | https://robu.in/product/dc-5v-5010-oil-containing-cooling-fan-with-usb-size505010mm/ | USB-A 5 V, 50 mm. |
| Shokitech | https://shokitech.com/product/8025-usb-cooling-fan-5v-0-27a-dual-ball-bearing-80x80x25mm-with-1m-cable/ | Larger USB fan. |
| Amazon | https://www.amazon.in/s?k=usb+desk+fan+5v | Desk fan is fine. |

---

## Extra — 10 kΩ resistors (AO divider)

Only if DMM shows MQ-2 **AO > 3.3 V**. Two ¼ W 10 kΩ in series as a 2:1 divider (or any equal pair). AO → top of divider, GND at bottom, **midpoint → GPIO 34**.

**DMM:** **Ω** each resistor ≈ 10 kΩ. After wiring: **DC V** at midpoint vs GND must be **≤ 3.3 V** (and still move when vapor/index changes).

| Shop | Link | Notes |
|------|------|-------|
| Amazon | https://www.amazon.in/s?k=10k+ohm+1%2F4+watt+resistor+pack | Two pieces from a pack. |

---

## Receive / desk checklist

Same items as `docs/implementation-plan.md` BUY section.

- [ ] B1 ESP32 enumerates (COM port)
- [ ] B2 data cable (not charge-only)
- [ ] B3 two **B10K** linear pots
- [ ] B4 128×64 I²C SSD1306
- [ ] B5 common-cathode RGB (or 3 LEDs) + 3× ~220 Ω
- [ ] B6 **active** buzzer
- [ ] B7 button
- [ ] B8 breadboard + Dupont
- [ ] B9 one MQ-2 module
- [ ] B10 5 V heater supply
- [ ] B11 DMM available
- [ ] B12 fan or explicitly skip P7
- [ ] Pin map open: `.cursor/skills/esp32-fuel-vapor/hardware.md`
