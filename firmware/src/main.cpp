#include <Arduino.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include "pins.h"
#include "math_params.h"

namespace {

#if DRY_POT
constexpr uint32_t kWarmupMs = 2000;
#else
constexpr uint32_t kWarmupMs = 60000;
#endif

enum class Alert : uint8_t { Warmup, Safe, Moderate, High };

Adafruit_SSD1306 oled(128, 64, &Wire, -1);

uint16_t baseline;
uint32_t warmupEnd;
uint32_t lastBeepToggle;
uint32_t lastLog;
bool buzzerOn;
Alert alert = Alert::Warmup;
bool oledOk;

uint16_t avgRead(int pin) {
  uint32_t sum = 0;
  for (int i = 0; i < kAvgSamples; ++i) {
    sum += analogRead(pin);
  }
  return static_cast<uint16_t>(sum / kAvgSamples);
}

void captureBaseline() { baseline = avgRead(PIN_MQ_TANK); }

int16_t deltaOf(uint16_t raw, uint16_t base) {
  return raw > base ? static_cast<int16_t>(raw - base) : 0;
}

void setRgb(bool r, bool g, bool b) {
  digitalWrite(PIN_LED_R, r);
  digitalWrite(PIN_LED_G, g);
  digitalWrite(PIN_LED_B, b);
}

void showStudy(Alert a, int16_t d, float speed, float tMod, float tHigh) {
  if (!oledOk) {
    return;
  }
  const char *st = "WARM";
  if (a == Alert::Safe) {
    st = "SAFE";
  } else if (a == Alert::Moderate) {
    st = "MOD";
  } else if (a == Alert::High) {
    st = "HIGH";
  }
  oled.clearDisplay();
  oled.setTextSize(1);
  oled.setTextColor(SSD1306_WHITE);
  oled.setCursor(0, 0);
  oled.println("Tank vapor");
  oled.printf("d=%d  v=%.0f km/h\n", d, speed);
  oled.printf("Tm=%.0f Th=%.0f\n", tMod, tHigh);
  oled.println(st);
  oled.display();
}

}  // namespace

void setup() {
  Serial.begin(115200);
  pinMode(PIN_LED_R, OUTPUT);
  pinMode(PIN_LED_G, OUTPUT);
  pinMode(PIN_LED_B, OUTPUT);
  pinMode(PIN_BUZZER, OUTPUT);
  pinMode(PIN_BTN_CAL, INPUT_PULLUP);
  pinMode(LED_BUILTIN, OUTPUT);
  analogSetAttenuation(ADC_11db);
  setRgb(false, false, false);
  digitalWrite(PIN_BUZZER, LOW);

  Wire.begin(PIN_OLED_SDA, PIN_OLED_SCL);
  oledOk = oled.begin(SSD1306_SWITCHCAPVCC, 0x3C);
  if (!oledOk) {
    Serial.println("OLED not found at 0x3C");
  }

  warmupEnd = millis() + kWarmupMs;
  Serial.println("t_ms,raw,baseline,delta,speed,Tmod,Thigh,state");
}

void loop() {
  const uint16_t raw = avgRead(PIN_MQ_TANK);
  const uint16_t pot = avgRead(PIN_SPEED_POT);
  const float speed = (pot / kAdcMax) * kVmaxKmh;
  const float tMod = kTmod0 + kKmod * speed;
  const float tHigh = kThigh0 + kKhigh * speed;
  const int16_t d = (alert == Alert::Warmup) ? 0 : deltaOf(raw, baseline);

  if (alert == Alert::Warmup) {
    showStudy(alert, 0, speed, tMod, tHigh);
    if (millis() < warmupEnd) {
      digitalWrite(LED_BUILTIN, (millis() / 250) % 2);
      delay(20);
      return;
    }
    captureBaseline();
    alert = Alert::Safe;
  }

  if (digitalRead(PIN_BTN_CAL) == LOW) {
    delay(30);
    if (digitalRead(PIN_BTN_CAL) == LOW) {
      captureBaseline();
      while (digitalRead(PIN_BTN_CAL) == LOW) {
      }
    }
  }

  const int enterMod = static_cast<int>(tMod);
  const int enterHigh = static_cast<int>(tHigh);
  if (d >= enterHigh) {
    alert = Alert::High;
  } else if (d >= enterMod) {
    alert = Alert::Moderate;
  } else if (d < enterMod - kHyst) {
    alert = Alert::Safe;
  }

  switch (alert) {
    case Alert::Safe:
      setRgb(false, true, false);
      digitalWrite(PIN_BUZZER, LOW);
      break;
    case Alert::Moderate:
      setRgb(true, true, false);
      if (millis() - lastBeepToggle >= 300) {
        lastBeepToggle = millis();
        buzzerOn = !buzzerOn;
        digitalWrite(PIN_BUZZER, buzzerOn);
      }
      break;
    case Alert::High:
      setRgb(true, false, false);
      digitalWrite(PIN_BUZZER, HIGH);
      break;
    default:
      break;
  }

  showStudy(alert, d, speed, tMod, tHigh);

  if (millis() - lastLog >= 500) {
    lastLog = millis();
    Serial.printf("%lu,%u,%u,%d,%.1f,%.0f,%.0f,%d\n", millis(), raw, baseline, d, speed,
                  tMod, tHigh, static_cast<int>(alert));
  }
}
