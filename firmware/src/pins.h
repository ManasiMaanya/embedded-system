#pragma once

// Must match .cursor/skills/esp32-fuel-vapor/hardware.md

#define PIN_MQ_TANK 34
#define PIN_SPEED_POT 33

#define PIN_OLED_SDA 21
#define PIN_OLED_SCL 22

#define PIN_LED_R 25
#define PIN_LED_G 26
#define PIN_LED_B 27
#define PIN_BUZZER 13
#define PIN_BTN_CAL 4

// 1 = short warm-up for two-pot dry tests (no MQ-2 heater)
#define DRY_POT 1
