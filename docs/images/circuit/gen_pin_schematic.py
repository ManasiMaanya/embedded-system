"""KiCad-style pin schematic SVG. Run: python docs/images/circuit/gen_pin_schematic.py"""
from pathlib import Path

OUT = Path(__file__).with_name("pin-connection-schematic.svg")

# U1 box
UX, UY, UW, UH = 430, 80, 280, 820
PIN_L = 28


def pin_left(y, num, name, net):
    x0 = UX
    return f"""
  <line x1="{x0 - PIN_L}" y1="{y}" x2="{x0}" y2="{y}" stroke="#111" stroke-width="1.6"/>
  <rect x="{x0}" y="{y - 8}" width="22" height="16" fill="#fff" stroke="#111" stroke-width="1"/>
  <text x="{x0 + 11}" y="{y + 4}" text-anchor="middle" font-size="10" font-family="Consolas,monospace">{num}</text>
  <text x="{x0 + 28}" y="{y + 4}" font-size="11" font-family="Segoe UI,Arial" fill="#111">{name}</text>
  <text x="{x0 - PIN_L - 6}" y="{y - 6}" text-anchor="end" font-size="11" font-family="Consolas,monospace" fill="#1565c0">{net}</text>
"""


def pin_right(y, num, name, net):
    x1 = UX + UW
    return f"""
  <line x1="{x1}" y1="{y}" x2="{x1 + PIN_L}" y2="{y}" stroke="#111" stroke-width="1.6"/>
  <rect x="{x1 - 22}" y="{y - 8}" width="22" height="16" fill="#fff" stroke="#111" stroke-width="1"/>
  <text x="{x1 - 11}" y="{y + 4}" text-anchor="middle" font-size="10" font-family="Consolas,monospace">{num}</text>
  <text x="{x1 - 28}" y="{y + 4}" text-anchor="end" font-size="11" font-family="Segoe UI,Arial" fill="#111">{name}</text>
  <text x="{x1 + PIN_L + 6}" y="{y - 6}" font-size="11" font-family="Consolas,monospace" fill="#1565c0">{net}</text>
"""


def gnd(x, y):
    return f"""
  <line x1="{x}" y1="{y}" x2="{x}" y2="{y + 10}" stroke="#111" stroke-width="1.4"/>
  <line x1="{x - 12}" y1="{y + 10}" x2="{x + 12}" y2="{y + 10}" stroke="#111" stroke-width="1.6"/>
  <line x1="{x - 8}" y1="{y + 16}" x2="{x + 8}" y2="{y + 16}" stroke="#111" stroke-width="1.4"/>
  <line x1="{x - 4}" y1="{y + 22}" x2="{x + 4}" y2="{y + 22}" stroke="#111" stroke-width="1.2"/>
"""


def box(x, y, w, h, title, dashed=False):
    dash = ' stroke-dasharray="6 4"' if dashed else ""
    return f"""
  <rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#fff" stroke="#111" stroke-width="1.6"{dash}/>
  <text x="{x + 8}" y="{y + 16}" font-size="12" font-weight="700" font-family="Segoe UI,Arial">{title}</text>
"""


parts = []
parts.append(
    f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 980" width="1600" height="980">
  <rect width="1600" height="980" fill="#ffffff"/>
  <text x="800" y="28" text-anchor="middle" font-size="18" font-weight="700" font-family="Segoe UI,Arial">U1 ESP32 DevKit V1 — pin connections (this capstone)</text>
  <text x="800" y="50" text-anchor="middle" font-size="12" font-family="Segoe UI,Arial" fill="#333">Nets match firmware/src/pins.h. GPIO34 = Fig A RV2 xor Fig B MQ-2 AO. Never 5 V on GPIO.</text>

  <rect x="{UX}" y="{UY}" width="{UW}" height="{UH}" fill="#fff" stroke="#111" stroke-width="2"/>
  <text x="{UX + UW / 2}" y="{UY + 28}" text-anchor="middle" font-size="14" font-weight="700" font-family="Segoe UI,Arial">U1</text>
  <text x="{UX + UW / 2}" y="{UY + 48}" text-anchor="middle" font-size="12" font-family="Segoe UI,Arial">ESP32-WROOM-32</text>
  <text x="{UX + UW / 2}" y="{UY + 66}" text-anchor="middle" font-size="11" font-family="Segoe UI,Arial">DevKit V1 30-pin</text>
"""
)

# Left pins (USB / power / ADC)
left = [
    (120, "USB", "5V_USB", "B2 VBUS (MCU only)"),
    (170, "GND", "GND", "USB GND"),
    (230, "3V3", "VDD_3V3", "logic rail"),
    (280, "GND", "GND", "logic GND"),
    (350, "34", "GPIO34", "VAPOR_ADC"),
    (410, "33", "GPIO33", "SPEED_ADC"),
    (480, "25", "GPIO25", "LED_R"),
    (530, "26", "GPIO26", "LED_G"),
    (580, "27", "GPIO27", "LED_B"),
    (650, "13", "GPIO13", "BUZZ"),
    (710, "4", "GPIO4", "BTN_CAL"),
    (780, "2", "GPIO2", "LED_BUILTIN"),
]
for y, num, name, net in left:
    parts.append(pin_left(y, num, name, net))

right = [
    (230, "21", "GPIO21", "I2C_SDA"),
    (280, "22", "GPIO22", "I2C_SCL"),
]
for y, num, name, net in right:
    parts.append(pin_right(y, num, name, net))

# USB block
parts.append(box(40, 90, 200, 110, "J1  USB  (B2)"))
parts.append(
    """
  <text x="50" y="128" font-size="11" font-family="Segoe UI,Arial">1 VBUS → U1 USB 5 V</text>
  <text x="50" y="146" font-size="11" font-family="Segoe UI,Arial">2 D−  → on-board UART</text>
  <text x="50" y="164" font-size="11" font-family="Segoe UI,Arial">3 D+  → on-board UART</text>
  <text x="50" y="182" font-size="11" font-family="Segoe UI,Arial">5 GND → GND</text>
  <line x1="240" y1="120" x2="402" y2="120" stroke="#111" stroke-width="1.4"/>
"""
)
parts.append(gnd(80, 188))

# VDD_3V3 rail note
parts.append(
    """
  <text x="48" y="248" font-size="11" font-family="Consolas,monospace" fill="#1565c0">VDD_3V3</text>
  <text x="48" y="264" font-size="10" font-family="Segoe UI,Arial">pots high side, OLED VCC</text>
"""
)

# RV1
parts.append(box(40, 380, 210, 100, "RV1  10k B  SPEED  (B3a)"))
parts.append(
    """
  <text x="50" y="418" font-size="11" font-family="Segoe UI,Arial">end 1 → VDD_3V3</text>
  <text x="50" y="436" font-size="11" font-family="Segoe UI,Arial">wiper → SPEED_ADC (GPIO33)</text>
  <text x="50" y="454" font-size="11" font-family="Segoe UI,Arial">end 2 → GND</text>
  <line x1="250" y1="410" x2="402" y2="410" stroke="#111" stroke-width="1.4"/>
"""
)
parts.append(gnd(70, 458))

# RV2 dashed
parts.append(box(40, 500, 210, 110, "RV2  10k B  VAPOR  (B3b)", dashed=True))
parts.append(
    """
  <text x="50" y="538" font-size="11" font-family="Segoe UI,Arial">FIG A only  (DRY_POT 1)</text>
  <text x="50" y="556" font-size="11" font-family="Segoe UI,Arial">end 1 → VDD_3V3</text>
  <text x="50" y="574" font-size="11" font-family="Segoe UI,Arial">wiper → VAPOR_ADC (GPIO34)</text>
  <text x="50" y="592" font-size="11" font-family="Segoe UI,Arial">end 2 → GND</text>
"""
)

# Right column components
parts.append(box(820, 90, 280, 130, "U2  SSD1306 128×64  (B4)"))
parts.append(
    """
  <text x="830" y="128" font-size="11" font-family="Segoe UI,Arial">VCC → VDD_3V3</text>
  <text x="830" y="146" font-size="11" font-family="Segoe UI,Arial">GND → GND</text>
  <text x="830" y="164" font-size="11" font-family="Segoe UI,Arial">SDA → I2C_SDA (GPIO21)</text>
  <text x="830" y="184" font-size="11" font-family="Segoe UI,Arial">SCL → I2C_SCL (GPIO22)   addr 0x3C</text>
  <line x1="738" y1="230" x2="820" y2="164" stroke="#111" stroke-width="1.4"/>
  <line x1="738" y1="280" x2="820" y2="184" stroke="#111" stroke-width="1.4"/>
"""
)
parts.append(gnd(860, 188))

parts.append(box(820, 240, 280, 150, "D1 RGB CC + R1–R3 220Ω  (B5)"))
parts.append(
    """
  <text x="830" y="278" font-size="11" font-family="Segoe UI,Arial">R1 220Ω: GPIO25 → R anode</text>
  <text x="830" y="296" font-size="11" font-family="Segoe UI,Arial">R2 220Ω: GPIO26 → G anode</text>
  <text x="830" y="314" font-size="11" font-family="Segoe UI,Arial">R3 220Ω: GPIO27 → B anode</text>
  <text x="830" y="332" font-size="11" font-family="Segoe UI,Arial">common cathode → GND</text>
  <text x="830" y="350" font-size="11" font-family="Segoe UI,Arial">active HIGH  (not common anode)</text>
  <line x1="402" y1="480" x2="430" y2="480" stroke="#111" stroke-width="1.2"/>
"""
)
parts.append(gnd(860, 354))

parts.append(box(820, 410, 280, 90, "LS1  active buzzer  (B6)"))
parts.append(
    """
  <text x="830" y="448" font-size="11" font-family="Segoe UI,Arial">+  → BUZZ (GPIO13)</text>
  <text x="830" y="466" font-size="11" font-family="Segoe UI,Arial">−  → GND     (not passive piezo)</text>
"""
)
parts.append(gnd(860, 468))

parts.append(box(820, 520, 280, 100, "SW1  tactile  (B7)"))
parts.append(
    """
  <text x="830" y="558" font-size="11" font-family="Segoe UI,Arial">A → BTN_CAL (GPIO4)</text>
  <text x="830" y="576" font-size="11" font-family="Segoe UI,Arial">B → GND</text>
  <text x="830" y="594" font-size="11" font-family="Segoe UI,Arial">U1 INPUT_PULLUP  press = LOW</text>
"""
)
parts.append(gnd(860, 598))

parts.append(box(820, 640, 360, 160, "U3  MQ-2  (B9)  +  J2 5 V  (B10)", dashed=True))
parts.append(
    """
  <text x="830" y="678" font-size="11" font-family="Segoe UI,Arial">FIG B only  (DRY_POT 0). Remove RV2 first.</text>
  <text x="830" y="696" font-size="11" font-family="Segoe UI,Arial">U3 VCC → J2 +5 V heater  (not VDD_3V3)</text>
  <text x="830" y="714" font-size="11" font-family="Segoe UI,Arial">U3 GND → GND  (common with U1)</text>
  <text x="830" y="732" font-size="11" font-family="Segoe UI,Arial">U3 AO  → VAPOR_ADC (GPIO34) after DMM ≤3.3 V</text>
  <text x="830" y="750" font-size="11" font-family="Segoe UI,Arial">U3 DO  → NC</text>
  <text x="830" y="768" font-size="11" font-family="Segoe UI,Arial">Extra 2×10k divider if AO &gt; 3.3 V (mid → 34)</text>
"""
)
parts.append(gnd(860, 772))

parts.append(box(40, 640, 210, 90, "LED  on-board"))
parts.append(
    """
  <text x="50" y="678" font-size="11" font-family="Segoe UI,Arial">GPIO2  no jumper</text>
  <text x="50" y="696" font-size="11" font-family="Segoe UI,Arial">warm-up blink (P1)</text>
"""
)

parts.append(box(40, 750, 210, 80, "FAN B12  optional"))
parts.append(
    """
  <text x="50" y="788" font-size="11" font-family="Segoe UI,Arial">own USB 5 V  — no GPIO</text>
"""
)

parts.append(
    """
  <rect x="1140" y="90" width="430" height="200" fill="#fafafa" stroke="#111" stroke-width="1"/>
  <text x="1152" y="112" font-size="12" font-weight="700" font-family="Segoe UI,Arial">Net legend</text>
  <text x="1152" y="134" font-size="12" font-family="Consolas,monospace" fill="#1565c0">VDD_3V3</text>
  <text x="1280" y="134" font-size="11" font-family="Segoe UI,Arial">ESP32 3V3 pin</text>
  <text x="1152" y="154" font-size="12" font-family="Consolas,monospace" fill="#1565c0">VAPOR_ADC</text>
  <text x="1280" y="154" font-size="11" font-family="Segoe UI,Arial">GPIO34  one source</text>
  <text x="1152" y="174" font-size="12" font-family="Consolas,monospace" fill="#1565c0">SPEED_ADC</text>
  <text x="1280" y="174" font-size="11" font-family="Segoe UI,Arial">GPIO33  RV1 wiper</text>
  <text x="1152" y="194" font-size="12" font-family="Consolas,monospace" fill="#1565c0">I2C_SDA / SCL</text>
  <text x="1280" y="194" font-size="11" font-family="Segoe UI,Arial">GPIO21 / 22</text>
  <text x="1152" y="214" font-size="12" font-family="Consolas,monospace" fill="#1565c0">LED_R/G/B</text>
  <text x="1280" y="214" font-size="11" font-family="Segoe UI,Arial">GPIO25 / 26 / 27</text>
  <text x="1152" y="234" font-size="12" font-family="Consolas,monospace" fill="#1565c0">BUZZ / BTN_CAL</text>
  <text x="1280" y="234" font-size="11" font-family="Segoe UI,Arial">GPIO13 / GPIO4</text>
  <text x="1152" y="258" font-size="11" font-family="Segoe UI,Arial">Dashed boxes = optional / phase-select.</text>
  <text x="1152" y="276" font-size="11" font-family="Segoe UI,Arial">On-board CP2102/CH340 is inside U1 (not wired).</text>

  <text x="800" y="960" text-anchor="middle" font-size="11" font-family="Segoe UI,Arial" fill="#444">Source of truth: this SVG + pins.h. Illustrated PNG is style-only if labels disagree.</text>
</svg>
"""
)

OUT.write_text("".join(parts), encoding="utf-8")
print("wrote", OUT)
