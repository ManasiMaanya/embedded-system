# Hardware reference

Single tank MQ-2 + speed potentiometer. Change firmware and this file together.

## BOM (class budget ~₹2000)

| Item | Qty | Role |
|------|-----|------|
| ESP32 DevKit | 1 | MCU, 3.3 V logic |
| MQ-2 module | 1 | Fuel-tank vapor index (AO) |
| 10 kΩ potentiometer | 1 | Simulated vehicle speed 0–120 km/h |
| 10 kΩ potentiometer | 1 | Optional: dry vapor stand-in (see tests.md) |
| SSD1306 OLED 128×64 I²C | 1 | Show v, delta, T_mod, T_high, state |
| Common-cathode RGB + ~220 Ω | 1 | Safe / moderate / high |
| Active buzzer | 1 | Intermittent / continuous |
| Tactile button | 1 | Recapture baseline |
| 5 V adapter | 1 | MQ-2 heater; common GND with ESP32 |
| USB fan (5 V) | 1 | Optional: airflow vs speed story |
| Breadboard, wires, AO divider if needed | — | AO must stay ≤ 3.3 V |

## Pin map (ESP32 DevKit V1)

| Function | GPIO | ADC | Notes |
|----------|------|-----|--------|
| MQ-2 tank AO | 34 | ADC1_CH6 | Input-only. Or vapor-sim pot on this pin (not both). |
| Speed pot wiper | 33 | ADC1_CH5 | Ends: 3V3 and GND |
| OLED SDA | 21 | — | I²C |
| OLED SCL | 22 | — | I²C |
| RGB red | 25 | — | Out |
| RGB green | 26 | — | Out |
| RGB blue | 27 | — | Out |
| Buzzer | 13 | — | Out |
| Recalibrate | 4 | — | INPUT_PULLUP to GND |
| On-board LED | 2 | — | Warm-up blink |

OLED address `0x3C` (try `0x3D` if needed).

## Power

- ESP32 from USB.
- MQ-2 **heater VCC = 5 V** from the adapter, not the ESP32 3V3 pin (~150 mA heater).
- Common ground: USB, 5 V brick, pots, OLED, MQ-2.
- Measure MQ-2 AO with a DMM at 5 V heater power. If AO can exceed 3.3 V, add a divider before GPIO 34.

## Speed pot wiring

```
3V3 ----[pot]---- GND
          |
        GPIO 33 (wiper)
```

Map in firmware: `v_kmh = (adc / 4095) * 120`. Label the pot “speed” on the board.

## MQ-2 vs dry vapor pot

Never parallel MQ-2 AO and a second pot on GPIO 34. Either:

- **Chemical / sensor run:** MQ-2 AO → GPIO 34, or
- **Dry algorithm run:** vapor pot wiper → GPIO 34 (3V3–GND like the speed pot).

## Adaptive constants (tune here after tests)

Document the values used in `firmware/src/main.cpp`:

- `T_MOD_0`, `K_MOD`
- `T_HIGH_0`, `K_HIGH`

Default start: `T_mod = 180 + 0.8 v`, `T_high = 420 + 1.2 v` (ADC delta counts, 12-bit averaged). Replace after Experiment 1–2 in tests.md.

## RGB

Common cathode, active high. Yellow = R+G. If the LED is common anode, invert writes and note it here.
